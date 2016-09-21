# -*- coding: utf-8 -*-
import sys, getopt, logging, datetime , sqlite3
from TunnelSegment import *
from tbmconfig import *
from pylab import *
import matplotlib.pyplot as plt
from bbt_database import *
import os,  csv
from bbtutils import *
from bbtnamedtuples import *
from tbmkpi import *
from collections import namedtuple
from pprint import pprint
from tbmkpi import FrictionCoeff
from multiprocessing import cpu_count, Pool
from logging import handlers
from time import time as ttime
from time import sleep as tsleep
import random

# danzi.tn@20151119 generazione variabili random per condizioni geotecniche
def insert_georandom(sDBPath,nIter, bbt_parameters, sKey):
    delete_eval4Geo(sDBPath,sKey)
    now = datetime.datetime.now()
    strnow = now.strftime("%Y%m%d%H%M%S")
    bbt_insertval = []
    for idx, bbt_parameter in enumerate(bbt_parameters):
        mynorms = build_normfunc_dict(bbt_parameter, nIter)
        for n in range(nIter):
            gamma = mynorms['gamma'].rvs()
            sci = mynorms['sci'].rvs()
            mi = mynorms['mi'].rvs()
            ei = mynorms['ei'].rvs()
            cai = mynorms['cai'].rvs()
            gsi = mynorms['gsi'].rvs()
            rmr =  mynorms['rmr'].rvs()
            sti = mynorms['sti'].rvs()
            #aghensi@20160715 - inutile, calcolo k0 da k0min e max
            #k0 = mynorms['k0'].rvs()
            bbt_insertval.append((strnow, n, sKey, sKey, bbt_parameter.fine, bbt_parameter.he,
                                  bbt_parameter.hp, bbt_parameter.co, bbt_parameter.wdepth,
                                  gamma, sci, mi, ei, cai, gsi,
                                  rmr, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  bbt_parameter.profilo_id, bbt_parameter.geoitem_id,
                                  bbt_parameter.title, sti, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, bbt_parameter.anidrite))
        if (idx+1) % 100 == 0:
            insert_eval4Geo(sDBPath,bbt_insertval)
            bbt_insertval = []
    if len(bbt_insertval) > 0:
        print "ultimi %d da inserire" % len(bbt_insertval)
        insert_eval4Geo(sDBPath,bbt_insertval)


def createLogger(indx=0, logger_name="main_loop"):
    '''
    creates main logger and a rotating file handler
    '''
    logger = logging.getLogger("%s_%02d" % (logger_name,indx))
    if not len(logger.handlers):
        # Log su file
        log_level = bbtConfig.get('MAIN_LOOP','log_level')
        logger.setLevel(eval("logging.%s"%log_level))

        file_handler = logging.handlers.RotatingFileHandler("%s_%02d.log" % (logger_name,indx),
                                                            maxBytes=5000000, backupCount=5)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(funcName)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # aghensi@20160502 - messaggi critici anche su stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_formatter = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s - %(message)s')
        stdout_handler.setFormatter(stdout_formatter)
        logger.addHandler(stdout_handler)
        logger.handler_set = True
    return logger

