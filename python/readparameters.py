# -*- coding: utf-8 -*-
import sqlite3, os, csv
import sys, getopt
from tbmconfig import tbms
from bbtutils import *
from bbtnamedtuples import *
import matplotlib.mlab as mlab
from readkpis import *
from collections import defaultdict
from bbt_database import load_tbm_table, getDBConnection
from matplotlib.ticker import FuncFormatter

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns


#def get_stress(cur):
#    for param in ("lining","front_shield","tail_skin"):
#        strSql="""SELECT a.*
#            FROM bbtparametereval a
#            INNER JOIN (
#                SELECT tunnelname, tbmname, min(sigma_v_max_{0}) min_par1, max(sigma_v_max_{0}) max_par1, min(sigma_h_max_{0}) min_par2, max(sigma_h_max_{0}) max_par2
#                FROM bbtparametereval
#                where tunnelname != 'XXX' and sigma_v_max_{0} > 0 and sigma_h_max_{0} > 0
#                GROUP BY tunnelname, tbmname
#            ) b
#            ON a.tunnelname = b.tunnelname AND a.tbmname = b.tbmname AND (
#            a.sigma_v_max_{0} = b.min_par1 OR a.sigma_v_max_{0} = b.max_par1
#            OR a.and sigma_h_max_{0} = b.min_par2 OR a.and sigma_h_max_{0} = b.max_par2)
#            order by a.tunnelname, a.tbmname, a.sigma_v_max_{0}, a.and sigma_h_max_{0}""".format(param)
#        cur.execute(strSql)
#        bbtresults = cur.fetchall()
#        for bbt_parametereval in bbtresults:

def get_xstrati(cur):
    sSql = """select distinct inizio from bbtgeoitem union select max(fine)
            from bbtgeoitem order by inizio"""
    cur.execute(sSql)
    bbtresults = cur.fetchall()
    return [record[0] for record in bbtresults]

def get_strata_labels(xstrati, xcampioni):
    xlabels = []
    for i, tick in enumerate(xstrati):
        if tick < xcampioni[0] and xstrati[i+1] > xcampioni[0]:
            xlabels.append(tick)
        elif xcampioni[0] <= tick <= xcampioni[-1]:
            xlabels.append(tick)
        elif tick > xcampioni[-1] and xstrati[i-1] < xcampioni[-1]:
            xlabels.append(tick)
    return xlabels

def beautify_axis(ax):
    '''
    impostazioni di base per un bel grafico
    '''
    ax.set_axis_bgcolor('white')
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.4)
    ax.get_xaxis().tick_bottom()


