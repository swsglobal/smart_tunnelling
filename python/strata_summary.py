# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:37:33 2016

@author: aghensi
"""
import sqlite3
import os
import csv
from bbtutils import bbtConfig
from bbt_database import getDBConnection

def get_strata_summary():

    tunnelArray = ['CE', 'GL Nord']
    tbmfilter = {'CE': ['CE_DS_HRK_6.82_00', 'CE_DS_HRK_6.82_112', 'CE_DS_RBS_6.73_00', 'CE_DS_RBS_6.73_12'],
                 'GL Nord': ['GL_DS_HRK_10.60_00', 'GL_DS_HRK_10.60_112', 'GL_DS_RBS_10.56_00', 'GL_DS_RBS_10.56_12']}


    outfoldername = bbtConfig.get('Diagrams','folder')
    outfolder = os.path.join(os.path.abspath('..'), outfoldername)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)


    db_name = bbtConfig.get('Database', 'dbname')
    db_path = os.path.join(os.path.abspath('..'), bbtConfig.get('Database', 'dbfolder'),
                           db_name)
    if not os.path.isfile(db_path):
        print "Errore! File %s inesistente!" % db_path
        exit(1)
    conn = getDBConnection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql_query = "select id, title, inizio, fine, perc from  BbtGeoitem"
    cur.execute(sql_query)
    strataresult = cur.fetchall()
    csv_header = ['inizio', 'fine', 'title', 'lung', 'iterazioni',
                  'contatto', 'sv_gt_400_Kpa', 'sv_gt_500_Kpa', 'sv_gt_1000_Kpa', 'sv_gt_1500_Kpa',
                  'sv_gt_2000_Kpa', 'sv_gt_2500_Kpa', 'sv_lt_1000_Kpa', 'sigma_v_max']
    for tun in tunnelArray:
        # dovrei filtrare i filtri tbm in base al tun...
        for tbm in tbmfilter[tun]:
            outvalues = []
            for strata in strataresult:
                sql_query = """select fine, dailyAdvanceRate, geoitem_id, title, sigma_v_max_tail_skin,
                sigma_v_max_front_shield, overcut_required, ei, k0_min, k0_max
                from BbtParameterEval
                where tunnelName = '{}' and tbmName = '{}'
                AND geoitem_id = {} order by inizio""".format(tun, tbm, strata['id'])
                cur.execute(sql_query)
                bbtresult = cur.fetchall()
                if len(bbtresult) > 0:
                    sigma_v_max = 0.
                    iter_count = len(bbtresult)
                    contatto = 0.
                    sv_gt_400_Kpa = 0.
                    sv_gt_500_Kpa = 0.
                    sv_gt_1000_Kpa = 0.
                    sv_gt_1500_Kpa = 0.
                    sv_gt_2000_Kpa = 0.
                    sv_gt_2500_Kpa = 0.
                    sv_lt_1000_Kpa = 0.
                    for item in bbtresult:
                        contatto += item['overcut_required']
                        sigma_v = max(item['sigma_v_max_front_shield'], item['sigma_v_max_tail_skin'])
                        sigma_v_max = max(sigma_v, sigma_v_max)
                        if sigma_v > 0.4:
                            sv_gt_400_Kpa += 1.
                        if sigma_v > .5:
                            sv_gt_500_Kpa += 1.
                        if sigma_v > 1.:
                            sv_gt_1000_Kpa += 1.
                        if sigma_v > 1.5:
                            sv_gt_1500_Kpa += 1.
                        if sigma_v > 2.:
                            sv_gt_2000_Kpa += 1.
                        if sigma_v > 2.5:
                            sv_gt_2500_Kpa += 1.
                        elif sigma_v > 0.:
                            sv_lt_1000_Kpa += 1.

                    sv_gt_400_Kpa /= float(iter_count)
                    sv_gt_500_Kpa /= float(iter_count)
                    sv_gt_1000_Kpa /= float(iter_count)
                    sv_gt_1500_Kpa /= float(iter_count)
                    sv_gt_2000_Kpa /= float(iter_count)
                    sv_gt_2500_Kpa /= float(iter_count)
                    sv_lt_1000_Kpa /= float(iter_count)
                    contatto /= float(iter_count)
                    lung = (strata['fine'] - strata['inizio']) * strata['perc']
            # scrivo in csv
                    outvalues.append([strata['inizio'], strata['fine'], strata['title'], lung,
                                      iter_count, contatto, sv_gt_400_Kpa, sv_gt_500_Kpa, sv_gt_1000_Kpa,
                                      sv_gt_1500_Kpa, sv_gt_2000_Kpa, sv_gt_2500_Kpa,
                                      sv_lt_1000_Kpa, sigma_v_max])
            if len(outvalues) > 0:
                csvfname=os.path.join(outfolder,"%s_%s_strata_summary.csv" % (tun.replace(" ", "_"), tbm))
                with open(csvfname, 'wb') as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(csv_header)
                    writer.writerows(outvalues)
                print "{} {} done.".format(tun, tbm)

if __name__ == "__main__":
    get_strata_summary()
