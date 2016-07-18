# -*- coding: utf-8 -*-
from copy import deepcopy

class TBMConfig:
    # nominalTorque, breakawayTorque, backupDragForce, friction, LDP_type
    # length in m
    # forces in kN
    name=''
    manifacturer=''
    type='' # O = open, S = single shield, DS = double shield
    alignmentCode=''
    shieldLength=0.
    frontShieldLength=0.
    frontShieldDiameter=0.
    tailShieldDiameter=0.
    nominalThrustForce=0.
    auxiliaryThrustForce=0.
    excavationDiameter=0.
    overcut=0.
    loadPerCutter=0.
    totalContactThrust=0.
    cutterSize=0. #diameter
    cutterSpacing=0.
    cutterThickness=0.
    cutterCount=0
    referenceRpm=0.
    nominalTorque=0.
    breakawayTorque=0.
    backupDragForce=0.
    openingRatio=0.
    cutterheadThickness=0.8 # in metri lo spessore della testa di scavo
    dotationForProspection=0. # da 0 a 1 se e' per niente o molto dotata
    weight = 0

tbms={}

#TBM 1
tbm1=TBMConfig()
tbm1.name = 'GL_DS_HRK_10.60_00'
tbm1.alignmentCode='GLSUD;GLNORD'
tbm1.manifacturer='Herrenknecht'
tbm1.type='DS' # O = open, S = single shield, DS = double shield
tbm1.shieldLength=12.05+1.
tbm1.frontShieldLength=4.82+1.
tbm1.frontShieldDiameter=10.60
tbm1.tailShieldDiameter=10.42
tbm1.excavationDiameter=10.66
tbm1.nominalThrustForce=95000.
tbm1.auxiliaryThrustForce=147730. #a velocita' ridotta!
tbm1.overcut=0. #fino a 0.112
tbm1.cutterheadThickness=1. # in metri lo spessore della testa di scavo
tbm1.loadPerCutter=315.
tbm1.cutterSize=19.*0.0254 #diameter
tbm1.cutterSpacing=0.09
tbm1.cutterCount=64
tbm1.totalContactThrust=tbm1.loadPerCutter*tbm1.cutterCount
tbm1.cutterThickness=0.02
tbm1.referenceRpm=3.8
tbm1.nominalTorque=13600.
tbm1.breakawayTorque=30636.
# QUESTI DATI NON CI SONO NELLE SPECIFICHE:
tbm1.weight=1300.*9.81
tbm1.backupDragForce=8000.
tbm1.openingRatio=0.05
tbm1.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
tbms[tbm1.name] = tbm1

#TBM 2
tbm2 = deepcopy(tbm1)
tbm2.name = 'GL_DS_HRK_10.60_03'
tbm2.overcut=0.03
tbms[tbm2.name] = tbm2

#TBM 3
tbm3 = deepcopy(tbm1)
tbm3.name = 'GL_DS_HRK_10.60_06'
tbm3.overcut=0.06
tbms[tbm3.name] = tbm3

#TBM 4
tbm4 = deepcopy(tbm1)
tbm4.name = 'GL_DS_HRK_10.60_09'
tbm4.overcut=0.09
tbms[tbm4.name] = tbm4

#TBM 5
tbm5 = deepcopy(tbm1)
tbm5.name = 'GL_DS_HRK_10.60_112'
tbm5.overcut=0.112
tbms[tbm5.name] = tbm5

#TBM 10 - Documento 092515-2-DS-T-REV5 22 JUNE 2016
tbm10=TBMConfig()
tbm10.name = 'GL_DS_RBS_10.56_00'
tbm10.alignmentCode='GLSUD;GLNORD'
tbm10.manifacturer='Robbins'
tbm10.type='DS' # O = open, S = single shield, DS = double shield
tbm10.excavationDiameter=10.56 # Nord; 10.51 per la sud
tbm10.frontShieldDiameter=10.44
tbm10.tailShieldDiameter=10.32
tbm10.overcut=0. # TODO: creare tutte le varianti
tbm10.shieldLength=11.2+1.
tbm10.frontShieldLength=4.7+1.
tbm10.cutterheadThickness=1. # in metri lo spessore della testa di scavo
tbm10.cutterSize=19.*0.0254 #diameter
tbm10.cutterCount=72
tbm10.cutterSpacing=0.0732
tbm10.loadPerCutter=311.4
tbm10.totalContactThrust=tbm10.cutterCount*tbm10.loadPerCutter
tbm10.nominalThrustForce=69305.
tbm10.auxiliaryThrustForce=171378. #usato Emergency Thrust
tbm10.referenceRpm=2.2 #relativo alla massima Cutterhead Torque
tbm10.nominalTorque=18083. #Cutterhead Torque
tbm10.breakawayTorque=27125. #Exceptional Cutterhead Torque; in low speed ho 40687
tbm10.weight=1300.*9.81
# QUESTI DATI NON CI SONO NELLE SPECIFICHE:
tbm10.cutterThickness=0.02
tbm10.backupDragForce=8000.
tbm10.openingRatio=0.1
tbm10.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata

tbms[tbm10.name] = tbm10