# qui vedi come leggere i parametri dal Database bbt_mules_2-3.db
# danzi.tn@20151114 completamento lettura nuovi parametri e TBM
# danzi.tn@20151114 integrazione KPI in readparameters
# danzi.tn@20151117 plot percentile
# danzi.tn@20151117 plot aggregato per tipologia TBM
# danzi.tn@20151118 filtro per tipologia TBM
# danzi.tn@20151124 generazione delle distribuzioni per pk
# danzi.tn@20151124 formattazione in percentuale per istogrammi
# danzi.tn@20151124 replaceTBMName
# aghensi@20160714 calcolo 5°, 50° e 95° percentile effettivo sui campioni
def main(argv):
    sParm = "p,parameter in \n"
    sParameterToShow = ""
    segmentsToShow = []
    sTbmCode = ""
    sTypeToGroup = ""
    bPrintHist = False
    bShowProfile = False
    bShowRadar = False
    bShowKPI = False
    bShowAllKpi = False
    bShowDetailKPI = False
    bGroupTypes = False
    bShowAdvance = False
    probability = False
    greaterThan = False
    for k in parmDict:
        sParm += "\t%s - %s\r\n" % (k,parmDict[k][0])
    sParm += "\n t,tbmcode  in \n"
    for k in tbms:
        sParm += "\t%s - Produttore %s di tipo %s per tunnel %s\r\n" % (k,tbms[k].manifacturer, tbms[k].type, tbms[k].alignmentCode)
    sParm += "\n\t-r => generazione diagramma Radar per tutte le TBM\n"
    sParm += "\n\t-k => generazione diagrammi KPI G, P e V\n"
    sParm += "\n\t-a => generazione diagrammi KPI G + P + V\n"
    sParm += "\n\t-d => generazione diagrammi KPI di Dettaglio\n"
    sParm += "\n\t-i => generazione delle distribuzioni per ogni tipo di KPI selezionato\n"
    sParm += "\n\t-c => raggruppamento per tipologia di TBM\n"
    sParm += "\n\t-m => per tipologia di TBM indicata viene eseguito raggruppamento per Produttore\n"
    sParm += "\n\t-s => per segmento progressivo indicata con km+m\n"
    try:
        opts, args = getopt.getopt(argv,"hp:t:rkadicm:s:o:g:",["parameter=","tbmcode=","radar","kpi","allkpi","detailkpi","histograms","compact_types","bytype","segment","probability","greater_than"])
    except getopt.GetoptError:
        print "readparameters.py -p <parameter> [-t <tbmcode>] [-rkai]\r\n where\r\n %s" % sParm
        sys.exit(2)
    if len(opts) < 1:
        print "readparameters.py -p <parameter> [-t <tbmcode>] [-rkai]\r\n where\r\n %s" % sParm
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "readparameters.py -p <parameter> [-t <tbmcode>] [-rkai]\r\n where\r\n %s" % sParm
            sys.exit()
        elif opt in ("-p", "--iparameter"):
            sParameterToShow = arg
            bShowProfile = True
            if sParameterToShow =='adv':
                bShowAdvance = True
        elif opt in ("-s", "--segment"):
            sSegmentToShow = arg
            splitted = sSegmentToShow.split(",")
            for s in splitted:
                sf= s.split("+")
                fSegmentToShow = float(sf[0])*1000+float(sf[1])
                segmentsToShow.append((str(fSegmentToShow),"+".join(sf)))
        elif opt in ("-t", "--tbmcode"):
            sTbmCode = arg
        elif opt in ("-r", "--radar"):
            bShowRadar = True
        elif opt in ("-k", "--kpi"):
            bShowKPI = True
        elif opt  in ("-a", "--allkpi"):
            bShowAllKpi = True
        elif opt in ("-d", "--detailkpi"):
            bShowDetailKPI = True
        elif opt in ("-i", "--histograms"):
            bPrintHist = True
        elif opt in ("-c", "--compact_types"):
            bGroupTypes = True
        elif opt in ("-m", "--bytype"):
            sTypeToGroup = arg
            #bGroupTypes = True
        elif opt in ("-o", "--probability"):
            probability = True
            sParameterToShow = arg
        elif opt in ("-g", "--greater_than"):
            greaterThan = True
            threshold = float(arg)


    if len(sTypeToGroup) >0 and sTypeToGroup not in ('DS','S','O'):
        print "Wrong TBM Type -m=%s!\nreadparameters.py -p <parameter> [-t <tbmcode>] [-rkai]\r\n where\r\n %s" % (sTypeToGroup,sParm)
        sys.exit(2)
    if len(sParameterToShow) >0 and sParameterToShow not in parmDict:
        print "Wrong parameter -p=%s!\nreadparameters.py -p <parameter> [-t <tbmcode>] [-rkai]\r\n where\r\n %s" % (sParameterToShow,sParm)
        sys.exit(2)
    if len(sTbmCode) >0 and sTbmCode not in tbms:
        print "Wrong TBM Code -t=%s!\nreadparameters.py -p <parameter> -t <tbmcode> [-rkai]\r\n where\r\n %s" % (sTbmCode,sParm)
        sys.exit(2)
    # mi metto nella directory corrente
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)

    ########## File vari: DB
    sDBName = bbtConfig.get('Database','dbname')
    sDBPath = os.path.join(os.path.abspath('..'), bbtConfig.get('Database','dbfolder'), sDBName)
    if not os.path.isfile(sDBPath):
        print "Errore! File %s inesistente!" % sDBPath
        exit(1)

    #load_tbm_table(sDBPath, tbms)
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
    # Legge tutti i Tunnell
    sSql = """SELECT distinct
            bbtTbmKpi.tunnelName
            FROM
            bbtTbmKpi
            ORDER BY bbtTbmKpi.tunnelName"""
    cur.execute(sSql)
    bbtresults = cur.fetchall()
    print "Sono presenti %d diverse Gallerie" % len(bbtresults)
    tunnelArray = []
    for bbtr in bbtresults:
        tunnelArray.append(bbtr[0])
