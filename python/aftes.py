# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 17:31:11 2016

@author: aghensi
"""
import sqlite3, os, csv
import numpy as np
from TunnelSegment import probabilityAftes2012, impact
from bbtutils import *
from bbt_database import load_tbm_table, getDBConnection

def RiskAnalisysAftes():
    '''

    '''
    sDBName = bbtConfig.get('Database','dbname')
    sDBPath = os.path.join(os.path.abspath('..'), bbtConfig.get('Database','dbfolder'), sDBName)
    if not os.path.isfile(sDBPath):
        print "Errore! File %s inesistente!" % sDBPath
        exit(1)

    # mi connetto al database
    conn = getDBConnection(sDBPath)
    # definisco il tipo di riga che vado a leggere, bbtparametereval_factory viene definita in bbtnamedtuples
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # TODO: aggiungo tutte le tbm...
    # tunnelname, tbmname, fine,
    sSql = """select sigma_v_max_tail_skin, sigma_v_max_front_shield
    from BbtParameterEval
    where fine = 36340 and tbmname = 'CE_DS_RBS_6.73_12'""" #!= 'XXX' order by fine, tunnelname, tbmname

    cur.execute(sSql)
    bbtresult = cur.fetchall()

    sigma_array = []
    totals = len(bbtresult)
    cur_pk = float("inf")
    cur_tbm = 'XXX'
    cur_tun = 'XXX'
    for bbtr in bbtresult:
        # Todo: controllo se sono su stesso tunnel, stessa TBM e stessa pk
        if bbtr['tunnelName'] != cur_tun:
            pass
        if bbtr['tbmName'] != cur_tbm:
            pass
        if bbtr['cur_pk'] != cur_pk:
            pass
        sigma = max(bbtr['sigma_v_max_tail_skin'], bbtr['sigma_v_max_front_shield'])
        if sigma > 0:
            sigma_array.append(sigma)
    sigma_ds = [.4, .5, 1., 1.5]

    for sigma_d in sigma_ds:
        sigma_95 = np.nanpercentile(sigma_array,95)
        impact_score = impact((sigma_95-sigma_d)/sigma_d)
        prob_score = probabilityAftes2012(float(len(sigma_array))/float(totals))
        risk_score = impact_score * prob_score




    print "totals=%d, evaluated=%d, sigma95=%f" % (totals, len(sigma_array), sigma_95)
    print "impact_score=%f, prob_score=%f, risk_score=%f" % (impact_score, prob_score, risk_score)

    conn.close()

if __name__ == "__main__":
   RiskAnalisysAftes()