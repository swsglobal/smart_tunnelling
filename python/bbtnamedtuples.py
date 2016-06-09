from collections import namedtuple
# aghensi@20160601 - adattamento tuple per filippine e restyling PEP8
BbtGeoitem = namedtuple('BbtGeoitem', ['id', 'inizio', 'fine', 'l', 'perc', 'type', 'g_med',
                                       'g_stddev', 'phimin', 'phimax', 'ei_med', 'ei_stdev',
                                       'c_med', 'c_stdev', 'rmr_med', 'rmr_stdev', 'title',
                                       'k0_min', 'k0_max', 'w_inflow_min', 'w_inflow_max',
                                       'UCS_min', 'UCS_max'])
BbtProfilo = namedtuple('BbtProfilo', ['id', 'inizio', 'fine', 'est', 'nord', 'he', 'hp', 'co',
                                       'hw', 'wdepth'])
BbtParameter = namedtuple('BbtParameter', ['inizio', 'fine', 'est', 'nord', 'he', 'hp', 'co', 'hw',
                                           'wdepth', 'g_med', 'g_stddev', 'phimin', 'phimax',
                                           'ei_med', 'ei_stdev', 'c_med', 'c_stdev', 'rmr_med',
                                           'rmr_stdev', 'profilo_id', 'geoitem_id', 'title',
                                           'k0_min', 'k0_max', 'w_inflow_min', 'w_inflow_max',
                                           'UCS_min', 'UCS_max'])
BbtReliability = namedtuple('BbtReliability', ['id', 'inizio', 'fine', 'gmr_class', 'gmr_val',
                                               'reliability', 'eval_var'])
BbtParameterEvalMin = namedtuple('BbtParameterEvalMin', ['gamma', 'phi', 'ei', 'c', 'rmr', 'k0',
                                                         'winflow', 'profilo_id'])

BbtParameterEvalMain = namedtuple('BbtParameterEvalMain', ['inizio', 'fine', 'est', 'nord', 'he',
                                                           'hp', 'co', 'hw', 'wdepth', 'g_med',
                                                           'g_stddev', 'phimin', 'phimax',
                                                           'ei_med', 'ei_stdev', 'c_med',
                                                           'c_stdev', 'rmr_med', 'rmr_stdev',
                                                           'profilo_id', 'geoitem_id', 'title',
                                                           'k0_min', 'k0_max', 'w_inflow_min',
                                                           'w_inflow_max', 'gamma', 'phi', 'ei',
                                                           'c', 'rmr', 'k0', 'winflow', 'ucs',
                                                           'iteration_no', 'insertdate'])

#danzi.tn@20151114 inseriti nuovi parametri calcolati su TunnelSegment
BbtParameterEval = namedtuple('BbtParameterEval', ['insertdate', 'iteration_no', 'fine', 'he', 'hp',
                                                   'co', 'hw', 'wdepth', 'gamma', 'phi', 'ei', 'c',
                                                   'rmr', 'pkgl', 'closure', 'rockburst',
                                                   'front_stability_ns', 'front_stability_lambda',
                                                   'penetrationRate', 'penetrationRateReduction',
                                                   'contactThrust', 'torque', 'frictionForce',
                                                   'requiredThrustForce', 'availableThrust',
                                                   'dailyAdvanceRate', 'profilo_id', 'geoitem_id',
                                                   'title', 'k0', 'winflow',
                                                   't0', 't1', 't3', 't4', 't5',
                                                   'inSituConditionSigmaV', 'tunnelRadius',
                                                   'rockE', 'mohrCoulombPsi', 'rockUcs',
                                                   'inSituConditionGsi', 'hoekBrownMi',
                                                   'hoekBrownD', 'hoekBrownMb', 'hoekBrownS',
                                                   'hoekBrownA', 'hoekBrownMr', 'hoekBrownSr',
                                                   'hoekBrownAr', 'urPiHB', 'rpl', 'picr',
                                                   'ldpVlachBegin', 'ldpVlachEnd','ucs'])

BbtParameter4Seg = namedtuple('BbtParameter4Seg', ['inizio', 'fine', 'length', 'he', 'hp', 'co',
                                                   'gamma', 'phi', 'ei', 'c', 'rmr', 'profilo_id',
                                                   'geoitem_id', 'descr', 'k0', 'winflow', 'ucs',
                                                   'wdepth', 'k0_min', 'k0_max'])
