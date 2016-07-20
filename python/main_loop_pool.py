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
            bbt_insertval.append((strnow, n, sKey, sKey, bbt_parameter.inizio, bbt_parameter.fine, bbt_parameter.he,
                                  bbt_parameter.hp, bbt_parameter.co, bbt_parameter.wdepth,
                                  gamma, sci, mi, ei, cai, gsi,
                                  rmr, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  bbt_parameter.profilo_id, bbt_parameter.geoitem_id,
                                  bbt_parameter.title, sti, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, bbt_parameter.anidrite,
                                  bbt_parameter.k0_min,bbt_parameter.k0_max,bbt_parameter.perc))
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
        stdout_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(stdout_formatter)
        logger.addHandler(stdout_handler)
        logger.handler_set = True
    return logger


# danzi.tn@20151114 gestione main e numero di iterazioni da linea comando
# danzi.tn@20151117 versione multithread
# danzi.tn@20151118 gestione loop per singola TBM
def mp_producer(parms):
    idWorker,  nIter, sDBPath, loopTbms, sKey, np = parms
    # ritardo per evitare conflitti su DB
    # commentare per velocizzare debug in single thread
    tsleep(idWorker*10+1)
    start_time = ttime()
    now = datetime.datetime.now()
    strnow = now.strftime("%Y%m%d%H%M%S")
    main_logger = createLogger(idWorker,"mp_producer")
    main_logger.info("[%d]############################# Starts at %s" % (idWorker,strnow))
    #with plock:
    #    print "[%d]############################# Starts at %s" % (idWorker,strnow)


    #inizializzo le info sui tracciati dai file di configurazione
    inizio_GLEST = bbtConfig.getfloat('Import','inizio_GLEST')
    fine_GLEST = bbtConfig.getfloat('Import','fine_GLEST')
    inizio_GLSUD = bbtConfig.getfloat('Import','inizio_GLSUD')
    fine_GLSUD = bbtConfig.getfloat('Import','fine_GLSUD')
    inizio_CE = bbtConfig.getfloat('Import','inizio_CE')
    fine_CE = bbtConfig.getfloat('Import','fine_CE')
    #differenza tra CE e GLEST in modo tale che GLNORD = delta_GLEST_CE - CE
    delta_GLEST_CE =  bbtConfig.getfloat('Import','delta_GLEST_CE')
    projectRefCost = bbtConfig.getfloat('Import','project_ref_cost') # mln di euro

    # danzi.tn@20151115 recepimento modifiche su InfoAlignment fatte da Garbriele
    #LEGGO I PARAMETRI DA FILE DI CONFIGURAZIONE
    fCShiledMin = bbtConfig.getfloat('Alignment','frictionCShiledMin')
    fCShiledMode = bbtConfig.getfloat('Alignment','frictionCShiledMode')
    fCShiledMax = bbtConfig.getfloat('Alignment','frictionCShiledMax')
    #CREO OGGETTO
    fcShield = FrictionCoeff(fCShiledMin,fCShiledMode,fCShiledMax)

    #LEGGO I PARAMETRI DA FILE DI CONFIGURAZIONE
    fCCutterdMin = bbtConfig.getfloat('Alignment','frictionCCutterMin')
    fCCutterMode = bbtConfig.getfloat('Alignment','frictionCCutterMode')
    fCCutterMax = bbtConfig.getfloat('Alignment','frictionCCutterMax')
    #CREO OGGETTO
    fcCutter =  FrictionCoeff(fCCutterdMin,fCCutterMode,fCCutterMax)

    # aghensi@20160713 - aggiunti parametri per rapporti Thrust e pressioni su conci
    minRequiredContactThrustRatio = bbtConfig.getfloat('TBM', 'minRequiredContactThrustRatio')
    liningRelaxationRatio = bbtConfig.getfloat('TBM', 'liningRelaxationRatio')

    alnAll = []
