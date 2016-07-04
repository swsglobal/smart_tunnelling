import sqlite3
from collections import defaultdict
from bbtnamedtuples import *

# danzi.tn@20151120 entry point per connessione db
def getDBConnection(sDBPath):
    return sqlite3.connect(sDBPath, timeout=30.0)

def get_bbtparameterseval(sDBPath):
    conn = getDBConnection(sDBPath)
    conn.row_factory = bbtparametereval_factory
    cur = conn.cursor()
    cur.execute("SELECT insertdate,iteration_no,fine,he,hp,co,gamma,sigma,mi,ei,cai,gsi,rmr,pkgl,closure,rockburst,front_stability_ns,front_stability_lambda,penetrationRate,penetrationRateReduction,contactThrust,torque,frictionForce,requiredThrustForce,availableThrust,dailyAdvanceRate,profilo_id,geoitem_id,title,sigma_ti,k0 FROM BbtParameterEval ORDER BY iteration_no, profilo_id")
    bbtresults = cur.fetchall()
    bbt_bbtparameterseval = []
    for bbt_parametereval in bbtresults:
        bbt_bbtparameterseval.append(bbt_parametereval)
    conn.close()
    return bbt_bbtparameterseval

def get_bbtparameterseval4iter(sDBPath,nIter,sKey):
    conn = getDBConnection(sDBPath)
    conn.row_factory = bbtParameterEvalMin_factory
    cur = conn.cursor()
    bbt_bbtparameterseval = {}
    cur.execute("SELECT gamma,sigma,mi,ei,cai,rmr, gsi, sigma_ti, k0 , profilo_id FROM BbtParameterEval WHERE iteration_no = ?AND tunnelName = ? ORDER BY profilo_id" , (nIter,sKey) )
    bbtresults = cur.fetchall()
    for bbt_parametereval in bbtresults:
        bbt_bbtparameterseval[bbt_parametereval.profilo_id] = bbt_parametereval
    conn.close()
    return bbt_bbtparameterseval

def get_mainbbtparameterseval(sDBPath,sKey,iterMin, iterMax):
    conn = getDBConnection(sDBPath)
    conn.row_factory = bbtParameterEvalMain_factory
    cur = conn.cursor()
    bbt_bbtparameterseval = defaultdict(list)
    cur.execute("SELECT BbtParameter.inizio,BbtParameter.fine,BbtParameter.est,BbtParameter.nord,\
                 BbtParameter.he,BbtParameter.hp,BbtParameter.co,BbtParameter.tipo,\
                 BbtParameter.g_med,BbtParameter.g_stddev,BbtParameter.sigma_ci_avg,\
                 BbtParameter.sigma_ci_stdev,BbtParameter.mi_med,BbtParameter.mi_stdev,\
                 BbtParameter.ei_med,BbtParameter.ei_stdev,BbtParameter.cai_med,\
                 BbtParameter.cai_stdev,BbtParameter.gsi_med,BbtParameter.gsi_stdev,\
                 BbtParameter.rmr_med,BbtParameter.rmr_stdev,BbtParameter.profilo_id,\
                 BbtParameter.geoitem_id,BbtParameter.title,BbtParameter.sigma_ti_min,\
                 BbtParameter.sigma_ti_max,BbtParameter.k0_min,BbtParameter.k0_max,\
                 BbtParameter.perc,BbtParameter.wdepth,\
                 BbtParameterEval.gamma,BbtParameterEval.sigma,BbtParameterEval.mi,\
                 BbtParameterEval.ei,BbtParameterEval.cai,BbtParameterEval.rmr,\
                 BbtParameterEval.gsi, BbtParameterEval.sigma_ti,BbtParameterEval.k0,\
                 BbtParameterEval.iteration_no,BbtParameterEval.insertdate\
                 FROM BbtParameterEval \
                 JOIN BbtParameter ON BbtParameter.profilo_id = BbtParameterEval.profilo_id \
                 WHERE BbtParameterEval.tunnelName = ? AND BbtParameterEval.iteration_no>=? \
                 AND BbtParameterEval.iteration_no < ? \
                 ORDER BY BbtParameterEval.profilo_id, BbtParameter.inizio",
                 (sKey,iterMin,iterMax))
    bbtresults = cur.fetchall()
    for bbt_parametereval in bbtresults:
        bbt_bbtparameterseval[bbt_parametereval.iteration_no].append( bbt_parametereval )
    conn.close()
    return bbt_bbtparameterseval