BbtTbmKpi = namedtuple('BbtTbmKpi', ['tunnelName', 'tbmName', 'iterationNo', 'kpiKey', 'kpiDescr',
                                     'minImpact', 'maxImpact', 'avgImpact', 'appliedLength',
                                     'percentOfApplication', 'probabilityScore', 'totalImpact'])

def bbtparameter_factory(cursor, row):
    return BbtParameter(*row)

def bbtprofilo_factory(cursor, row):
    return BbtProfilo(*row)

def bbtgeoitem_factory(cursor, row):
    return BbtGeoitem(*row)

def bbtparametereval_factory(cursor, row):
    return BbtParameterEval(*row)

def bbttbmkpi_factory(cursor, row):
    return BbtTbmKpi(*row)

def bbtParameterEvalMin_factory(cursor, row):
    return BbtParameterEvalMin(*row)

def bbtParameterEvalMain_factory(cursor, row):
    return BbtParameterEvalMain(*row)

bbtClassReliabilityList = []
BbtClassReliability = namedtuple('BbtClassReliability', ['code', 'reliability', 'gmr_min',
                                                         'gmr_max', 'min_val', 'max_val'])
bbtcls = BbtClassReliability('A', 'Buona', 7.5, 10, 50, 0)
bbtClassReliabilityList.append(bbtcls)
bbtcls = BbtClassReliability('B', 'Discreta', 5, 7.5, 100, 50)
bbtClassReliabilityList.append(bbtcls)
bbtcls = BbtClassReliability('C', 'Scarsa', 2.5, 5, 200, 100)
bbtClassReliabilityList.append(bbtcls)
bbtcls = BbtClassReliability('D', 'Non affidabile', 0, 2.5, 400, 200)
bbtClassReliabilityList.append(bbtcls)


parmDict = {
    'iteration_no': ("Numero Iterazioni", "N", 0, 0),
    'fine':("Progressiva", "m", 0, 0),
    'he':("Quota", "m", 0, 0),
    'hp':("Quota di progetto", "m", 0, 0),
    'co':("Copertura", "m", 0, 0),
    'hw':("Quota Falda", "m", 0, 0),
    'wdepth':("Profondita falda", "m", 0, 0),
    'gamma':("Peso di volume", "kN/mc", 0, 0),
    'sigma':("Resistenza a compressione", "GPa", 0, 0),
    'mi':("Parametro dell'inviluppo di rottura", "-", 0, 0),
    'ei':("Modulo di deformazione", "GPa", 0, 0),
    'cai':("Indice di Abrasivita'", "-", 0, 0),
    'gsi':("GSI", "-", 0, 0),
    'rmr':("RMR", "-", 0, 0),
    'inSituConditionSigmaV':("In-situ Stress", "MPA", 0, 0),
    'rockE':("Young modulus in MPa", "MPA", 0, 0),
    'rockUcs':("UCS", "MPA", 0, 0),
    'pkgl':("Progressiva", "m", 0, 0),
    'closure':("Chiusura a fine scudo", "cm", 0, 40),
    'ldpVlachBegin':("Convergenza al fronte", "cm", 0, 0.1),
    'ldpVlachEnd':("Convergenza a fine scudo", "cm", 0, 0.1),
    'rockburst':("Rockburst", "-", 0, 0.6),
    'front_stability_ns':("xxx", "GPa", 0, 1.2),
    'front_stability_lambda':("Metodo di Panet (Lambda E)", "-", 0, 3.2),
    'penetrationRate':("xxx", "GPa", 0, 0),
    'penetrationRateReduction':("xxx", "GPa", 0, 0),
    'contactThrust':("xxx", "GPa", 0, 0),
    'torque':("xxx", "GPa", 0, 0),
    'frictionForce':("xxx", "GPa", 0, 0),
    'requiredThrustForce':("Required thrust force", "kN", 0, 0),
    'availableThrust':("Available thrust force", "kN", 0, 0),
    'dailyAdvanceRate':("Avanzamento giornaliero", "m/die", 0, 0),
    't1':("Tempo di produzione teorico", "gg", 0, 0),
    't2':("Tempo di montaggio/smontaggio/spostamento", "gg", 0, 0),
    't3':("Extra tempo per scavo in rocce dure", "gg", 0, 0),
    't4':("Tempo apprestamento prospezioni", "gg", 0, 0),
    't5':("Tempo approstamento consolidamenti", "gg", 0, 0),
    'tsum':("Tempo di scavo totale", "gg", 0, 0),
    'adv':("Avanzamento cumulato", "gg", 0, 1400),
    'sigma_ti':("Resistenza a trazione", "GPa", 0, 0),
    'k0':("K0", "-", 0, 0)
}
