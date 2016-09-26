# -*- coding: utf-8 -*-
from collections import namedtuple

# aghensi@20160922 riorganizzato tuple per una più veloce modifica del codice
strata_pos_fields = ['inizio', 'fine', 'l']
fixed_geoitem_fields = ['geoitem_id', 'perc', 'type', 'title', 'anidrite', 'eff_factor', 'tbm_eff']
var_geoitem_fields = [
    'g_min','g_avg', 'g_max',
    'sigma_ci_min','sigma_ci_avg','sigma_ci_max', #o UCS..
    'mi_min', 'mi_max',
    'mr_min', 'mr_max',
    'ei_min', 'ei_max',
    #'cai_med', 'cai_stdev',
    'gsi_min', 'gsi_max',
    'rmr_min', 'rmr_max',
    #'sigma_ti_min','sigma_ti_max',
    #'k0_min','k0_max',
    "w_in_min", "w_in_max"
    ]
geoitem_fields = strata_pos_fields + fixed_geoitem_fields + var_geoitem_fields
BbtGeoitem = namedtuple('BbtGeoitem', geoitem_fields)

#id=Vertice altimetrico inizio(calcolato)	fine=Progressiva	Est	Nord	he=Quota altimetrica esistente	hp=Progetto quota altimetrica	co=Differenza quota altimetrica	tipo=Tipo di punto
profile_fields = ['profilo_id','inizio','fine','est','nord','he','hp','co','tipo'] #,'wdepth']
BbtProfilo = namedtuple('BbtProfilo', profile_fields)

#unione di profilo e geoitem senza informazioni ridondanti
parameter_fields = profile_fields + fixed_geoitem_fields + var_geoitem_fields
BbtParameter =  namedtuple('BbtParameter', parameter_fields)
# uso questa variabile per la creazione dei georandom
georandom_geoitem_len = len(profile_fields)+len(fixed_geoitem_fields)
# aghensi@20160922 var_to_randomize per creare la namedtuple e generare i valori random
iteration_fields = ['insertdate', 'iteration_no', "tunnelname", "tbmname"]
var_to_randomize = ["g", "sigma_ci", "mi", "mr", "ei", "gsi", "rmr", "w_in"]  #, "mr", "cai", "sigma_ti", "k0"]
output_fields = ['pkgl', 'closure', 'rockburst', 'front_stability_ns', 'front_stability_lambda',
                   'penetrationRate', 'penetrationRateReduction', 'contactThrust', 'torque',
                   'frictionForce', 'requiredThrustForce', 'availableThrust', 'dailyAdvanceRate',
                   't0','t1','t3','t4','t5', 'inSituConditionSigmaV', 'tunnelRadius', 'rockE',\
                   'mohrCoulombPsi', 'rockUcs', 'inSituConditionGsi',
                   'hoekBrownMi', 'hoekBrownD', 'hoekBrownMb', 'hoekBrownS', 'hoekBrownA',
                   'hoekBrownMr', 'hoekBrownSr', 'hoekBrownAr', 'urPiHB', 'rpl', 'picr',
                   'ldpVlachBegin', 'ldpVlachEnd', "sigma_v_max_tail_skin",
                   "sigma_h_max_tail_skin", "sigma_v_max_front_shield", "sigma_h_max_front_shield",
                   "overcut_required", "auxiliary_thrust_required", "consolidation_required",
                   "sigma_h_max_lining", "sigma_v_max_lining", "frictionCoeff"]
par_eval_fields = iteration_fields + profile_fields + fixed_geoitem_fields + var_to_randomize + output_fields
BbtParameterEval =  namedtuple('BbtParameterEval', par_eval_fields)
# tupla utile per lo slicing di range_bbt_parameter per la scrittura sul db
range_bbt_parameter = (len(iteration_fields), len(par_eval_fields)-len(output_fields))

BbtReliability = namedtuple('BbtReliability', ['id', 'inizio','fine','gmr_class','gmr_val','reliability','eval_var'])
BbtParameterEvalMin = namedtuple('BbtParameterEvalMin',['gamma','sigma','mi','ei','cai','rmr', 'gsi','sigma_ti', 'k0' ,'profilo_id'])
#param4seg_fields =  ['inizio', 'fine', 'length', 'he', 'hp', 'co', 'gamma', 'sci', 'mi', 'ei',
#                     'cai', 'gsi', 'rmr', 'profilo_id', 'geoitem_id', 'descr', 'sti', #'k0',
#                     'k0_min', 'k0_max', 'wdepth', 'anidrite']
#BbtParameter4Seg =  namedtuple('BbtParameter4Seg', param4seg_fields)