#    tunnelArray = ['CE', 'GL Nord']
    # Legge tutte le TBM solo per associare i colori in maniera univoca
    sSql = """SELECT bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer, count(*) as cnt
            FROM
            bbtTbmKpi
			JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
			GROUP BY bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer
            ORDER BY bbtTbmKpi.tbmName"""
    if bGroupTypes:
        sSql = """SELECT BbtTbm.type, count(*) as cnt
                FROM
                bbtTbmKpi
    			JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
    			GROUP BY BbtTbm.type
                ORDER BY BbtTbm.type"""
    cur.execute(sSql)
    bbtresults = cur.fetchall()
    # HACK
#    tbmfilter = ['CE_DS_HRK_6.82_00', 'CE_DS_HRK_6.82_112', 'CE_DS_RBS_6.73_00', 'CE_DS_RBS_6.73_12',
#                 'GL_DS_HRK_10.60_00', 'GL_DS_HRK_10.60_112', 'GL_DS_RBS_10.56_00', 'GL_DS_RBS_10.56_12']
    # associare un colore diverso ad ogni TBM
    tbmColors = {}
    for bbtr in bbtresults:
        #tbmColors[bbtr[0]] = main_colors.pop(0)
        tbmColors[bbtr] = main_colors.pop(0)
    bShowlTunnel = False

    xstrati = get_xstrati(cur)
    #sns.set(style="white", context="talk")

    for tun in tunnelArray:
        allTbmData = []
        print "\r\n%s" % tun