if __name__ == "__main__":
    sKey = "XXX"
    main_logger = createLogger()
    main_logger.info("__main__ Started!")
    mp_np = cpu_count() - 1
    argv = sys.argv[1:]
    loopTbms = {}
    nIter = 0
    bPerformTBMClean = False
    bGeorandom = True
    sTbmCode =""
    sParm = "\n g,skipgeo per saltare la generazione dei parametri geotecnici\n"
    sParm += "\n t,tbmcode  in \n"
    for k in tbms:
        sParm += "\t%s - Produttore %s di tipo %s per tunnel %s\r\n" % (k,tbms[k].manifacturer, tbms[k].type, tbms[k].alignmentCode)
    try:
        opts, args = getopt.getopt(argv,"hn:dt:g",["iteration_no=","deletetbms=","tbmcode=","skipgeo"])
    except getopt.GetoptError:
        print "main_loop_mp.py -n <number of iteration (positive integer)> [-t <tbmcode>] [-g]\n\tCi sono %d processori disponibili\n%s" % (mp_np, sParm)
        sys.exit(2)
    if len(opts) < 1:
        print "main_loop_mp.py -n <number of iteration (positive integer)> [-t <tbmcode>] [-g]\n\tCi sono %d processori disponibili\n%s" % (mp_np, sParm)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "main_loop_mp.py -n <number of iteration (positive integer)> [-t <tbmcode>] [-g]\n\tCi sono %d processori disponibili\n%s" % (mp_np, sParm)
            sys.exit()
        elif opt in ("-n", "--iteration_no"):
            try:
                nIter = int(arg)
            except ValueError:
                print "main_loop_mp.py -n <number of iteration (positive integer)> [-t <tbmcode>] [-g]\n\tCi sono %d processori disponibili\n%s" % (mp_np, sParm)
                sys.exit(2)
        elif opt in ("-d", "--deletetbms"):
            bPerformTBMClean = True
        elif opt in ("-g", "--skipgeo"):
            bGeorandom = False
        elif opt in ("-t", "--tbmcode"):
            sTbmCode = arg

            loopTbms[sTbmCode] = tbms[sTbmCode]
    if nIter > 0:
        number_of_threads = bbtConfig.getint('MAIN_LOOP','number_of_threads')
        wait_before_start = bbtConfig.getint('MAIN_LOOP','wait_before_start')
        mp_np = number_of_threads * mp_np
        main_logger.info("Richieste %d iterazioni" % nIter )
        # mi metto nella directory corrente
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)
        main_logger.info("Percorso di esecuzione %s" % path )
        ########## File vari: DB
        sDBName = bbtConfig.get('Database','dbname')
        sDBPath = os.path.join(os.path.abspath('..'), bbtConfig.get('Database','dbfolder'), sDBName)
        main_logger.info("Database utilizzato %s" % sDBPath )
        if not os.path.isfile(sDBPath):
            main_logger.error( "Errore! File %s inesistente!" % sDBPath)
        bbt_parameters = []
        bbt_parameters = get_bbtparameters(sDBPath)
        if len(bbt_parameters) == 0:
            main_logger.error( "Attenzione! Nel DB %s non ci sono i dati necessari!" % sDBPath)

        main_logger.info("Ci sono %d pk" % len(bbt_parameters) )
        totIterations = mp_np*nIter
        if bGeorandom:
            geo_start_time = ttime()
            insert_georandom(sDBPath,totIterations, bbt_parameters, sKey)
            geo_tot_time = ttime() - geo_start_time
            main_logger.info("Generazione dei parametri geotecnici per %d iterazioni su %d segmenti ha richiesto %d secondi" % (totIterations,len(bbt_parameters) ,geo_tot_time ) )
        else:
            main_logger.info("Generazione dei parametri geotecnici saltata")
            iMax = check_eval4Geo(sDBPath,"XXX")
            if iMax >= totIterations:
                main_logger.info("Sono disponibili %d iterazioni" % iMax)
            else:
                main_logger.info("Ci sono %d iterazioni disponibili per i parametri geotecnici su totali %d necessarie, ci sono ancora da generare %d iterazioni!" % (iMax,totIterations, totIterations - iMax))
                raise ValueError("Ci sono %d iterazioni disponibili per i parametri geotecnici su totali %d necessarie, ci sono ancora da generare %d iterazioni!" % (iMax,totIterations, totIterations - iMax))
        # danzi.tn@20151116
        if bPerformTBMClean:
            main_logger.info("Richiesta la cancellazione di tutti i dati")
            clean_all_eval_ad_kpi(sDBPath)
            compact_database(sDBPath)
        end_time = ttime()
        main_logger.info("Processo principale terminato")
    else:
        print "main_loop_mp.py -n <number of iteration (positive integer)>\n\tCi sono %d processori disponibili" % mp_np
