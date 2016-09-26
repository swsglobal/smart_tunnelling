# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:37:33 2016

@author: aghensi
"""
import sqlite3
import os
import csv

import bbtutils
from bbt_database import getDBConnection

def get_strata_summary():
    '''
    restituisce una tabella con pressioni agenti sull'anello, modulo elastico e k0 relativi,
    oltre alle dimensioni dell'anello (r = raggio, d = spessore, l = lunghezza)
    '''
    tunnelArray = ['GL']
    tbmfilter = {'GL': ['TEST_5', 'TEST_10', 'TEST_12']}
    dimensions = {'GL': {'r':11.9/2+0.55,'d':0.55,'l':1.5}}


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
    sql_query = "select id, title, inizio, fine, perc, k0_min, k0_max from  BbtGeoitem"
    cur.execute(sql_query)
    strataresult = cur.fetchall()
    csv_header = ['inizio', 'fine', 'title', 'lung',
                  'sigma_v', 'E', 'K0_min', 'K0_max', 'r', 'd', 'l' ]
    for tun in tunnelArray:
        # dovrei filtrare i filtri tbm in base al tun...
        for tbm in tbmfilter[tun]:
            outvalues = []
            for strata in strataresult:
                sql_query = """select fine, geoitem_id, title, sigma_v_max_lining, ei
                from BbtParameterEval
                where tunnelName = '{}' and tbmName = '{}' and sigma_v_max_lining>0
                AND geoitem_id = {} order by inizio""".format(tun, tbm, strata['id'])
                cur.execute(sql_query)
                bbtresult = cur.fetchall()
                if len(bbtresult) > 0:
                    sigma_v_max = 0.
                    ei = 0
                    for item in bbtresult:
                        sigma_v = item['sigma_v_max_lining']
                        if sigma_v > sigma_v_max:
                            sigma_v_max = sigma_v
                            ei = item['ei']
                    lung = (strata['fine'] - strata['inizio']) * strata['perc']
            # scrivo in csv
                    outvalues.append([strata['inizio'], strata['fine'], strata['title'], lung,
                                      sigma_v_max, ei, strata['k0_min'], strata['k0_max'],
                                      dimensions[tun]['r'], dimensions[tun]['d'],
                                      dimensions[tun]['l'] ])
            if len(outvalues) > 0:
                csvfname=os.path.join(outfolder,"%s_%s_lining_summary.csv" % (tun.replace(" ", "_"), tbm))
                with open(csvfname, 'wb') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(csv_header)
                    writer.writerows(outvalues)
                print "{} {} done.".format(tun, tbm)

if __name__ == "__main__":
    get_strata_summary()
