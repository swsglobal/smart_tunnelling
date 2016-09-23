import sqlite3
from collections import defaultdict
from bbtnamedtuples import *

# danzi.tn@20151120 entry point per connessione db
def getDBConnection(sDBPath):
    return sqlite3.connect(sDBPath, timeout=30.0)

def check_journal_mode(sDBPath):
    conn = getDBConnection(sDBPath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode")
    return cur.fetchone()[0]

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

def get_mainbbtparameterseval(sDBPath, sKey, iterMin, iterMax):
    # TODO: qui devo raggruppare gli elementi per iteration_no! in un defaultdict(list)
    wherestring = "tunnelName = '{}' AND iteration_no>= {} AND iteration_no < {}".format(sKey, iterMin, iterMax)
    tuple_list = get_db_namedtuple(sDBPath, BbtParameterEval, wherestring, "profilo_id, fine, iteration_no")
    return_dict = defaultdict(list)
    for pareval_tuple in tuple_list:
        return_dict[pareval_tuple.iteration_no].append(pareval_tuple)
    return return_dict

def get_db_namedtuple(db_path, named_tuple, where=None, order=None):
    conn = getDBConnection(db_path)
    conn.row_factory = nt_factory(named_tuple)
    selectquery = "SELECT {} FROM {}".format(",".join(named_tuple._fields), named_tuple.__name__)
    if where:
        wherequery = "WHERE {}".format(where)
    else:
        wherequery = ""
    if order:
        orderquery = "ORDER BY {}".format(order)
    else:
        orderquery = ""
    query = " ".join([selectquery, wherequery, orderquery])
    len(named_tuple._fields)
    cur = conn.cursor()
    return_list = list(cur.execute(query))
    conn.close()
    return return_list


def get_namedtuple_fields(named_tuple):
    """Return the name of a namedtuple, a string containing the fields names and the number of fields"""
    return named_tuple.__class__.__name__, ",".join(named_tuple._fields), len(named_tuple._fields)


def insert_namedtuple(db_path, tuple_list, delete=False):
    """Inserts a list of a generic namedtuple into a table with the same name of the namedtuple"""
    table_name, fields, howmany = get_namedtuple_fields(tuple_list[0])
    sql_string = "insert into {} ({}) values ({})".format(table_name, fields,
                                                          ",".join("?" * howmany))
    conn = getDBConnection(db_path)
    c = conn.cursor()
    if delete:
        c.execute("delete from {}".format(table_name))
    c.executemany(sql_string, tuple_list)
    conn.commit()
    conn.close()


def compact_database(sDBPath):
    conn = getDBConnection(sDBPath)
    c = conn.cursor()
    c.execute("VACUUM")
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


def insert_eval4Iter(db_path, bbt_evalparameters, bbttbmkpis):
    if len(bbt_evalparameters) > 0 and len(bbttbmkpis) > 0:
        insert_namedtuple(db_path, bbttbmkpis)
        insert_namedtuple(db_path, bbt_evalparameters)


# OLD
#danzi.tn@20151114 inseriti nuovi parametri calcolati su TunnelSegment
#def insert_bbtparameterseval(sDBPath, bbt_evalparameters, iteration_no=0):
#    conn = getDBConnection(sDBPath)
#    c = conn.cursor()
#    isFirst=True
#    if len(bbt_evalparameters) > 0:
#        bbtpar = bbt_evalparameters[0]
#        c.execute("delete from BbtParameterEval WHERE iteration_no = %d AND tunnelName ='%s' AND tbmName='%s'" % (bbtpar[1],bbtpar[2],bbtpar[3]))
#        c.executemany("insert into BbtParameterEval (           insertdate,\
#                                                            iteration_no, \
#                                                            tunnelName,\
#                                                            tbmName,\
#                                                            fine,\
#                                                            he,\
#                                                            hp,\
#                                                            co,\
#                                                            wdepth,\
#                                                            gamma,\
#                                                            sigma,\
#                                                            mi,\
#                                                            ei,\
#                                                            cai,\
#                                                            gsi,\
#                                                            rmr,\
#                                                            pkgl,\
#                                                            closure,\
#                                                            rockburst,\
#                                                            front_stability_ns,\
#                                                            front_stability_lambda,\
#                                                            penetrationRate,\
#                                                            penetrationRateReduction,\
#                                                            contactThrust,\
#                                                            torque,\
#                                                            frictionForce,\
#                                                            requiredThrustForce,\
#                                                            availableThrust,\
#                                                            dailyAdvanceRate,profilo_id, geoitem_id ,title,sigma_ti,k0,t0,t1,t3,t4,t5, \
#                                                            inSituConditionSigmaV,\
#                                                            tunnelRadius,\
#                                                            rockE,\
#                                                            mohrCoulombPsi,\
#                                                            rockUcs,\
#                                                            inSituConditionGsi,\
#                                                            hoekBrownMi,\
#                                                            hoekBrownD,\
#                                                            hoekBrownMb,\
#                                                            hoekBrownS,\
#                                                            hoekBrownA,\
#                                                            hoekBrownMr,\
#                                                            hoekBrownSr,\
#                                                            hoekBrownAr,\
#                                                            urPiHB,\
#                                                            rpl,\
#                                                            picr,\
#                                                            ldpVlachBegin,\
#                                                            ldpVlachEnd\
#        ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", bbt_evalparameters)
#        conn.commit()
#    conn.close()



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