#        sSql = """SELECT bbtTbmKpi.tbmName, count(*) as cnt, BbtTbm.type, BbtTbm.manufacturer
#                FROM bbtTbmKpi JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
#                WHERE bbtTbmKpi.tunnelName = '{0}' AND bbtTbmKpi.tbmName in ('{1}')
#                GROUP BY bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer
#                ORDER BY bbtTbmKpi.tbmName""".format(tun, "', '".join(tbmfilter))

        sSql = """SELECT bbtTbmKpi.tbmName, count(*) as cnt, BbtTbm.type, BbtTbm.manufacturer
                FROM
                bbtTbmKpi
                JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
                WHERE bbtTbmKpi.tunnelName = '"""+tun+"""'
                GROUP BY bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer
                ORDER BY bbtTbmKpi.tbmName"""
        # Filtro sulla eventuale TBM passata come parametro
        if len(sTbmCode) > 0:
            sSql = """SELECT bbtTbmKpi.tbmName, count(*) as cnt, BbtTbm.type, BbtTbm.manufacturer
                    FROM
                    bbtTbmKpi
        			JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
                    WHERE bbtTbmKpi.tunnelName = '"""+tun+"""' AND BbtTbm.name = '"""+sTbmCode+"""'
        			GROUP BY bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer
                    ORDER BY bbtTbmKpi.tbmName"""
        # Filtro sulla eventuale Tipologia passata come parametro
        elif len(sTypeToGroup) > 0:
            sSql = """SELECT bbtTbmKpi.tbmName, count(*) as cnt, BbtTbm.type, BbtTbm.manufacturer
                    FROM
                    bbtTbmKpi
        			JOIN BbtTbm on BbtTbm.name = bbtTbmKpi.tbmName
                    WHERE bbtTbmKpi.tunnelName = '"""+tun+"""' AND BbtTbm.type = '"""+sTypeToGroup+"""'
        			GROUP BY bbtTbmKpi.tbmName, BbtTbm.type, BbtTbm.manufacturer
                    ORDER BY bbtTbmKpi.tbmName"""
        # Raggruppamento per Tipo TBM
        elif bGroupTypes:
            sSql = """SELECT BbtTbm.type, count(*) as cnt_tbmtype
                    FROM
                    BbtTbm
					WHERE
					BbtTbm.name IN (
                    SELECT DISTINCT BbtTbmKpi.tbmName
					FROM bbtTbmKpi
                    WHERE
                    bbtTbmKpi.tunnelName = '"""+tun+"""')
        			GROUP BY BbtTbm.type
                    ORDER BY BbtTbm.type"""
        cur.execute(sSql)
        bbtresults = cur.fetchall()
        print "Sono presenti %d diverse TBM" % len(bbtresults)
        for tb in bbtresults:
            tbmKey = tb[0]
            tbmCount = float(tb[1])
            if len(segmentsToShow) > 0:
                for sCriteria, sProg in segmentsToShow:
                    # danzi.tn@20151123 calcolo iterazioni per la TBM corrente (non e' detto che siano tutte uguali)
                    sSql = """SELECT BBtParameterEval.*, BBtParameterEval.t1 +BBtParameterEval.t3
                            +BBtParameterEval.t4 +BBtParameterEval.t5 AS tsum, 1 AS adv
                            FROM BbtParameter, BBtParameterEval
                            WHERE BbtParameter.profilo_id = BBtParameterEval.profilo_id
                                AND BbtParameter.fine = """+sCriteria+"""
                                AND BBtParameterEval.tunnelNAme = '"""+tun+"""'
                                AND tbmNAme='"""+tbmKey+""""'"""
                    if bGroupTypes:
                        sSql = """SELECT BBtParameterEval.*, BBtParameterEval.t1 +BBtParameterEval.t3
                                +BBtParameterEval.t4 +BBtParameterEval.t5 AS tsum, 1 AS adv
                                FROM BbtParameter, BBtParameterEval, BbtTbm
                                WHERE BbtParameter.profilo_id = BBtParameterEval.profilo_id
                                  AND BbtParameter.fine = """+sCriteria+"""
                                  AND  BbtTbm.name = BBtParameterEval.tbmName
                                  AND BbtParameter.profilo_id = BBtParameterEval.profilo_id
                                  AND BBtParameterEval.tunnelNAme = '"""+tun+"""'
                                  AND BbtTbm.type='"""+tbmKey+"""'"""
                    cur.execute(sSql)
                    bbtresults = cur.fetchall()
                    pValues = []
                    for bbt_parametereval in bbtresults:
                        pVal = bbt_parametereval[sParameterToShow]
                        if pVal == None:
                            pVal = 0
                        pVal = float(pVal)
                        pValues.append(pVal)
                    if len(pValues) > 0:
                        num_bins = 50
                        fig = plt.figure(figsize=(32, 20), dpi=100)
                        ax1 = fig.add_subplot(111)
                        fig.suptitle("%s - %s" % (tun,replaceTBMName(tbmKey)))
                        weights = np.ones_like(pValues)/float(len(pValues))
                        n, bins, patches = ax1.hist(pValues,num_bins , normed=1, histtype ='stepfilled', weights=weights , color=tbmColors[tbmKey], alpha=0.3)
                        tbmMean = np.mean(pValues)
                        tbmSigma = np.std(pValues)
                        y = mlab.normpdf(bins, tbmMean, tbmSigma)
                        ax1.plot(bins, y, '--', color=tbmColors[tbmKey])
                        ax1.set_xlabel("%s (%f)" % (parmDict[sParameterToShow][0],tbmMean), color='r')
                        ax1.set_ylabel("Probabilita'(%)")
                        ax1.axvline(tbmMean, color='r', linewidth=2)
                        ax1.yaxis.grid(True)