def get_bbtparameters(sDBPath):
    conn = getDBConnection(sDBPath)
    conn.row_factory = bbtparameter_factory
    cur = conn.cursor()
    bbtresults = cur.execute("SELECT inizio,fine,est,nord,he,hp,co,tipo,wdepth,g_med,g_stddev,\
                              sigma_ci_avg,sigma_ci_stdev,mi_med,mi_stdev,ei_med,ei_stdev,cai_med,\
                              cai_stdev,gsi_med,gsi_stdev,rmr_med,rmr_stdev,profilo_id,geoitem_id,\
                              title,sigma_ti_min,sigma_ti_max,k0_min,k0_max,perc\
                              FROM bbtparameter ORDER BY profilo_id")
    bbt_parameters = []
    for bbt_parameter in bbtresults:
        bbt_parameters.append(bbt_parameter)
    conn.close()
    return bbt_parameters


def insert_parameters(sDBPath,bbtpar_items):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute('delete from BbtParameter')
    for bbtpar in bbtpar_items:
        c.execute('insert into BbtParameter (inizio,fine,est,nord,he,hp,co,tipo,wdepth,g_med,g_stddev,\
                   sigma_ci_avg,sigma_ci_stdev,mi_med,mi_stdev,ei_med,ei_stdev,cai_med,cai_stdev,\
                   gsi_med,gsi_stdev,rmr_med,rmr_stdev,profilo_id,geoitem_id,title,sigma_ti_min,\
                   sigma_ti_max,k0_min,k0_max,perc)\
                   values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', bbtpar)
    conn.commit()
    conn.close()

def insert_profilo(sDBPath,profilo_list):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute('delete from BbtProfilo')
    for bbtpro in profilo_list:
        c.execute('insert into BbtProfilo (id,inizio,fine,est,nord,he,hp,co,tipo,wdepth) values (?,?,?,?,?,?,?,?,?,?)', bbtpro)
    conn.commit()
    conn.close()

def insert_geoitems(sDBPath,geoseg_list):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute('delete from BbtGeoitem')
    for geoseg in geoseg_list:
        c.execute('insert into BbtGeoitem (id,inizio,fine,l,perc,type,g_med,g_stddev,sigma_ci_avg,sigma_ci_stdev,mi_med,mi_stdev,ei_med,ei_stdev,cai_med,cai_stdev,gsi_med,gsi_stdev,rmr_med,rmr_stdev,title,sigma_ti_min,sigma_ti_max,k0_min,k0_max ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', geoseg)
    conn.commit()
    conn.close()

def insert_bbtreliability(sDBPath, reliability_list):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute('delete from BbtReliability')
    for rel in reliability_list:
        c.execute('insert into BbtReliability (id ,inizio, fine , gmr_class, gmr_val, reliability, eval_var) values (?,?,?,?,?,?,?)', rel)
    conn.commit()
    conn.close()

def compact_database(sDBPath):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute("VACUUM")
    conn.commit()
    conn.close()

def insert_BbtTbm(sDBPath, tbm_list):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute('delete from BbtTbm')
    for rel in reliability_list:
        c.execute('insert into BbtTbm (id ,inizio, fine , gmr_class, gmr_val, reliability, eval_var) values (?,?,?,?,?,?,?)', rel)
    conn.commit()
    conn.close()


#danzi.tn@20151118 ottmizzazione scritture su DB
def deleteEval4Tbm(sDBPath,loopTbms):
    if len(loopTbms) > 0:
        tbmList = []
        for k in loopTbms:
            tbmList.append((k,))
        conn = getDBConnection(sDBPath)
        c = conn.cursor()
        c.executemany("DELETE FROM BbtTbmKpi WHERE tbmName = ? ", tbmList)
        conn.commit()
        c.executemany("DELETE FROM BbtParameterEval WHERE tbmName = ?" , tbmList)
        conn.commit()
        conn.close()

