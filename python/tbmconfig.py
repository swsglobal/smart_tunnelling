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
    torqueLimits = None
    requiredThrustForceLimits = None
    sigma_v_max_liningLimits = None

tbms={}


#TBM 1
tbm1=TBMConfig()
tbm1.name = 'TEST_5'
tbm1.alignmentCode='GL'
tbm1.manifacturer='Test'
tbm1.type='S' # O = open, S = single shield, DS = double shield
tbm1.shieldLength=14 #aumentato a 1.2 il gap tra scudo e testa, prima era 1.
tbm1.frontShieldLength=14 #1.815+1 #4.82+1.
tbm1.frontShieldDiameter=13.3
tbm1.tailShieldDiameter=13.3
tbm1.excavationDiameter=13.5 #0.09 di conicità
tbm1.overcut=0.05 #fino a .12
tbm1.nominalThrustForce=95000.
tbm1.auxiliaryThrustForce=147730. #a velocita' ridotta!
tbm1.cutterheadThickness=1.2 #1. # in metri lo spessore della testa di scavo
tbm1.loadPerCutter=315.
tbm1.cutterSize=19.*0.0254 #diameter
tbm1.cutterSpacing=0.1
tbm1.cutterCount=90
tbm1.totalContactThrust=tbm1.loadPerCutter*tbm1.cutterCount
tbm1.cutterThickness=0.02
tbm1.referenceRpm=3.8
tbm1.nominalTorque=13600.
tbm1.breakawayTorque=30636.
tbm1.weight=1300.*9.81
tbm1.backupDragForce=8000.
tbm1.openingRatio=0.07
tbm1.dotationForProspection=1.
tbm1.torqueLimits = (10000, 15000)
tbm1.requiredThrustForceLimits = (90000, 150000)
#tbm1.sigma_v_max_liningLimits = (1)

tbms[tbm1.name] = tbm1

tbm2 = deepcopy(tbm1)
tbm2.name = 'TEST_10'
tbm2.overcut=0.10
tbms[tbm2.name] = tbm2

tbm3 = deepcopy(tbm1)
tbm3.name = 'TEST_12'
tbm3.overcut=0.12
tbms[tbm3.name] = tbm3