#TBM 11
tbm11 = deepcopy(tbm10)
tbm11.name = 'GL_DS_RBS_10.56_03'
tbm11.overcut=0.03
tbms[tbm11.name] = tbm11

#TBM 12
tbm12 = deepcopy(tbm10)
tbm12.name = 'GL_DS_RBS_10.56_06'
tbm12.overcut=0.06
tbms[tbm12.name] = tbm12

#TBM 13
tbm13 = deepcopy(tbm10)
tbm13.name = 'GL_DS_RBS_10.56_09'
tbm13.overcut=0.09
tbms[tbm13.name] = tbm13

#TBM 14
tbm14 = deepcopy(tbm10)
tbm14.name = 'GL_DS_RBS_10.56_12'
tbm14.overcut=0.12
tbms[tbm14.name] = tbm14


#TBM 1
tbm51=TBMConfig()
tbm51.name = 'CE_DS_HRK_6.82_00'
tbm51.alignmentCode='CE'
tbm51.manifacturer='Herrenknecht'
tbm51.type='DS' # O = open, S = single shield, DS = double shield
tbm51.shieldLength=11.83+1.
tbm51.frontShieldLength=4.59+1.
tbm51.frontShieldDiameter=6.77
tbm51.tailShieldDiameter=6.63
tbm51.excavationDiameter=6.82
tbm51.nominalThrustForce=42750.
tbm51.auxiliaryThrustForce=66350. #a velocita' ridotta!
tbm51.overcut=0. #fino a 0.112
tbm51.cutterheadThickness=1. # spessore della testa di scavo in metri
tbm51.loadPerCutter=315.
tbm51.cutterSize=19.*0.0254 #diameter
tbm51.cutterSpacing=0.09
tbm51.cutterCount=38
tbm51.totalContactThrust=12000
tbm51.cutterThickness=0.02
tbm51.referenceRpm=4.5 # non è reference, è valore medio del range I
tbm51.nominalTorque=5250.
tbm51.breakawayTorque=11800.
# QUESTI DATI NON CI SONO NELLE SPECIFICHE:
tbm51.weight=1300.*9.81
tbm51.backupDragForce=8000.
tbm51.openingRatio=0.05
tbm51.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
tbms[tbm51.name] = tbm51

#tbm52
tbm52 = deepcopy(tbm51)
tbm52.name = 'CE_DS_HRK_6.82_03'
tbm52.overcut=0.03
tbms[tbm52.name] = tbm52

#tbm53
tbm53 = deepcopy(tbm51)
tbm53.name = 'CE_DS_HRK_6.82_06'
tbm53.overcut=0.06
tbms[tbm53.name] = tbm53

#tbm54
tbm54 = deepcopy(tbm51)
tbm54.name = 'CE_DS_HRK_6.82_09'
tbm54.overcut=0.09
tbms[tbm54.name] = tbm54

#tbm55
tbm55 = deepcopy(tbm51)
tbm55.name = 'CE_DS_HRK_6.82_112'
tbm55.overcut=0.112
tbms[tbm55.name] = tbm55


#TBM 23
tbm23=TBMConfig()
tbm23.name = 'CE_DS_RBS_6.73_00'
tbm23.alignmentCode='CE'
tbm23.manifacturer='Robbins'
tbm23.type='DS' # O = open, S = single shield, DS = double shield
tbm23.shieldLength=11.+1.
tbm23.frontShieldDiameter=6.67
tbm23.frontShieldLength=4.3+1.
tbm23.tailShieldDiameter=6.56
tbm23.excavationDiameter=6.73
tbm23.overcut=0. #fino a .12
tbm23.loadPerCutter=311
tbm23.cutterSize=19.*0.0254 #diameter
tbm23.cutterSpacing=0.084
tbm23.cutterThickness=0.02
tbm23.cutterCount=42
tbm23.totalContactThrust=tbm23.loadPerCutter*tbm23.cutterCount
tbm23.referenceRpm=5.4
tbm23.nominalTorque=4632.
tbm23.breakawayTorque=10424.
tbm23.backupDragForce=4000.
tbm23.nominalThrustForce=27630.
tbm23.auxiliaryThrustForce=97205.
tbm23.openingRatio=0.1
tbm23.dotationForProspection=1.
tbm23.cutterheadThickness=1.
tbms[tbm23.name] = tbm23

#tbm24
tbm24 = deepcopy(tbm51)
tbm24.name = 'CE_DS_RBS_6.73_03'
tbm24.overcut=0.03
tbms[tbm24.name] = tbm24

#tbm25
tbm25 = deepcopy(tbm51)
tbm25.name = 'CE_DS_RBS_6.73_06'
tbm25.overcut=0.06
tbms[tbm25.name] = tbm25

#tbm26
tbm26 = deepcopy(tbm51)
tbm26.name = 'CE_DS_RBS_6.73_09'
tbm26.overcut=0.09
tbms[tbm26.name] = tbm26

#tbm27
tbm27 = deepcopy(tbm51)
tbm27.name = 'CE_DS_RBS_6.73_12'
tbm27.overcut=0.12
tbms[tbm27.name] = tbm27