def delete_eval4Geo(sDBPath,sKey):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute("DELETE FROM BbtParameterEval WHERE tunnelName = '%s'" % sKey )
    conn.commit()
    conn.close()

def check_eval4Geo(sDBPath,sKey):
    iMax = 0
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute("SELECT  max(BbtParameterEval.iteration_no) +1 FROM BbtParameterEval WHERE BbtParameterEval.tunnelName = '%s'" % sKey )
    bbtresult = c.fetchone()
    iMax = float(bbtresult[0])
    conn.close()
    return iMax


def insert_eval4Geo(sDBPath, bbt_evalparameters):
    if len(bbt_evalparameters) > 0:
        conn = getDBConnection(sDBPath)
        c = conn.cursor()
        c.executemany("INSERT INTO BbtParameterEval (insertdate,iteration_no,tunnelName,tbmName,\
                       fine,he,hp,co,wdepth,gamma,sigma,mi,ei,cai,gsi,rmr,pkgl,closure,rockburst,\
                       front_stability_ns,front_stability_lambda,penetrationRate,\
                       penetrationRateReduction,contactThrust,torque,frictionForce,\
                       requiredThrustForce,availableThrust,dailyAdvanceRate,profilo_id,geoitem_id,\
                       title,sigma_ti,k0,t0,t1,t3,t4,t5,inSituConditionSigmaV,tunnelRadius,rockE,\
                       mohrCoulombPsi,rockUcs,inSituConditionGsi,hoekBrownMi,hoekBrownD,\
                       hoekBrownMb,hoekBrownS,hoekBrownA,hoekBrownMr,hoekBrownSr,hoekBrownAr,\
                       urPiHB,rpl,picr,ldpVlachBegin,ldpVlachEnd)\
                       values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                       ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       bbt_evalparameters)
        conn.commit()
        conn.close()

def insert_eval4Iter(sDBPath, bbt_evalparameters, bbttbmkpis):
    if len(bbt_evalparameters) > 0 and len(bbttbmkpis) > 0:
        conn = getDBConnection(sDBPath)
        c = conn.cursor()
        c.executemany("INSERT INTO BbtTbmKpi (tunnelName,tbmName,iterationNo,kpiKey,kpiDescr,minImpact,maxImpact,avgImpact,appliedLength,percentOfApplication,probabilityScore,totalImpact) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", bbttbmkpis)
        conn.commit()
        c.executemany("INSERT INTO BbtParameterEval (insertdate,\
                                                            iteration_no, \
                                                            tunnelName,\
                                                            tbmName,\
                                                            fine,\
                                                            he,\
                                                            hp,\
                                                            co,\
                                                            wdepth,\
                                                            gamma,\
                                                            sigma,\
                                                            mi,\
                                                            ei,\
                                                            cai,\
                                                            gsi,\
                                                            rmr,\
                                                            pkgl,\
                                                            closure,\
                                                            rockburst,\
                                                            front_stability_ns,\
                                                            front_stability_lambda,\
                                                            penetrationRate,\
                                                            penetrationRateReduction,\
                                                            contactThrust,\
                                                            torque,\
                                                            frictionForce,\
                                                            requiredThrustForce,\
                                                            availableThrust,\
                                                            dailyAdvanceRate,profilo_id, geoitem_id ,title,sigma_ti,k0,t0,t1,t3,t4,t5, \
                                                            inSituConditionSigmaV,\
                                                            tunnelRadius,\
                                                            rockE,\
                                                            mohrCoulombPsi,\
                                                            rockUcs,\
                                                            inSituConditionGsi,\
                                                            hoekBrownMi,\
                                                            hoekBrownD,\
                                                            hoekBrownMb,\
                                                            hoekBrownS,\
                                                            hoekBrownA,\
                                                            hoekBrownMr,\
                                                            hoekBrownSr,\
                                                            hoekBrownAr,\
                                                            urPiHB,\
                                                            rpl,\
                                                            picr,\
                                                            ldpVlachBegin,\
                                                            ldpVlachEnd\
        ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", bbt_evalparameters)
        conn.commit()
        conn.close()


#danzi.tn@20151114 inseriti nuovi parametri calcolati su TunnelSegment
def insert_bbtparameterseval(sDBPath, bbt_evalparameters, iteration_no=0):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    isFirst=True
    if len(bbt_evalparameters) > 0:
        bbtpar = bbt_evalparameters[0]
        c.execute("delete from BbtParameterEval WHERE iteration_no = %d AND tunnelName ='%s' AND tbmName='%s'" % (bbtpar[1],bbtpar[2],bbtpar[3]))
        c.executemany("insert into BbtParameterEval (           insertdate,\
                                                            iteration_no, \
                                                            tunnelName,\
                                                            tbmName,\
                                                            fine,\
                                                            he,\
                                                            hp,\
                                                            co,\
                                                            wdepth,\
                                                            gamma,\
                                                            sigma,\
                                                            mi,\
                                                            ei,\
                                                            cai,\
                                                            gsi,\
                                                            rmr,\
                                                            pkgl,\
                                                            closure,\
                                                            rockburst,\
                                                            front_stability_ns,\
                                                            front_stability_lambda,\
                                                            penetrationRate,\
                                                            penetrationRateReduction,\
                                                            contactThrust,\
                                                            torque,\
                                                            frictionForce,\
                                                            requiredThrustForce,\
                                                            availableThrust,\
                                                            dailyAdvanceRate,profilo_id, geoitem_id ,title,sigma_ti,k0,t0,t1,t3,t4,t5, \
                                                            inSituConditionSigmaV,\
                                                            tunnelRadius,\
                                                            rockE,\
                                                            mohrCoulombPsi,\
                                                            rockUcs,\
                                                            inSituConditionGsi,\
                                                            hoekBrownMi,\
                                                            hoekBrownD,\
                                                            hoekBrownMb,\
                                                            hoekBrownS,\
                                                            hoekBrownA,\
                                                            hoekBrownMr,\
                                                            hoekBrownSr,\
                                                            hoekBrownAr,\
                                                            urPiHB,\
                                                            rpl,\
                                                            picr,\
                                                            ldpVlachBegin,\
                                                            ldpVlachEnd\
        ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", bbt_evalparameters)
        conn.commit()
    conn.close()



def insert_one_bbtparameterseval(cur, bbtpar):
    cur.execute("insert into BbtParameterEval (           insertdate,\
                                                        iteration_no, \
                                                        fine,\
                                                        he,\
                                                        hp,\
                                                        co,\
                                                        wdepth,\
                                                        gamma,\
                                                        sigma,\
                                                        mi,\
                                                        ei,\
                                                        cai,\
                                                        gsi,\
                                                        rmr,\
                                                        pkgl,\
                                                        closure,\
                                                        rockburst,\
                                                        front_stability_ns,\
                                                        front_stability_lambda,\
                                                        penetrationRate,\
                                                        penetrationRateReduction,\
                                                        contactThrust,\
                                                        torque,\
                                                        frictionForce,\
                                                        requiredThrustForce,\
                                                        availableThrust,\
                                                        dailyAdvanceRate,profilo_id, geoitem_id ,title,sigma_ti,k0 \
    ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", bbtpar)


# danzi.tn@20151116 pulizia delle valutazioni
def clean_all_eval_ad_kpi(sDBPath):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute("delete from BbtParameterEval")
    c.execute("delete from BbtTbmKpi")
    conn.commit()
    conn.close()


def load_tbm_table(sDBPath, tbmsDict):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute("delete from BbtTbm")
    for tbmKey in tbmsDict:
        tbmData = tbmsDict[tbmKey]
        inputVal = (tbmData.name,tbmData.alignmentCode,tbmData.manifacturer,tbmData.type,tbmData.shieldLength,tbmData.overcut)
        c.execute("INSERT INTO BbtTbm (name,alignmentCode,manufacturer,type,shieldLength,overcut) VALUES (?,?,?,?,?,?)", inputVal)
    conn.commit()
    conn.close()
