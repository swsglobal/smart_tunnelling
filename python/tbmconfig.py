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

#TBM 3
tbm3 = deepcopy(tbm1)
tbm3.name = 'GL_DS_HRK_10.60_09'
tbm3.overcut=0.09
tbms[tbm3.name] = tbm3

#TBM 4
tbm4 = deepcopy(tbm1)
tbm4.name = 'GL_DS_HRK_10.60_112'
tbm4.overcut=0.112
tbms[tbm4.name] = tbm4

#TBM 8
#tbm8=TBMConfig()
#tbm8.name = 'CE_DS_HRK_6.82'
#tbm8.alignmentCode='CE'
#tbm8.manifacturer='Herrenknecht'
#tbm8.type='DS' # O = open, S = single shield, DS = double shield
#tbm8.shieldLength=11.695 + .9
#tbm8.frontShieldDiameter=6.77
#tbm8.frontShieldLength=4.595+.9
#tbm8.tailShieldDiameter=6.65
#tbm8.excavationDiameter=6.82
#tbm8.overcut=0.12
#tbm8.loadPerCutter=315.
#tbm8.cutterSize=19.*0.0254 #diameter
#tbm8.cutterSpacing=0.085
#tbm8.cutterThickness=0.02
#tbm8.cutterCount=39
#tbm8.totalContactThrust=tbm8.loadPerCutter*tbm8.cutterCount
#tbm8.referenceRpm=5.
#tbm8.nominalTorque=5250.
#tbm8.breakawayTorque=11800.
#tbm8.backupDragForce=4000.
#tbm8.nominalThrustForce=35539.
#tbm8.auxiliaryThrustForce=60236.
#tbm8.openingRatio=0.05
#tbm8.dotationForProspection=0.75 # da 0 a 1 se e' per niente o molto dotata
#tbm8.cutterheadThickness=0.9
#tbms[tbm8.name] = tbm8

#TBM 10 - Documento 092515-2-DS-T-REV5 22 JUNE 2016
#tbm10=TBMConfig()
#tbm10.name = 'GL_DS_RBS_10.56_00'
#tbm10.alignmentCode='GLSUD;GLNORD'
#tbm10.manifacturer='Robbins'
#tbm10.type='DS' # O = open, S = single shield, DS = double shield
#tbm10.excavationDiameter=10.56 # Nord; 10.51 per la sud
#tbm10.frontShieldDiameter=10.44
#tbm10.tailShieldDiameter=10.32
#tbm10.overcut=0. # TODO: creare tutte le varianti
#tbm10.shieldLength=11.2+1.
#tbm10.frontShieldLength=4.7+1.
#tbm10.cutterheadThickness=1. # in metri lo spessore della testa di scavo
#tbm10.cutterSize=19.*0.0254 #diameter
#tbm10.cutterCount=72
#tbm10.cutterSpacing=0.0732
#tbm10.loadPerCutter=311.4
#tbm10.totalContactThrust=tbm10.cutterCount*tbm10.loadPerCutter
#tbm10.nominalThrustForce=69305.
#tbm10.auxiliaryThrustForce=171378. #usato Emergency Thrust
#tbm10.referenceRpm=2.2 #relativo alla massima Cutterhead Torque
#tbm10.nominalTorque=18083. #Cutterhead Torque
#tbm10.breakawayTorque=27125. #Exceptional Cutterhead Torque; in low speed ho 40687
#tbm10.weight=1300.*9.81
## QUESTI DATI NON CI SONO NELLE SPECIFICHE:
#tbm10.cutterThickness=0.02
#tbm10.backupDragForce=8000.
#tbm10.openingRatio=0.1
#tbm10.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
#
#tbms[tbm10.name] = tbm10
#
##TBM 11
#tbm11 = deepcopy(tbm10)
#tbm11.name = 'GL_DS_RBS_10.56_03'
#tbm11.overcut=0.03
#tbms[tbm11.name] = tbm11
#
##TBM 12
#tbm12 = deepcopy(tbm10)
#tbm12.name = 'GL_DS_RBS_10.56_06'
#tbm12.overcut=0.06
#tbms[tbm12.name] = tbm12
#
##TBM 13
#tbm13 = deepcopy(tbm10)
#tbm13.name = 'GL_DS_RBS_10.56_09'
#tbm13.overcut=0.09
#tbms[tbm13.name] = tbm13
#
##TBM 14
#tbm14 = deepcopy(tbm10)
#tbm14.name = 'GL_DS_RBS_10.56_12'
#tbm14.overcut=0.12
#tbms[tbm14.name] = tbm14

#TBM 23
#tbm23=TBMConfig()
#tbm23.name = 'CE_DS_RBS_6.73'
#tbm23.alignmentCode='CE'
#tbm23.manifacturer='Robbins'
#tbm23.type='DS' # O = open, S = single shield, DS = double shield
#tbm23.shieldLength=11.+1.
#tbm23.frontShieldDiameter=6.67
#tbm23.frontShieldLength=4.3+1.
#tbm23.tailShieldDiameter=6.56
#tbm23.excavationDiameter=6.73
#tbm23.overcut=0.12
#tbm23.loadPerCutter=311.4
#tbm23.cutterSize=19.*0.0254 #diameter
#tbm23.cutterSpacing=0.087
#tbm23.cutterThickness=0.02
#tbm23.cutterCount=42
#tbm23.totalContactThrust=tbm23.loadPerCutter*tbm23.cutterCount
#tbm23.referenceRpm=5.4
#tbm23.nominalTorque=4053.
#tbm23.breakawayTorque=14034.
#tbm23.backupDragForce=4000.
#tbm23.nominalThrustForce=27630.
#tbm23.auxiliaryThrustForce=97205.
#tbm23.openingRatio=0.1
#tbm23.dotationForProspection=1.
#tbm23.cutterheadThickness=1.
#tbms[tbm23.name] = tbm23
