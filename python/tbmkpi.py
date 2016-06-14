from scipy.stats import triang

from TunnelSegment import PerformanceIndex
from bbtutils import get_my_norm, get_my_norm_min_max
from bbtnamedtuples import BbtTbmKpi, BbtParameter4Seg
from bbt_database import getDBConnection

# danzi.tn@20151113 distribuzione triangolare per friction on Shield e on Cutter Head
# danzi.tn@20151115 recepimento modifiche gabriele

class TriangDist:
    '''
    Crea distribuzione trangolare partendo da tre valori: minimo, media e massimo.

    Per un maggior controllo i valori vengono riordinati automaticamente.
    '''
    def __init__(self, minVal, avgVal, maxVal):
        '''
        aghensi@20160614 - mi assicuro che i valori siano in ordine
        crea la distribuzione triangolare ordinando i parametri di input in modo crescente

        Args:
            * minVal (float): valore minimo
            * avgVal (float): valore medio
            * maxVal (float): valore massimo
        '''
        self.minVal, self.avgVal, self.maxVal = sorted([minVal, avgVal, maxVal])
        self.loc = self.minVal
        self.scale = self.maxVal-self.minVal
        try:
            self.c = (self.avgVal-self.minVal)/(self.maxVal-self.minVal)
        except ZeroDivisionError:
            self.c = 1
        self.triangFunc = triang(self.c, loc=self.loc, scale=self.scale)

    def rvs(self):
        '''
        ritorna un valore random appartenente alla distribuzione

        Returns:
            float - numero random nella distribuzione
        '''
        try:
            return self.triangFunc.rvs()
        except:
            print "errore in TriangDist, minVal={}, maxVal={}, avgVal={}, loc={}, c={}, scale={}". format(self.minVal, self.maxVal, self.avgVal, self.loc, self.c, self.scale)
            return self.avgVal