#    aln=InfoAlignment('GL Sud', 'GLSUD', inizio_GLSUD, fine_GLSUD,fCCutterMode, fCShiledMode)
#    alnAll.append(aln)
    aln=InfoAlignment('CE', 'CE', delta_GLEST_CE - fine_CE, delta_GLEST_CE - inizio_CE , fCCutterMode, fCShiledMode)
    alnAll.append(aln)
    aln=InfoAlignment('GL Nord', 'GLNORD',inizio_GLEST, fine_GLEST, fCCutterMode, fCShiledMode)
    alnAll.append(aln)

    kpiTbmList = []
    main_logger.debug("[%d]############################# Inizia a recuperare le iterazioni di %s dalla %d alla %d" % (idWorker,sKey,idWorker*nIter, (idWorker+1)*nIter))
    bbt_bbtparameterseval = get_mainbbtparameterseval(sDBPath, sKey, idWorker*nIter, (idWorker+1)*nIter)
    main_logger.debug("[%d]############################# ...recuperate %d iterazioni, memoria totale" % (idWorker,len(bbt_bbtparameterseval)))
    for iIterationNo in range(nIter):
        mainIterationNo = idWorker*nIter + iIterationNo
        # genero valore probabilità in base all'iterazione
        par_prob = float(mainIterationNo+1)/float(nIter*np)
        tbmSegmentCum = 0
        iter_start_time = ttime()
        bbttbmkpis = []
        bbt_evalparameters = []
        iCheckEvalparameters = 0
        iCheckBbttbmkpis = 0
        # Per tutti i Tunnel
        main_logger.info("[%d]########### iteration %d - %d" % (idWorker, iIterationNo, mainIterationNo))        #with plock:
        #    print "[%d]########### iteration %d - %d" % (idWorker, iIterationNo, mainIterationNo)
        for alnCurr in alnAll:
            for tbmKey in loopTbms:
                tbmData = loopTbms[tbmKey]
                # Se la TBM e' conforme al TUnnel
                if alnCurr.tbmKey in tbmData.alignmentCode:
                    tbm = TBM(tbmData, 'V')
                    kpiTbm = KpiTbm4Tunnel(alnCurr.description, mainIterationNo)
                    iCheckBbttbmkpis += 1
                    kpiTbm.setKPI4TBM(alnCurr,tbmKey,tbm,projectRefCost)
                    # cerco i segmenti che rientrano tra inizio e fine del Tunnel
                    # aghensi@20160704 - ci sono più bbt_parameter multipli per la stessa pk - inizio
                    cur_fine = float("inf")
                    par_found = False
                    cum_prob = 0
                    matches_params = [bpar for bpar in bbt_bbtparameterseval[mainIterationNo] if alnCurr.pkStart <= bpar.inizio and bpar.fine <= alnCurr.pkEnd]
                    for bbt_parameter in matches_params:
                        if bbt_parameter.fine != cur_fine:
                            if not par_found and cur_fine != float("inf"):
                                main_logger.error("non ho trovato il title per la pk %s", cur_fine)
                            # nuova pk, resetto variabili controllo
                            cur_fine = bbt_parameter.fine
                            par_found = False
                            cum_prob = 0
                        if not par_found:
                            # non ho ancora trovato la pk con la giusta probabilità, controllo
                            cum_prob += bbt_parameter.perc
                            if par_prob - cum_prob <= 0.001:
                                par_found = True
                                # aghensi@20160704 - ci sono più bbt_parameter multipli per la stessa pk - fine
                                bbtparameter4seg = build_bbtparameterVal4seg(bbt_parameter)
                                iCheckEvalparameters += 1
                                if bbtparameter4seg == None:
                                    main_logger.error("[%d] %s, %s per pk %d parametri Geo non trovati" % (idWorker, alnCurr.description, tbmKey, bbt_parameter.fine) )
                                    continue
                                # danzi.tn@20151115 recepimento modifiche su InfoAlignment fatte da Garbriele
                                if iIterationNo > 2:
                                    alnCurr.frictionCoeff = fcShield.rvs()
                                    alnCurr.fiRi = fcCutter.rvs()
                                else:
                                    alnCurr.frictionCoeff = fCShiledMode
                                    alnCurr.fiRi = fCCutterMode
                                try:
                                    tbmSegBefore = ttime()
                                    tbmsect = TBMSegment(bbtparameter4seg, tbm, alnCurr.fiRi, alnCurr.frictionCoeff, minRequiredContactThrustRatio, liningRelaxationRatio)
                                    tbmSegAfter = ttime()
                                    tbmSegmentCum += (tbmSegAfter - tbmSegBefore)
                                except Exception as e:
                                    main_logger.error("[%d] %s, %s per pk %d TBMSegment va in errore: %s", idWorker, alnCurr.description, tbmKey, bbt_parameter.fine, e)
                                    main_logger.error("[%d] bbtparameter4seg = %s", idWorker, str(bbtparameter4seg))
                                    continue
                                kpiTbm.setKPI4SEG(alnCurr,tbmsect,bbtparameter4seg)
                                #☻danzi.tn@20151114 inseriti nuovi parametri calcolati su TunnelSegment
                                bbt_evalparameters.append((
                                    strnow, mainIterationNo, alnCurr.description, tbmKey,
                                    bbt_parameter.fine, bbt_parameter.he, bbt_parameter.hp,
                                    bbt_parameter.co, bbt_parameter.wdepth, bbtparameter4seg.gamma,
                                    bbtparameter4seg.sci, bbtparameter4seg.mi, bbtparameter4seg.ei,
                                    bbtparameter4seg.cai,bbtparameter4seg.gsi,bbtparameter4seg.rmr,\
                                    tbmsect.pkCe2Gl(bbt_parameter.fine),
                                    tbmsect.TunnelClosureAtShieldEnd*1000., tbmsect.rockBurst.Val,\
                                    tbmsect.frontStability.Ns, tbmsect.frontStability.lambdae,\
                                    tbmsect.penetrationRate*1000.,
                                    tbmsect.penetrationRateReduction*1000.,
                                    tbmsect.contactThrust, tbmsect.torque,
                                    tbmsect.frictionForce,
                                    tbmsect.requiredThrustForce,
                                    tbmsect.availableThrust,
                                    tbmsect.dailyAdvanceRate,
                                    bbt_parameter.profilo_id,
                                    bbt_parameter.geoitem_id,
                                    bbt_parameter.title,
                                    bbtparameter4seg.sti,
                                    tbmsect.InSituCondition.K0,
                                    tbmsect.t0,
                                    tbmsect.t1,
                                    tbmsect.t3,
                                    tbmsect.t4,
                                    tbmsect.t5,
                                    tbmsect.InSituCondition.SigmaV,
                                    tbmsect.Excavation.Radius,
                                    tbmsect.Rock.E,
                                    tbmsect.MohrCoulomb.psi,
                                    tbmsect.Rock.Ucs,
                                    tbmsect.InSituCondition.Gsi,
                                    tbmsect.HoekBrown.Mi,
                                    tbmsect.HoekBrown.D,
                                    tbmsect.HoekBrown.Mb,
                                    tbmsect.HoekBrown.S,
                                    tbmsect.HoekBrown.A,
                                    tbmsect.HoekBrown.Mr,
                                    tbmsect.HoekBrown.Sr,
                                    tbmsect.HoekBrown.Ar,
                                    tbmsect.UrPi_HB(0.),
                                    tbmsect.Rpl,
                                    tbmsect.Picr,
                                    tbmsect.LDP_Vlachopoulos_2009(0.),
                                    tbmsect.LDP_Vlachopoulos_2009(tbm.Slen),
                                    #aghensi@20160713 - aggiunta parametri al DB
                                    tbmsect.sigma_v_max_tail_skin, tbmsect.sigma_h_max_tail_skin,
                                    tbmsect.sigma_v_max_front_shield, tbmsect.sigma_h_max_front_shield,
                                    tbmsect.overcut_required, tbmsect.auxiliary_thrust_required,
                                    tbmsect.consolidation_required, tbmsect.sigma_h_max_lining,
                                    tbmsect.sigma_v_max_lining, bbtparameter4seg.anidrite,
                                    alnCurr.frictionCoeff
                                    ))

                    kpiTbm.updateKPI(alnCurr)
                    bbttbmkpis += kpiTbm.getBbtTbmKpis()
                    sys.stdout.flush()
        iter_end_time = ttime()
        main_logger.info("[%d]#### iteration %d - %d terminated in %d seconds (%d)" % (idWorker, iIterationNo, mainIterationNo, iter_end_time-iter_start_time, tbmSegmentCum))
        main_logger.debug("[%d]### Start inserting %d (%d) Parameters and %d (21x%d) KPIs" % (idWorker, len(bbt_evalparameters),iCheckEvalparameters,len(bbttbmkpis),iCheckBbttbmkpis))
        insert_eval4Iter(sDBPath,bbt_evalparameters,bbttbmkpis)
        insert_end_time = ttime()
        main_logger.info("[%d]]### Insert terminated in %d seconds" % (idWorker,insert_end_time-iter_end_time))
    now = datetime.datetime.now()
    strnow = now.strftime("%Y%m%d%H%M%S")
    end_time = ttime()
    main_logger.info("[%d]############################# Ends at %s (%s seconds)" % (idWorker,strnow, end_time-start_time))
    #with plock:
    #    print "[%d]############################# Ends at %s (%s seconds)" % (idWorker,strnow, end_time-start_time)


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

        load_tbm_table(sDBPath, tbms)
        main_logger.info("%d mp_producers, ognuno con %d iterazioni, totale iterazioni attese %d" % (mp_np , nIter, totIterations))
        sys.stdout.flush()
        if len(loopTbms) == 0:
            loopTbms = tbms
        deleteEval4Tbm(sDBPath,loopTbms)
        main_logger.info("Analisi per %d TBM" % len(loopTbms) )
        for tbk in loopTbms:
            main_logger.info( tbk )
        list_a = range(mp_np)
        start_time = ttime()
        job_args = [(i, nIter, sDBPath, loopTbms, sKey, mp_np) for i, item_a in enumerate(list_a)]

        # aghensi@20160603 singolo thread per debug - inizio
        workers = Pool(processes=mp_np)
        main_logger.info("Istanziati %d processi" % mp_np  )
        results = workers.map(mp_producer, job_args)
        workers.close()
        workers.join()

#        for ja in job_args:
#            mp_producer(ja)
        # aghensi@20160603 singolo thread per debug - fine

        end_time = ttime()
        main_logger.info("Tutti i processi terminati, tempo totale %d secondi (in minuti = %f , in ore = %f ore)" % (end_time-start_time,(end_time-start_time)/60.,(end_time-start_time)/3600.))
        main_logger.info("Processo principale terminato")
    else:
        print "main_loop_mp.py -n <number of iteration (positive integer)>\n\tCi sono %d processori disponibili" % mp_np
