# -*- coding: utf-8 -*-
import csv, pprint, os
from shutil import copyfile
import sys
from collections import defaultdict
from collections import namedtuple
from bbtnamedtuples import BbtGeoitem, BbtParameter, BbtProfilo, BbtReliability
from bbt_database import *
from bbtutils import *
from collections import OrderedDict
import numpy as np
from pylab import *
from scipy.stats import *
import xlrd
from tbmconfig import tbms
########## Mi metto nella directory corrente
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
########## File vari: DB e file excel
# aghensi@20160715 - in import prendo database vuoto e lo sostituisco a database pieno (backup!)
db_folder = os.path.join(os.path.abspath('..'), bbtConfig.get('Database','dbfolder'))
empty_db_name = bbtConfig.get('Database','empty_dbname')
empty_db_path = os.path.join(db_folder, empty_db_name)
if not os.path.isfile(empty_db_path):
    print "Errore! File %s inesistente!" % empty_db_path
    exit(1)
sDBName = bbtConfig.get('Database','dbname')
sDBPath = os.path.join(db_folder, sDBName)
if os.path.isfile(sDBPath):
    os.rename(sDBPath,
              "{}_{}.db".format(os.path.splitext(sDBPath)[0],
                                datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
copyfile(empty_db_path, sDBPath)

import_folder = os.path.join(os.path.abspath('..'),bbtConfig.get('Import','folder'))
sGeoReliability_XLS = os.path.join(import_folder, bbtConfig.get('Import','valutazione'))
if not os.path.isfile(sGeoReliability_XLS):
    print "Errore! File %s inesistente!" % sGeoReliability_XLS
    exit(2)
sCE_XLS = os.path.join(import_folder, bbtConfig.get('Import','geo'))
if not os.path.isfile(sCE_XLS):
    print "Errore! File %s inesistente!" % sCE_XLS
    exit(3)
sProfilo_XLS =os.path.join(import_folder, bbtConfig.get('Import','profilo'))
if not os.path.isfile(sProfilo_XLS):
    print "Errore! File %s inesistente!" % sProfilo_XLS
    exit(4)
# indice dei segmenti gelogici
geosec_index = defaultdict(list)
########### BbtReliability - Acquisisco affidabilita modello GEO
book = xlrd.open_workbook(sGeoReliability_XLS)
xl_sheet = book.sheet_by_name(u'val')
headrow = xl_sheet.row(3)  # header
row = xl_sheet.row(4)  # first row
num_cols = xl_sheet.ncols
reliability_list = []
for row_idx in range(4, xl_sheet.nrows):
    rowvalues=[]
    for col_idx in range(0, num_cols):  # Iterate through columns
        cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
        rowvalues.append(cell_obj.value)
    reliability_item = BbtReliability(*rowvalues)
    reliability_list.append(reliability_item)
# salvo in db BbtReliability
insert_bbtreliability(sDBPath,reliability_list)
######### BbtReliability fine

########### BbtGeoitem - Acquisisco caratteristiche GEO da tavola
book = xlrd.open_workbook(sCE_XLS)
xl_sheet = book.sheet_by_name(u'geo')
headrow = xl_sheet.row(2)  # header
row = xl_sheet.row(3)  # first row
num_cols = xl_sheet.ncols
geoseg_list = []
for row_idx in range(3, xl_sheet.nrows):
    rowvalues=[]
    for col_idx in range(0, num_cols):  # Iterate through columns
        cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
        rowvalues.append(cell_obj.value)
    geoseg = BbtGeoitem(*rowvalues)
    geoseg_list.append(geoseg)
#    reliab_match = [rel for rel in reliability_list if rel.inizio <= geoseg.fine < rel.fine]
#    for reli in reliab_match:
#        print "reliab %d-%s finisce in %f vicino a Geoseg %f" % (reli.id,reli.gmr_class, reli.fine,geoseg.fine)
    geosec_index[geoseg.fine].append(geoseg)
# salvo in db BbtGeoitem
insert_geoitems(sDBPath, geoseg_list)
######### BbtGeoitem fine

########### BbtProfilo - Acquisisco Profilo
bprofilo = xlrd.open_workbook(sProfilo_XLS)
civilReport_sheet = bprofilo.sheet_by_name(u'CivilReport')
headrow = civilReport_sheet.row(0)  # header
row = civilReport_sheet.row(1)  # first row
"""
from xlrd.sheet import ctype_text
print('(Column #) type:value')
for idx, cell_obj in enumerate(row):
    cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
    print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
"""
num_cols = civilReport_sheet.ncols
profilo_list = []
prev_prog = 0
for row_idx in range(17, civilReport_sheet.nrows):
    keepRow = False
    rowvalues=[]
    for col_idx in range(1, num_cols):  # Iterate through columns
        cell_obj = civilReport_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
        if col_idx == 1: # progressiva
            s1 = cell_obj.value.split(',')
            dec = int(s1[1])
            s2 = s1[0].split('+')
            strVal = ''.join(s2)
            pkend = float(strVal)
            if dec == 0 and int(pkend) % 10 == 0:
                rowvalues.append(prev_prog)
                keepRow = True
                rowvalues.append(pkend-10)
                rowvalues.append(pkend)
                prev_prog += 1
        elif keepRow:
            if col_idx in (2, 3, 7, 8): # est, nord, tipo punto, prof falda
                rowvalues.append(cell_obj.value)
            if col_idx in (4, 5, 6): #quota altimetrica, di progetto e copertura: 1.871,894m
                s1 = cell_obj.value.split(",")
                if len(s1) > 1:
                    s2 = s1[0].split('.')
                    strVal = ''.join(s2)
                    rowvalues.append(float(strVal))
                else:
                    rowvalues.append(0)
    if rowvalues:
        bbtpro = BbtProfilo(*rowvalues)
        profilo_list.append(bbtpro)
# salvo profilo
insert_profilo(sDBPath,profilo_list)
######### BbtProfilo fine

######## BbtParameter rappresenta il segmento unitario con i parametri geologici base valorizzati secondo i dati provenienti dalle tavole geologiche
geoitems=defaultdict(list)
# aghensi@20160704 - mantengo tutti i terreni con le loro percentuali - inizio
bbtpar_items = []
for bbtpro in profilo_list:
    for geosec in geoseg_list:
        if geosec.inizio <=  bbtpro.fine < geosec.fine:
            tmparr = [bbtpro.inizio , bbtpro.fine, bbtpro.est, bbtpro.nord, bbtpro.he, bbtpro.hp,
                      bbtpro.co, bbtpro.tipo, bbtpro.wdepth,
                      geosec.g_med, geosec.g_stddev, geosec.sigma_ci_avg, geosec.sigma_ci_stdev,
                      geosec.mi_med, geosec.mi_stdev, geosec.ei_med, geosec.ei_stdev,
                      geosec.cai_med, geosec.cai_stdev, geosec.gsi_med, geosec.gsi_stdev,
                      geosec.rmr_med, geosec.rmr_stdev, bbtpro.id, geosec.id, geosec.title,
                      geosec.sigma_ti_min, geosec.sigma_ti_max, geosec.k0_min, geosec.k0_max,
                      geosec.perc, geosec.anidrite]
            bbtpar = BbtParameter(*tmparr)
            bbtpar_items.append(bbtpar)

#bbtpar_items = []
#for k in geoitems:
#    print "geoseg %d-%d ================" % (geosec_index[k][0].inizio, geosec_index[k][0].fine)
#    totItem = 0
#    px = []
#    gx = []
#    for geosec in geosec_index[k]:
#        itemNo = int(geosec.perc*len(geoitems[k]))
#        if itemNo == 0:
#            itemNo = 1
#        px.append(itemNo)
#        gx.append(geosec)
#        totItem = sum(px)
#        print "\t%s - %f - %d" % (geosec.type, geosec.perc, itemNo)
#    missing = len(geoitems[k])-totItem
#    print "\n\t%d vs %d, missing %d" % (totItem, len(geoitems[k]), missing)
#    for i in range(missing):
#        px[i] = px[i] + 1
#    print "\t%s" % px
#    prev = 0
#    for i, pitem in enumerate(px):
#        geosec = gx[i]
#        for j in range(prev, prev+pitem):
#            pk = geoitems[k][j]
#            tmparr = [pk.inizio , pk.fine, pk.est, pk.nord, pk.he, pk.hp, pk.co, pk.tipo,
#                      geosec.g_med, geosec.g_stddev, geosec.sigma_ci_avg, geosec.sigma_ci_stdev,
#                      geosec.mi_med, geosec.mi_stdev, geosec.ei_med, geosec.ei_stdev,
#                      geosec.cai_med, geosec.cai_stdev, geosec.gsi_med, geosec.gsi_stdev,
#                      geosec.rmr_med, geosec.rmr_stdev, pk.id, geosec.id, geosec.title,
#                      geosec.sigma_ti_min, geosec.sigma_ti_max, geosec.k0_min, geosec.k0_max]
#            #print "\t profile %f-%f has geoclass ending in %f with perc %f" % (pk.inizio,pk.fine,geosec.fine,geosec.perc)
#            bbtpar = BbtParameter(*tmparr)
#            bbtpar_items.append(bbtpar)
#        prev += px[i]
# aghensi@20160704 - mantengo tutti i terreni con le loro percentuali - fine

# salvo parametri
insert_parameters(sDBPath,bbtpar_items)
######### BbtParameter fine
load_tbm_table(sDBPath, tbms)
print "######### BbtParameter fine"