class KpiTbm4Tunnel:
    kpis = {}
    tbmName = ""
    tunnelName = ""
    bbttbmkpis = []
    iterationNo = 0

    def __init__(self,sTunnelName, iIterationNo):
        self.kpis= {}
        self.tunnelName = sTunnelName
        self.iterationNo = iIterationNo
        # inizializzo i performance index
        #indicatori di produzione (restituiscono un tempo in ore)
        # vanno sommati segmento a segmento
        self.kpis['P1'] = PerformanceIndex('Produzione in condizioni standard') #
        self.kpis['P2'] = PerformanceIndex('Montaggio e smontaggio TBM') #
        self.kpis['P3'] = PerformanceIndex('Avanzamento in rocce dure') #
        self.kpis['P4'] = PerformanceIndex('Preparazione prospezioni')
        self.kpis['P5'] = PerformanceIndex('Preparazione consolidamenti')
        self.kpis['P6'] = PerformanceIndex('Posa rivestimento')

        #indicatori geotecnici (restituiscono un parametro adimensionale che considera tempi, costi e impatti
        # vanno sommati segmento a segmento

        self.kpis['G1'] = PerformanceIndex('Instabilita\' del fronte')
        self.kpis['G2'] = PerformanceIndex('Instabilita\' del cavo')
        self.kpis['G5'] = PerformanceIndex('Splaccaggio calotta')
        self.kpis['G6'] = PerformanceIndex('Cavita\' o faglie')
        self.kpis['G7'] = PerformanceIndex('Venute acqua')
        self.kpis['G8'] = PerformanceIndex('Presenza gas')
        self.kpis['G11'] = PerformanceIndex('Rigonfiamento')
        self.kpis['G12'] = PerformanceIndex('Distacco blocchi al fronte')
        #self.kpis['G13'] = PerformanceIndex('Rockburst')

        #indicatori vari
        self.kpis['V1'] = PerformanceIndex('Ambiente di lavoro')
        self.kpis['V2'] = PerformanceIndex('Costo TBM')
        self.kpis['V3'] = PerformanceIndex('Attrezzaggio per prospezioni')
        self.kpis['V4'] = PerformanceIndex('Deviazione traiettoria')
        self.kpis['V5'] = PerformanceIndex('Integrita\' conci')
        self.kpis['V6'] = PerformanceIndex('Complessita\' TBM')


    def setKPI4TBM(self,alnCurr,tbmName, tbm, projectRefCost):
        self.tbmName = tbmName
        #definisco impatto montaggio e smontaggio
        tProductionMin =alnCurr.length/tbm.maxProduction # tempo minimo di produzione dato applicando la produzione massima a tutta la tratta
        tbm.P2.defineImpact(tProductionMin)
        tbm.P6.defineImpact(tProductionMin, tbm.type,  alnCurr.tbmKey)

        pCur=1.

        iCur=tbm.P2.impact
        #danzi.tn@20151115 recepimento modifiche gabriele
        self.kpis['P2'].updateIndex(0.005, iCur,alnCurr.length)
        self.kpis['P2'].finalizeIndex(alnCurr.length)

        iCur=tbm.P6.impact
        self.kpis['P6'].updateIndex(pCur, iCur, 1.)
        self.kpis['P6'].finalizeIndex(1.)

        iCur=tbm.V1.impact
        self.kpis['V1'].updateIndex(0.005, iCur, alnCurr.length)
        self.kpis['V1'].finalizeIndex(alnCurr.length)

        tbm.V2.defineImpact(projectRefCost)
        iCur=tbm.V2.impact
        self.kpis['V2'].updateIndex(0.005, iCur, alnCurr.length)
        self.kpis['V2'].finalizeIndex( alnCurr.length)

        iCur=tbm.V3.impact
        self.kpis['V3'].updateIndex(1.0, iCur, alnCurr.length)
        self.kpis['V3'].finalizeIndex(alnCurr.length)

        iCur=tbm.V4.impact
        self.kpis['V4'].updateIndex(0.005, iCur, alnCurr.length)
        self.kpis['V4'].finalizeIndex(alnCurr.length)

        iCur=tbm.V5.impact
        self.kpis['V5'].updateIndex(0.005, iCur, alnCurr.length)
        self.kpis['V5'].finalizeIndex(alnCurr.length)

        iCur=tbm.V6.impact
        self.kpis['V6'].updateIndex(0.005, iCur, alnCurr.length)
        self.kpis['V6'].finalizeIndex(alnCurr.length)


    def setKPI4SEG(self,alnCurr, tbmsect, p):
        # aggiorno indici produzione. l'impatto medio dovra' poi essere diviso per la lunghezza del tracciato
        pCur=tbmsect.P1.probability
        iCur=tbmsect.P1.impact
        self.kpis['P1'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.P3.probability
        iCur=tbmsect.P3.impact
        self.kpis['P3'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.P4.probability
        iCur=tbmsect.P4.impact
        self.kpis['P4'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.P5.probability
        iCur=tbmsect.P5.impact
        self.kpis['P5'].updateIndex(pCur, iCur, p.length)

        # aggiorno indici geotecnici
        pCur=tbmsect.G1.probability
        iCur=tbmsect.G1.impact
        self.kpis['G1'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.G2.probability
        iCur=tbmsect.G2.impact
        self.kpis['G2'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.G5.probability
        iCur=tbmsect.G5.impact
        self.kpis['G5'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.G6.probability
        iCur=tbmsect.G6.impact
        #scalo probabilita' in base al tracciato
        prob=0.
        if alnCurr.tbmKey =='CE':
            prob=.2 # classe 4 aftes
        elif alnCurr.tbmKey =='GLNORD':
            prob=.005 #classe 1 aftes perche' noto da cunicolo
        elif alnCurr.tbmKey =='GLSUD':
            prob=.005 #classe 1 aftes perche' noto da cunicolo
        self.kpis['G6'].updateIndex(pCur, iCur, prob*p.length)

        pCur=tbmsect.G7.probability
        iCur=tbmsect.G7.impact
        #scalo probabilita' in base al tracciato
        prob=0.
        if alnCurr.tbmKey =='CE':
            prob=.05 # classe 3 aftes
        elif alnCurr.tbmKey =='GLNORD':
            prob=.005 # drenato dal cunicolo
        elif alnCurr.tbmKey =='GLSUD':
            prob=.005 # drenato dal cunicolo
        self.kpis['G7'].updateIndex(pCur, iCur, prob*p.length)

        pCur=tbmsect.G8.probability
        iCur=tbmsect.G8.impact
        #scalo probabilita' in base al tracciato
        prob=0.
        if alnCurr.tbmKey =='CE':
            prob=.02
        elif alnCurr.tbmKey =='GLNORD':
            prob=.005
        elif alnCurr.tbmKey =='GLSUD':
            prob=0.
        self.kpis['G8'].updateIndex(pCur, iCur, prob*p.length)

        pCur=tbmsect.G11.probability
        iCur=tbmsect.G11.impact
        self.kpis['G11'].updateIndex(pCur, iCur, p.length)

        pCur=tbmsect.G12.probability
        iCur=tbmsect.G12.impact
        self.kpis['G12'].updateIndex(pCur, iCur, p.length)

        #pCur=tbmsect.G13.probability
        #iCur=tbmsect.G13.impact
        #self.kpis['G13'].updateIndex(pCur, iCur, p.length)


    def updateKPI(self, alnCurr):
        self.kpis['P1'].finalizeIndex(alnCurr.length)
        self.kpis['P3'].finalizeIndex(alnCurr.length)
        self.kpis['P4'].finalizeIndex(alnCurr.length)
        self.kpis['P5'].finalizeIndex(alnCurr.length)

        self.kpis['G1'].finalizeIndex(alnCurr.length)
        self.kpis['G2'].finalizeIndex(alnCurr.length)
        self.kpis['G5'].finalizeIndex(alnCurr.length)
        self.kpis['G6'].finalizeIndex(alnCurr.length)
        self.kpis['G7'].finalizeIndex(alnCurr.length)
        self.kpis['G8'].finalizeIndex(alnCurr.length)
        self.kpis['G11'].finalizeIndex(alnCurr.length)
        self.kpis['G12'].finalizeIndex(alnCurr.length)
        #self.kpis['G13'].finalizeIndex(alnCurr.length)


    def getBbtTbmKpis(self):
        bbttbmkpis =[]
        for key in self.kpis:
            _kpi = self.kpis[key]
            bbttbmkpi = BbtTbmKpi(self.tunnelName, self.tbmName,self.iterationNo,key, _kpi.definition, _kpi.minImpact, _kpi.maxImpact, _kpi.avgImpact, _kpi.appliedLength, _kpi.percentOfApplication, _kpi.probabilityScore, _kpi.totalImpact)
            bbttbmkpis.append(bbttbmkpi)
        return bbttbmkpis


    def saveBbtTbmKpis(self,sDBPath):
        bbttbmkpis =[]
        for key in self.kpis:
            _kpi = self.kpis[key]
            bbttbmkpi = BbtTbmKpi(self.tunnelName, self.tbmName,self.iterationNo,key, _kpi.definition, _kpi.minImpact, _kpi.maxImpact, _kpi.avgImpact, _kpi.appliedLength, _kpi.percentOfApplication, _kpi.probabilityScore, _kpi.totalImpact)
            bbttbmkpis.append(bbttbmkpi)
        conn = getDBConnection(sDBPath)

        c = conn.cursor()
        c.execute("DELETE FROM BbtTbmKpi WHERE tunnelName=? AND tbmName=? AND iterationNo=?" , (self.tunnelName,self.tbmName, self.iterationNo))
        conn.commit()
        c.executemany("INSERT INTO BbtTbmKpi (tunnelName,tbmName,iterationNo,kpiKey,kpiDescr,minImpact,maxImpact,avgImpact,appliedLength,percentOfApplication,probabilityScore,totalImpact) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", bbttbmkpis)
        conn.commit()
        conn.close()
        return bbttbmkpis


    def printoutKPI(self):
        for key in self.kpis:
            _kpi = self.kpis[key]
            print '%s;%s;%d;%s;%s;%f;%f;%f;%f;%f;%f;%f' \
                % (self.tunnelName, self.tbmName,self.iterationNo,key, _kpi.definition, _kpi.minImpact, _kpi.maxImpact, _kpi.avgImpact, _kpi.appliedLength, _kpi.percentOfApplication, _kpi.probabilityScore, _kpi.totalImpact)



def build_normfunc_dict(bbt_parameter, nIter=1000):
    return {
        'gamma': get_my_norm(bbt_parameter.g_med, bbt_parameter.g_stddev, 'gamma', nIter),
        'phi': get_my_norm_min_max(bbt_parameter.phimin, bbt_parameter.phimax, 'phi', nIter),
        'ei': get_my_norm(bbt_parameter.ei_med, bbt_parameter.ei_stdev, 'ei', nIter),
        'c': get_my_norm(bbt_parameter.c_med, bbt_parameter.c_stdev, 'c', nIter),
        'rmr': get_my_norm(bbt_parameter.rmr_med, bbt_parameter.rmr_stdev, 'rmr'),
        'k0': get_my_norm_min_max(bbt_parameter.k0_min, bbt_parameter.k0_max, 'k0', nIter),
        'winflow': get_my_norm_min_max(bbt_parameter.w_inflow_min, bbt_parameter.w_inflow_max,
                                       'winflow', nIter),
        'ucs': get_my_norm_min_max(bbt_parameter.UCS_min, bbt_parameter.UCS_max, 'ucs'),
        #gsi = get_my_norm(bbt_parameter.gsi_med, bbt_parameter.gsi_stdev, 'gsi', nIter)
        #sti = get_my_norm_min_max(bbt_parameter.sigma_ti_min, bbt_parameter.sigma_ti_max,
        #                          'sigma_ti', nIter)
        'open_std_eff': TriangDist(bbt_parameter.open_std_eff_min, bbt_parameter.open_std_eff_avg, bbt_parameter.open_std_eff_max),
        'open_bould_eff': TriangDist(bbt_parameter.open_bould_eff_min, bbt_parameter.open_bould_eff_avg, bbt_parameter.open_bould_eff_max),
        'open_water_eff': TriangDist(bbt_parameter.open_water_eff_min, bbt_parameter.open_water_eff_avg, bbt_parameter.open_water_eff_max),
        'open_mixit_eff': TriangDist(bbt_parameter.open_mixit_eff_min, bbt_parameter.open_mixit_eff_avg, bbt_parameter.open_mixit_eff_max),
        'open_tbm_eff': TriangDist(bbt_parameter.open_tbm_eff_min, bbt_parameter.open_tbm_eff_avg, bbt_parameter.open_tbm_eff_max),
        'dual_std_eff': TriangDist(bbt_parameter.dual_std_eff_min, bbt_parameter.dual_std_eff_avg, bbt_parameter.dual_std_eff_max),
        'dual_bould_eff': TriangDist(bbt_parameter.dual_bould_eff_min, bbt_parameter.dual_bould_eff_avg, bbt_parameter.dual_bould_eff_max),
        'dual_water_eff': TriangDist(bbt_parameter.dual_water_eff_min, bbt_parameter.dual_water_eff_avg, bbt_parameter.dual_water_eff_max),
        'dual_mixit_eff': TriangDist(bbt_parameter.dual_mixit_eff_min, bbt_parameter.dual_mixit_eff_avg, bbt_parameter.dual_mixit_eff_max),
        'dual_tbm_eff': TriangDist(bbt_parameter.dual_tbm_eff_min, bbt_parameter.dual_tbm_eff_avg, bbt_parameter.dual_tbm_eff_max)
        }


def build_bbtparameter4seg(bbt_parameter, bbtparametereval):
    return BbtParameter4Seg(bbt_parameter.inizio, bbt_parameter.fine,
                            abs(bbt_parameter.fine - bbt_parameter.inizio),
                            bbt_parameter.he, bbt_parameter.hp, bbt_parameter.co,
                            bbtparametereval.gamma, bbtparametereval.phi, bbtparametereval.ei,
                            bbtparametereval.c, bbtparametereval.rmr, bbt_parameter.profilo_id,
                            bbt_parameter.geoitem_id, bbt_parameter.title, bbtparametereval.k0,
                            bbt_parameter.winflow, bbt_parameter.ucs, bbt_parameter.wdepth,
                            bbt_parameter.k0_min, bbt_parameter.k0_max)


def build_bbtparameterVal4seg(bbt_parameterVal):
    return BbtParameter4Seg(bbt_parameterVal.inizio, bbt_parameterVal.fine,
                            abs(bbt_parameterVal.fine - bbt_parameterVal.inizio),
                            bbt_parameterVal.he, bbt_parameterVal.hp, bbt_parameterVal.co,
                            bbt_parameterVal.gamma, bbt_parameterVal.phi, bbt_parameterVal.ei,
                            bbt_parameterVal.c, bbt_parameterVal.rmr, bbt_parameterVal.profilo_id,
                            bbt_parameterVal.geoitem_id, bbt_parameterVal.title,
                            bbt_parameterVal.k0, bbt_parameterVal.winflow, bbt_parameterVal.ucs,
                            bbt_parameterVal.wdepth, bbt_parameterVal.k0_min,
                            bbt_parameterVal.k0_max, bbt_parameterVal.open_std_eff,
                            bbt_parameterVal.open_bould_eff, bbt_parameterVal.open_water_eff,
                            bbt_parameterVal.open_mixit_eff, bbt_parameterVal.open_tbm_eff,
                            bbt_parameterVal.dual_std_eff, bbt_parameterVal.dual_bould_eff,
                            bbt_parameterVal.dual_water_eff, bbt_parameterVal.dual_mixit_eff,
                            bbt_parameterVal.dual_tbm_eff)


def build_bbtparameter4seg_from_bbt_parameter(bbt_parameter, normfunc_dict):
    return BbtParameter4Seg(bbt_parameter.inizio, bbt_parameter.fine,
                            abs(bbt_parameter.fine - bbt_parameter.inizio),
                            bbt_parameter.he, bbt_parameter.hp, bbt_parameter.co,
                            normfunc_dict['gamma'].rvs(), normfunc_dict['phi'].rvs(),
                            normfunc_dict['ei'].rvs(), normfunc_dict['c'].rvs(),
                            normfunc_dict['rmr'].rvs(), bbt_parameter.profilo_id,
                            bbt_parameter.geoitem_id, bbt_parameter.title,
                            normfunc_dict['k0'].rvs(), normfunc_dict['winflow'].rvs(),
                            bbt_parameter.ucs, bbt_parameter.wdepth, bbt_parameter.k0_min,
                            bbt_parameter.k0_max)