#                        sFileNAme = "bbt_%s_%s_%s_%s_hist.svg" % ( tun.replace (" ", "_"), replaceTBMName(tbmKey),sParameterToShow,sProg)
#                        outputFigure(sDiagramsFolderPath, sFileNAme, format="svg")
#                        print "Output su %s disponibile" % sFileNAme
                        sFileNAme = "%s_%s_%s_%s_hist.png" % (tun.replace(" ", "_"), tbmKey, sParameterToShow, sProg)
                        outputFigure(sDiagramsFolderPath, sFileNAme)
                        print "Output su %s disponibile" % sFileNAme
                        plt.close(fig)
            elif bShowProfile:
                # danzi.tn@20151118 calcolo iterazioni per la TBM corrente (non e' detto che siano tutte uguali)
                sSql = """SELECT MAX(BbtParameterEval.iteration_no) AS max_iter
                          FROM BbtParameterEval
                          WHERE BbtParameterEval.tbmName ='"""+ tbmKey + """'"""
                if bGroupTypes:
                    sSql = """select max(BbtParameterEval.iteration_no) as max_iter
                              from BbtParameterEval
                              JOIN BbtTbm on BbtTbm.name = BbtParameterEval.tbmName
                              WHERE BbtTbm.type ='"""+ tbmKey +""""'"""
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
                if bGroupTypes:
                    sSql = """SELECT *, BBtParameterEval.t1 +BBtParameterEval.t3
                              +BBtParameterEval.t4 +BBtParameterEval.t5 as tsum, 1 as adv
                              FROM BBtParameterEval
                              JOIN BbtTbm on BbtTbm.name = BBtParameterEval.tbmName
                              WHERE BBtParameterEval.tunnelNAme = '"""+tun+"""'
                                  AND BbtTbm.type='"""+tbmKey+"""'
                              order by BBtParameterEval.iteration_no, BBtParameterEval.fine, BbtTbm.type"""
                cur.execute(sSql)
                bbtresults = cur.fetchall()
                # recupero tutti i parametri e li metto in una lista
                N = len(bbtresults)/M # No di segmenti
                pi = np.zeros(shape=(N,))
                he = np.zeros(shape=(N,))
                hp = np.zeros(shape=(N,))
                #ti = np.zeros(shape=(N,), dtype=float)
                parm2show = np.zeros(shape=(N,M))
                mean2Show = np.zeros(shape=(N,3))
                tti = np.zeros(shape=(N,M))
                xti = np.zeros(shape=(N,M))
                percOverThreshold = np.zeros(shape=(N,))
                i = 0
                pj = 0
                prev = 0.0
                outValues =[]
#                if tun not in ('GL Sud'):
#                    bbtresults.reverse()
                maxval = 0
                for bbt_parametereval in bbtresults:
                    j = int(bbt_parametereval['iteration_no'])
                    if pj != j:
                        pj = j
                        prev = i = 0
                    pi[i] = bbt_parametereval['fine']
                    xti[i][j] = float(bbt_parametereval['dailyAdvanceRate'])
                    tti[i][j] = prev + 10.0/xti[i][j]
                    prev = tti[i][j]
                    he[i] = bbt_parametereval['he']
                    hp[i] = bbt_parametereval['hp']
                    pVal = bbt_parametereval[sParameterToShow]
                    if pVal == None:
                        pVal = 0
                    pVal = float(pVal)
                    if bShowAdvance:
                        pVal = tti[i][j]
                        if bGroupTypes:
                            pVal = pVal/tbmCount
                    #aghensi@20160714 - memorizzo solo i percentili