BbtTbmKpi = namedtuple('BbtTbmKpi',['tunnelName', 'tbmName', 'iterationNo', 'kpiKey', 'kpiDescr',
                                    'minImpact', 'maxImpact', 'avgImpact', 'appliedLength',
                                    'percentOfApplication','probabilityScore','totalImpact'])



def nt_factory(named_tuple):
    def namedtuple_facotry(cursor, row):
        return named_tuple(*row)
    ntf = namedtuple_facotry
    return ntf

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


bbtClassReliabilityList = []
BbtClassReliability = namedtuple('BbtClassReliability',['code','reliability','gmr_min','gmr_max','min_val','max_val'])
bbtcls = BbtClassReliability('A','Buona',7.5,10,50,0)
bbtClassReliabilityList.append(bbtcls)
bbtcls = BbtClassReliability('B','Discreta',5,7.5,100,50)
bbtClassReliabilityList.append(bbtcls)
bbtcls = BbtClassReliability('C','Scarsa',2.5,5,200,100)
bbtClassReliabilityList.append(bbtcls)
bbtcls = BbtClassReliability('D','Non affidabile',0,2.5,400,200)
bbtClassReliabilityList.append(bbtcls)

# TODO: far diventare la descrizione un dizionario con testi in lingue differenti?
parmDict = {
    'iteration_no': ("Numero Iterazioni", "N", 0, 0),
    'fine':("Progressiva", "m", 0, 0),
    'he':("Elevation", "m", 0, 0),
    'hp':("Quota di progetto", "m", 0, 0),
    'co':("Overburden", "m", 0, 0),
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
    'closure':("Closure at shield tail", "mm", 0, 0),
    'ldpVlachBegin':("Convergenza al fronte", "cm", 0, 0.1),
    'ldpVlachEnd':("Convergenza a fine scudo", "cm", 0, 0.1),
    'rockburst':("Rockburst", "-", 0, 0.6),
    'front_stability_ns':("xxx", "GPa", 0, 1.2),
    'front_stability_lambda':("Panet Method (Lambda E)", "-", 0, 3.2),
    'penetrationRate':("Penetration Rate", "mm/min", 0, 0),
    'penetrationRateReduction':("Penetration Rate Reduction", "mm/min", 0, 0),
    'contactThrust':("Contact thrust", "kN", 0, 0),
    'torque':("Torque", "kNm", 0, 0),
    'frictionForce':("Friction Force", "kN", 0, 0),
    'requiredThrustForce':("Required thrust force", "kN", 0, 0),
    'availableThrust':("Available thrust force", "kN", 0, 0),
    'dailyAdvanceRate':("Daily advance rate", "m/die", 0, 0),
    't1':("Tempo di produzione teorico", "gg", 0, 0),
    't2':("Tempo di montaggio/smontaggio/spostamento", "gg", 0, 0),
    't3':("Extra tempo per scavo in rocce dure", "gg", 0, 0),
    't4':("Tempo apprestamento prospezioni", "gg", 0, 0),
    't5':("Tempo apprestamento consolidamenti", "gg", 0, 0),
    'tsum':("Tempo di scavo totale", "gg", 0, 0),
    'adv':("Avanzamento cumulato", "gg", 0, 0),
    'sigma_ti':("Resistenza a trazione", "GPa", 0, 0),
    'k0':("K0", "-", 0, 0),
    'LocFt':("Per-cutter force", 'kN', 0, 0),
    'pvcTubeDiameter': ("dewatering tube diameter - PVC", "m", 0, 0),
    'clsTubeDiameter': ("dewatering tube diameter - concrete", "m", 0, 0),
    'sigma_v_max_tail_skin': ("Pressione verticale sulla tailskin", "MPa", 0, 0),
    'sigma_h_max_tail_skin': ("Pressione orizzontale sulla tailskin", "MPa", 0, 0),
    'sigma_v_max_front_shield': ("Pressione verticale sullo scudo anteriore", "MPa", 0, 0),
    'sigma_h_max_front_shield': ("Pressione orizzontale sullo scudo anteriore", "MPa", 0, 0),
    'overcut_required': ("Overcut richiesto", "", -.1, 1.1),
    'auxiliary_thrust_required': ("Auxiliary Thrust richiesta", "", -.1, 1.1),
    'consolidation_required': ("Consolidamento richiesto", "", -.1, 1.1),
    'sigma_h_max_lining': ("Pressione orizzontale sull'anello", "MPa", 0, 0),
    'sigma_v_max_lining': ("Pressione verticale sull'anello", "MPa", 0, 0),
    "w_in": ("Water inflow", "l/s", 0, 0)
    }