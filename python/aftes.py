# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 17:31:11 2016

@author: aghensi
"""
import sqlite3
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import math

from TunnelSegment import probabilityAftes2012, impact
import bbtutils
from bbt_database import getDBConnection
from readparameters import get_xstrati, get_strata_labels, beautify_axis

SIGMA_DS = [.4, .5, 1., 1.5]


def calculate_pk_risks(impacts, probs, risks, sigmas, tot_samples):
    prev_pk_impacts = []
    prev_pk_probs = []
    prev_pk_risks = []
    for sigma_d in SIGMA_DS:
        sigma_95 = np.nanpercentile(sigmas, 95)
        impact_score = impact((sigma_95-sigma_d)/sigma_d)
        prob_score = probabilityAftes2012(float(len(sigmas))/float(tot_samples))
        risk_score = impact_score * prob_score
        prev_pk_impacts.append(impact_score)
        prev_pk_probs.append(prob_score)
        prev_pk_risks.append(risk_score)
    impacts.append(prev_pk_impacts)
    probs.append(prev_pk_probs)
    risks.append(prev_pk_risks)
    return impacts, probs, risks

def plot_aftes(tun, tbm, pks, hes, impacts, probs, risks, xstrati, outfolder):
    '''
    crea grafici per le aftes
    '''
    # le etichette sono fisse per ogni grafico dello stesso tun-tbm
    xlabels = get_strata_labels(xstrati, pks)
    csv_header = ['pk']
    outvalues = pks
    for i, sigmad in enumerate(SIGMA_DS):
        fig = plt.figure(figsize=(59.4/2.54, 2.5/2.54), dpi=300)
        plt.rcParams.update({'font.size': 2})
#        fig.suptitle("%s - %s" % (tun, tbm))

        ax1 = fig.add_subplot(111)
        beautify_axis(ax1)
        ax1.set_ylim(min(hes)-100, max(hes)+100)
#        ax1.set_xlabel('progressiva (m)')
#        ax1.set_ylabel('Altitudine (m)')
        ax1.yaxis.grid(False)
        ax1.xaxis.grid(True)
        ax1.get_yaxis().tick_left()
        ax1.plot(pks, hes, color='b', linewidth=0.5, alpha=0.6)

#        plt.xticks(xlabels, rotation='vertical')

        ax2 = ax1.twinx()
        beautify_axis(ax2)
#        ax2.set_ylabel("rischio relativo a sigma v > {:.1f} MPa".format(sigmad))

        ax2.set_xlim(xlabels[0], xlabels[-1])
        ylimInf = 0
        ylimSup = math.ceil(max(risks[:, i]))
        ax2.set_ylim(ylimInf, ylimSup)

        # tengo i tickmarks solo sull'altrimetria, per il resto ho grid
#        plt.tick_params(axis="both", which="both", bottom="off", top="off",
#                labelbottom="on", left="on", right="off", labelleft="on")

        ax2.get_yaxis().tick_right()
        yticks = np.arange(ylimInf, ylimSup+1)
#        plt.yticks(yticks)

        # definisco fasce aftes
        plt.axhspan(0, 2, color='green', alpha=0.3, edgecolor='none')
        plt.axhspan(2, 5, color='yellow', alpha=0.3, edgecolor='none')
        plt.axhspan(5, 10, color='darkorange', alpha=0.3, edgecolor='none')
        plt.axhspan(10, ylimSup, color='red', alpha=0.3, edgecolor='none')

        #ax1.bar(pks, risks[:, i], align='center')
        # visualizzo stacked bars per dare l'idea del rapporto tra probabilità e impatto
        plt_prob = risks[:, i] * probs[:, i]/(probs[:, i] + impacts[:, i])
        plt_impact = risks[:, i] - plt_prob
        ax2.bar(pks, plt_prob, align='center', color='indigo', edgecolor='indigo',
                label=u'probabilità')
        ax2.bar(pks, plt_impact, align='center', bottom=plt_prob, color='blue',
                edgecolor='blue', label='impatto')

#        leg = plt.legend()
#        leg.get_frame().set_linewidth(0.0)

        outfilename = "%s_%s_aftes_%s.png" % (tun.replace(" ", "_"), tbm, sigmad)
        bbtutils.outputFigure(outfolder, outfilename)
        outfilename = "%s_%s_aftes_%s.svg" % (tun.replace(" ", "_"), tbm, sigmad)
        bbtutils.outputFigure(outfolder, outfilename, format='svg')

        plt.close(fig)
        csv_header.append("impact_{}".format(sigmad))
        csv_header.append("prob_{}".format(sigmad))
        csv_header.append("risk_{}".format(sigmad))
        outvalues = np.column_stack((outvalues, impacts[:, i], probs[:, i], risks[:, i]))
    # esporto in csv i valori
    csvfname=os.path.join(outfolder,"%s_%s_aftes.csv" % (tun.replace(" ", "_"), tbm))
    with open(csvfname, 'wb') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(csv_header)
        writer.writerows(outvalues)

def risk_analisys_aftes():
    '''
    analisi del rischio secondo Aftes per superamento sigma v
    '''

    sql_query = """SELECT tunnelname as tun, tbmname as tbm, fine as pk, he, sigma_v_max_tail_skin, sigma_v_max_front_shield
    FROM BbtParameterEval
    WHERE tbmname IN ('CE_DS_HRK_6.82_112', 'CE_DS_RBS_6.73_12', 'GL_DS_HRK_10.60_112', 'GL_DS_RBS_10.56_12')
    ORDER BY tunnelname, tbmname, fine"""

    outfoldername = bbtutils.bbtConfig.get('Diagrams','folder')
    outfolder = os.path.join(os.path.abspath('..'), outfoldername)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)


    db_name = bbtutils.bbtConfig.get('Database', 'dbname')
    db_path = os.path.join(os.path.abspath('..'), bbtutils.bbtConfig.get('Database', 'dbfolder'),
                           db_name)
    if not os.path.isfile(db_path):
        print "Errore! File %s inesistente!" % db_path
        exit(1)
    conn = getDBConnection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # memorizzo le pk delle interfacce tra strati per il plot
    xstrati = get_xstrati(cur)
    cur.execute(sql_query)
    bbtresult = cur.fetchall()

    prev_pk = float("inf")
    prev_he = 0
    prev_tbm = 'XXX'
    prev_tun = 'XXX'
    sigmas = []
    pks = []
    impacts = []
    probs = []
    risks = []
    hes = []
    tot_samples = 0
    for bbtr in bbtresult:
        # Todo: controllo se sono su stesso tunnel, stessa TBM e stessa pk
        if bbtr['pk'] != prev_pk:
            # calcolo percentili pk precedente e salvo in array
            if prev_pk != float("inf"):
                impacts, probs, risks = calculate_pk_risks(impacts, probs, risks, sigmas, tot_samples)
                pks.append(prev_pk)
                hes.append(prev_he)
                #print "{} done".format(prev_pk)
            #resetto variabili della pk
            prev_pk = bbtr['pk']
            prev_he = bbtr['he']
            sigmas = []
            tot_samples = 0
        if bbtr['tbm'] != prev_tbm or bbtr['tun'] != prev_tun:
            if prev_tbm != 'XXX' and prev_tun != 'XXX':
                plot_aftes(prev_tun, prev_tbm, np.array(pks), np.array(hes), np.array(impacts),
                           np.array(probs), np.array(risks), xstrati, outfolder)
                print "{}, {} done".format(prev_tun, prev_tbm)
            # salvo/plotto gli array e resetto
            prev_tbm = bbtr['tbm']
            prev_tun = bbtr['tun']
            sigmas = []
            tot_samples = 0
            pks = []
            hes = []
            impacts = []
            probs = []
            risks = []
        # processo item corrente
        tot_samples += 1
        sigma = max(bbtr['sigma_v_max_tail_skin'], bbtr['sigma_v_max_front_shield'])
        if sigma > 0:
            sigmas.append(sigma)

    # Resta fuori l'ultimo gruppo di pk/tbm/tunnel processo...
    impacts, probs, risks = calculate_pk_risks(impacts, probs, risks, sigmas, tot_samples)
    pks.append(prev_pk)
    hes.append(prev_he)
    plot_aftes(prev_tun, prev_tbm, np.array(pks), np.array(hes), np.array(impacts),
               np.array(probs), np.array(risks), xstrati, outfolder)
    print "{}, {} done".format(prev_tun, prev_tbm)

#    print "totals=%d, evaluated=%d, sigma95=%f" % (totals, len(sigmas), sigma_95)
#    print "impact_score=%f, prob_score=%f, risk_score=%f" % (impact_score, prob_score, risk_score)

    conn.close()

if __name__ == "__main__":
    risk_analisys_aftes()