#                    if j == 0:
#                        outValues.append([float(bbt_parametereval['fine']),
#                                          float(bbt_parametereval['he']),
#                                          float(bbt_parametereval['hp'])])
                    if not greaterThan:
                        outValues.append([int(bbt_parametereval['iteration_no']),
                                         float(bbt_parametereval['fine']),
                                         float(bbt_parametereval['he']),
                                         float(bbt_parametereval['hp']),pVal])
                        maxval = max(maxval, pVal)
                    parm2show[i][j] = pVal
                    i += 1
                for i in range(int(N)):
                    if greaterThan:
                        # percentuale superamento di un certo valore
                        percOverThreshold[i] = (float(np.sum(parm2show[i, :] > threshold))/float(M))
                        maxval = max(maxval, percOverThreshold[i])
                    else:
                        # aghensi@20160714 calcolo 5°, 50° e 95° percentile effettivo sui campioni
                        # TODO: si possono calcolare i percentili di tutto param2show usando axis=...
                        mean2Show[i] = list(np.nanpercentile(parm2show[i,:],(5,50,95)))
                        outValues[i].append(mean2Show[i][1])
                        outValues[i].append(mean2Show[i][0])
                        outValues[i].append(mean2Show[i][2])
                        #pki_mean = np.nanmean(parm2show[i,:])
                        #pki_std = np.nanstd(parm2show[i,:])
                        #mean2Show[i][0] = pki_mean - 2*pki_std
                        #mean2Show[i][1] = pki_mean
                        #mean2Show[i][2] = pki_mean + 2*pki_std

                if N==0:
                    print "\tPer TBM %s non ci sono dati in %s" % (tbmKey, tun)
                elif greaterThan and maxval == 0:
                    print "\tPer TBM %s non ci sono valori in %s oltre %f" % (tbmKey, tun, threshold)
                else:
                    if greaterThan:
                        ylimInf = 0
                        ylimSup = min(maxval * 1.01, 1)
                    else:
                        ylimInf = parmDict[sParameterToShow][2]
                        ylimSup = max(maxval * 1.01, parmDict[sParameterToShow][3])

                    fig = plt.figure(figsize=(60, 10), dpi=100)

                    plt.rcParams.update({'font.size': 18})
                    ax1 = fig.add_subplot(111)
                    beautify_axis(ax1)
                    fig.suptitle("%s - %s" % (tun,tbmKey))
                    ax1.get_yaxis().tick_left()
                    ax1.set_ylim(min(he)-100, max(he)+100)
                    ax1.plot(pi, he,'b-', linewidth=0.5, alpha=0.6)
                    if bShowlTunnel:
                        ax1.plot(pi, hp,'k-', linewidth=0.5, alpha=0.6)
                    ax1.set_xlabel('Station (m)')
                    ax1.set_ylabel('Elevation (m)', color='b')
                    ax1.grid(False)
                    #########
                    ax2 = ax1.twinx()
                    #ax2.yaxis.grid(True)
                    ax2.spines["top"].set_visible(False)
                    ax2.spines["bottom"].set_visible(greaterThan)
                    ax2.spines["right"].set_visible(False)
                    ax2.spines["left"].set_visible(False)
                    ax2.get_xaxis().tick_bottom()
                    ax2.get_yaxis().tick_right()
                    ax2.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.4)

                    ax2.set_ylim(ylimInf, ylimSup)
                    if greaterThan:
                        ax2.bar(pi, percOverThreshold, align='center', color="lightgray", edgecolor="lightgray")
                        ax2.set_ylabel("%s (probability over %f)" % (parmDict[sParameterToShow][0], threshold))
                    else:
                        ax2.plot(pi, parm2show, 'r.', markersize=3.0, alpha=0.5)
                        ax2.plot(pi, mean2Show[:,0], 'm-', linewidth=1, alpha=0.4)
                        ax2.plot(pi, mean2Show[:,1], 'g-', linewidth=2, alpha=0.6)
                        ax2.plot(pi, mean2Show[:,2], 'c-', linewidth=1, alpha=0.4)
                        ax2.set_ylabel("%s (%s)" % (parmDict[sParameterToShow][0],parmDict[sParameterToShow][1]), color='r')

                    for tl in ax1.get_yticklabels():
                        tl.set_color('b')
                    for tl in ax2.get_yticklabels():
                        tl.set_color('r')

                    xlabels = get_strata_labels(xstrati, pi)
                    ax1.set_xlim(xlabels[0],xlabels[-1])
                    plt.xticks(xlabels, rotation='vertical')
                    yticks = np.around(np.arange(ylimInf, ylimSup, (ylimSup-ylimInf)/10.),2)
                    plt.yticks(yticks)


                        # visualizzo valori asse ma senza tacche
    #                    plt.tick_params(axis="both", which="both", bottom="off", top="off",
    #                                    labelbottom="on", left="off", right="off", labelleft="on")
                    plt.tight_layout(h_pad=3)
                    if greaterThan:
                        outfilename = "%s_%s_%s-%.2f.png" % (tun.replace(" ", "_"), tbmKey, sParameterToShow, threshold)
                    else:
                        outfilename = "%s_%s_%s.png" % (tun.replace(" ", "_"), tbmKey, sParameterToShow)
