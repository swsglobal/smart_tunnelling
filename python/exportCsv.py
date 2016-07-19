# -*- coding: utf-8 -*-
import sqlite3, os, csv
from tbmconfig import tbms
from bbtutils import *
from bbtnamedtuples import *
from readkpis import *
from bbt_database import getDBConnection
import numpy as np


def main():
    tunnelArray = ['CE', 'GL Nord']
    tbmfilter = ['CE_DS_HRK_6.82_00', 'CE_DS_HRK_6.82_112', 'CE_DS_RBS_6.73_00', 'CE_DS_RBS_6.73_12',
                 'GL_DS_HRK_10.60_00', 'GL_DS_HRK_10.60_112', 'GL_DS_RBS_10.56_00', 'GL_DS_RBS_10.56_12']
    ### Inserire qui i parametri da esportare
    paramsToExport = ['sigma_v_max_tail_skin', 'sigma_h_max_tail_skin', 'sigma_v_max_front_shield',
                      'sigma_h_max_front_shield', 'sigma_h_max_lining', 'sigma_v_max_lining']
    ### Inserire qui i parametri per cui calcolare i percentili
    paramsToPercentile = ['sigma_v_max_tail_skin', 'sigma_h_max_tail_skin', 'sigma_v_max_front_shield',
                          'sigma_h_max_front_shield', 'sigma_h_max_lining', 'sigma_v_max_lining']

    # mi metto nella directory corrente
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)

    ########## File vari: DB
    sDBName = bbtConfig.get('Database','dbname')
    sDBPath = os.path.join(os.path.abspath('..'), bbtConfig.get('Database','dbfolder'), sDBName)
    if not os.path.isfile(sDBPath):
        print "Errore! File %s inesistente!" % sDBPath
        exit(1)

    ########### Outupt Folder
    sDiagramsFolder = bbtConfig.get('Diagrams','folder')
    sDiagramsFolderPath = os.path.join(os.path.abspath('..'), sDiagramsFolder)
    if not os.path.exists(sDiagramsFolderPath):
        os.makedirs(sDiagramsFolderPath)
    # mi connetto al database
    conn = getDBConnection(sDBPath)
    # definisco il tipo di riga che vado a leggere, bbtparametereval_factory viene definita in bbtnamedtuples
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # quante iterazioni?
    sSql = "select max(BbtParameterEval.iteration_no) as max_iter from BbtParameterEval"
    cur.execute(sSql)
    bbtresult = cur.fetchone()
    M_Max = float(bbtresult[0]) + 1.0
    print "Numero massimo di iterazioni presenti %d" % M_Max

    for tun in tunnelArray:
        print "\r\n%s" % tun
        sSql = """SELECT bbtTbmKpi.tbmName, count(*) as cnt, BbtTbm.type, BbtTbm.manufacturer
                FROM bbtTbmKpi JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
                WHERE bbtTbmKpi.tunnelName = '{0}' AND bbtTbmKpi.tbmName in ('{1}')
                GROUP BY bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer
                ORDER BY bbtTbmKpi.tbmName""".format(tun, "', '".join(tbmfilter))
        cur.execute(sSql)
        bbtresults = cur.fetchall()
        print "Sono presenti %d diverse TBM" % len(bbtresults)
        for tb in bbtresults:
            tbmKey = tb[0]
            tbmCount = float(tb[1])
            # danzi.tn@20151118 calcolo iterazioni per la TBM corrente (non e' detto che siano tutte uguali)
            sSql = """SELECT MAX(BbtParameterEval.iteration_no) AS max_iter
                      FROM BbtParameterEval
                      WHERE BbtParameterEval.tbmName ='{}'""".format(tbmKey)
            cur.execute(sSql)
            bbtresult = cur.fetchone()
            M = float(bbtresult[0]) + 1.0
            if M_Max > M:
                print "Numero massimo di iterazioni per %s sono %d" % (tbmKey, M)
            sSql = """SELECT *, t1+t3+t4+t5 as tsum, 1 as adv
                      FROM BBtParameterEval
                      WHERE tunnelNAme = '"""+tun+"""'
                          AND tbmNAme='"""+tbmKey+"""'
                      order by iteration_no, fine"""
            cur.execute(sSql)
            bbtresults = cur.fetchall()
            # recupero tutti i parametri e li metto in una lista
            N = len(bbtresults)/M # No di segmenti
            parm2show = {}
            percCsvHeader = ['fine', 'he', 'hp']
            outCsvHeader = ['fine', 'he', 'hp']
            for param in paramsToExport:
                parm2show[param] = np.zeros(shape=(N,M), dtype=float)
                outCsvHeader.append(param)
                percCsvHeader.append("{}_50perc".format(param))
                percCsvHeader.append("{}_5perc".format(param))
                percCsvHeader.append("{}_95perc".format(param))
            outValues = []
            outPercentile = []
            i = 0
            pj = 0
            for bbt_parametereval in bbtresults:
                j = int(bbt_parametereval['iteration_no'])
                if pj != j:
                    pj = j
                    i = 0
                if j == 0:
                    outPercentile.append([float(bbt_parametereval['fine']),
                                          float(bbt_parametereval['he']),
                                          float(bbt_parametereval['hp'])])
                cur_line= [int(bbt_parametereval['iteration_no']),
                           float(bbt_parametereval['fine']),
                           float(bbt_parametereval['he']),
                           float(bbt_parametereval['hp'])]
                for param in paramsToExport:
                    pVal = float(bbt_parametereval[param] or 0)
                    cur_line.append(pVal)
                    parm2show[param][i][j] = pVal
                outValues.append(cur_line)
                i += 1

            for i in range(int(N)):
                for param in paramsToExport:
                    perc = list(np.nanpercentile(parm2show[param][i,:],(5,50,95)))
                    outPercentile[i].append(perc[1])
                    outPercentile[i].append(perc[0])
                    outPercentile[i].append(perc[2])
            if N==0:
                print "\tPer TBM %s non ci sono dati in %s" % (tbmKey, tun)
            else:
                # esporto in csv i valori di confronto
                csvfname=os.path.join(sDiagramsFolderPath,"%s_%s_combined_parms.csv" % (tun.replace(" ", "_"), tbmKey))
                with open(csvfname, 'wb') as f:
                    writer = csv.writer(f,delimiter=";")
                    writer.writerow(outCsvHeader)
                    writer.writerows(outValues)
                csvfname=os.path.join(sDiagramsFolderPath,"%s_%s_combined_parms_percentile.csv" % (tun.replace(" ", "_"), tbmKey))
                with open(csvfname, 'wb') as f:
                    writer = csv.writer(f,delimiter=";")
                    writer.writerow(percCsvHeader)
                    writer.writerows(outPercentile)

if __name__ == "__main__":
   #main(sys.argv[1:])
    main()