#                    outputFigure(sDiagramsFolderPath,"%s_%s_%s.svg" % (tun.replace(" ", "_"), tbmKey, sParameterToShow), "svg")
                    outputFigure(sDiagramsFolderPath,outfilename)
                    plt.close(fig)
                    if not greaterThan:
                        # esporto in csv i valori di confronto
                        csvfname=os.path.join(sDiagramsFolderPath,"%s_%s_%s.csv" % ( tun.replace(" ", "_"), tbmKey, sParameterToShow))
                        with open(csvfname, 'wb') as f:
                            writer = csv.writer(f,delimiter=";")
                            writer.writerow(('iterazione','fine','he','hp',sParameterToShow, '50perc', '5perc', '95perc'))
                            writer.writerows(outValues)
            # aghensi@20160715 - aggiunto istogramma probabilità ristretta su pk in cui è maggiore di 0
            elif probability:
                sSql = """SELECT * FROM(
                    SELECT fine, CAST(sum({0}) AS REAL)/cast(count({0}) as real) as probability
                    FROM bbtparametereval
                    WHERE tunnelname = '{1}' AND tbmname = '{2}'
                    GROUP BY fine
                    ORDER BY fine
                    ) WHERE probability > {3}""".format(sParameterToShow, tun, tbmKey, 0.0)
                cur.execute(sSql)
                bbtresults = cur.fetchall()
                N = len(bbtresults)
                if N > 0:
#                    if tun not in ('GL Sud'):
#                        bbtresults.reverse()
                    # recupero tutti i parametri e li metto in una lista
                    xvalues = np.zeros(shape=(N), dtype=float)
                    parm2show = np.zeros(shape=(N), dtype=float)
                    outValues = []
                    ymax = 0
                    for i, bbt_parametereval in enumerate(bbtresults):
                        xvalues[i] = bbt_parametereval['fine']
                        parm2show[i] = float(bbt_parametereval['probability'])*100
                        outValues.append([bbt_parametereval['fine'], bbt_parametereval['probability']])
                        ymax = max(ymax, parm2show[i])

                    xlabels = get_strata_labels(xstrati, xvalues)

                    # creo grafico
                    fig = plt.figure(figsize=(60, 10), dpi=100)
                    plt.rcParams.update({'font.size': 18})
                    ax1 = fig.add_subplot(111)
                    ax1.set_ylim(0,ymax*1.1)
                    ax1.set_xlim(xlabels[0],xlabels[-1])
                    # titolo ed etichette
                    fig.suptitle("%s - %s" % (tun,tbmKey))
                    ax1.set_xlabel('Station (m)')
                    ax1.set_ylabel("%s (probability)" % (parmDict[sParameterToShow][0]))


                    plt.xticks(xlabels, rotation='vertical')
                    yticks = np.around(np.arange(0, ymax+1, ymax/10),1)
                    plt.yticks(yticks, [str(x) + "%" for x in yticks])
                    ax1.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.4)

                    # tolgo bordi
                    ax1.spines["top"].set_visible(False)
                    ax1.spines["bottom"].set_visible(True)
                    ax1.spines["right"].set_visible(False)
                    ax1.spines["left"].set_visible(False)
                    # visualizzo valori asse ma senza tacche
                    ax1.get_xaxis().tick_bottom()
                    ax1.get_yaxis().tick_left()
                    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                                    labelbottom="on", left="off", right="off", labelleft="on")

                    # plotto grafico
                    ax1.bar(xvalues, parm2show, align='center', color="lightgray", edgecolor="lightgray")

                    plt.tight_layout(h_pad=3)
                    ##########

                    #outputFigure(sDiagramsFolderPath,"%s_%s_%s.svg" % (tun.replace(" ", "_"), tbmKey, sParameterToShow), "svg")
                    outputFigure(sDiagramsFolderPath,"%s_%s_%s-prob.png" % (tun.replace(" ", "_"), tbmKey, sParameterToShow))
                    plt.close(fig)
                    # esporto in csv i valori di confronto
                    csvfname=os.path.join(sDiagramsFolderPath,"%s_%s_%s-prob.csv" % ( tun.replace(" ", "_"), tbmKey, sParameterToShow))
                    with open(csvfname, 'wb') as f:
                        writer = csv.writer(f,delimiter=";")
                        writer.writerow(('fine','probability' ))
                        writer.writerows(outValues)

            if bShowKPI:
                print "%s %s" % (tun, tbmKey)
                allTbmData += plotKPIS(cur,sDiagramsFolderPath,tun,tbmKey,tbmColors,bGroupTypes, sTypeToGroup, bPrintHist)
            if bShowAllKpi:
                allTbmData += plotTotalsKPIS(cur,sDiagramsFolderPath,tun,tbmKey,tbmColors,bGroupTypes, sTypeToGroup, bPrintHist)
            if bShowDetailKPI:
                allTbmData += plotDetailKPIS(cur,sDiagramsFolderPath,tun,tbmKey,tbmColors,bGroupTypes, sTypeToGroup, bPrintHist)
        if len(allTbmData) > 0:
            dictKPI = defaultdict(list)
            dictDescr = {}
            listToExport = []
            for item in allTbmData:
                key = item[0]
                dictDescr[key] = item[-1]
                dictKPI[key].append( item[1:-1] )
                listToExport.append(item[:4])
            # esposrto in csv i valori di confronto
#            csvfname=os.path.join(sDiagramsFolderPath,"%s_all_data.csv" %  tun.replace (" ", "_") )
#            with open(csvfname, 'wb') as f:
#                writer = csv.writer(f,delimiter=";")
#                writer.writerow(('kpi','tbm','medie','sigma'  ))
#                writer.writerows(listToExport)
            for key in dictKPI:
                keyDescr = dictDescr[key]
                allTbmData = dictKPI[key]
                fig = plt.figure(figsize=(22, 10), dpi=75)
                ax = fig.add_subplot(111)
                ax.yaxis.grid(True)
                tbmNames = map(lambda y:y[0],allTbmData)
                tbmMeans = map(lambda y:y[1],allTbmData)
                tbmSigmas = map(lambda y:y[2],allTbmData)
                tbmDatas = map(lambda y:y[3],allTbmData)
                ax.set_xticks([y+1 for y in range(len(tbmDatas)) ])
                ax.set_xlabel('TBMs')
                ax.set_ylabel("%s - %s" % (key,keyDescr))
                ax.set_title("%s, comparazione %s " % (tun,keyDescr))
                xind = np.arange(len(tbmDatas))
                plotColors =[]
                tbmHiddenNames = []
                for tk in tbmNames:
                    plotColors.append(tbmColors[tk])
                    tbmHiddenNames.append(tk)
                if len(tbmDatas[0]) < 3:
                    #Stampa per quando len(tbmDatas) < 3
                    width = 0.35
                    plt.bar(xind, tbmMeans, width,color=plotColors, yerr=tbmSigmas)
                    plt.xticks(xind + width/2., tbmHiddenNames)
                else:
                    try:
                        violin_parts = violinplot(tbmDatas,showmeans = True, points=50)
                        idx = 0
                        indMin = np.argmin(tbmMeans)
                        for vp in violin_parts['bodies']:
                            vp.set_facecolor(tbmColors[tbmNames[idx]])
                            vp.set_edgecolor(tbmColors[tbmNames[idx]])
                            vp.set_alpha(0.4)
                            if idx==indMin:
                                vp.set_edgecolor('y')
                                vp.set_linewidth(2)
                            idx +=1

                        plt.setp(ax, xticks=[y+1 for y in range(len(tbmDatas))],xticklabels=tbmHiddenNames)
                    except Exception as e:
                        print "Impossibile generare violin di %s per: %s" % ( key ,e)
                        width = 0.35
                        plt.bar(xind, tbmMeans, width,color=plotColors, yerr=tbmSigmas)
                        plt.xticks(xind + width/2., tbmHiddenNames)

                #outputFigure(sDiagramsFolderPath,"%s_%s_comp.svg" % (tun.replace (" ", "_") , key), format="svg")
                outputFigure(sDiagramsFolderPath,"%s_%s_comp.png" % (tun.replace (" ", "_") , key))
                plt.close(fig)


    if bShowRadar:
        plotRadarKPIS(cur,tunnelArray,sDiagramsFolderPath,tbmColors,bGroupTypes, sTypeToGroup)
    conn.close()

if __name__ == "__main__":
   main(sys.argv[1:])
