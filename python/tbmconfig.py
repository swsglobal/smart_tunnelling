class TBMConfig:
    # nominalTorque, breakawayTorque, backupDragForce, friction, LDP_type
    # length in m
    # forces in kN
    name=''
    manifacturer=''
    type='' # O = open, S = single shield, DS = double shield
    dstype='' #aghensi@20160614 - O = open, DM = dual mode
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
    weight = 610*9.81 # in kN

tbms={}

#TBM 4
tbm4=TBMConfig()
tbm4.name = 'RBS'
tbm4.alignmentCode='GLEST'
tbm4.manifacturer='Robbins'
tbm4.type='DS' # O = open, S = single shield, DS = double shield
tbm4.dstype='O'
tbm4.shieldLength=12.26
tbm4.frontShieldLength=3.5
tbm4.frontShieldDiameter=5.06
tbm4.tailShieldDiameter=4.98
tbm4.excavationDiameter=5.06
tbm4.overcut=0.04
tbm4.loadPerCutter=267.
tbm4.cutterCount=33
tbm4.cutterSize=17.*0.0254 #diameter
tbm4.cutterSpacing=0.0732
tbm4.cutterThickness=0.02
tbm4.totalContactThrust=tbm4.loadPerCutter*tbm4.cutterCount
tbm4.referenceRpm=11.4
tbm4.nominalTorque=3475.
tbm4.breakawayTorque=5212.
tbm4.backupDragForce=3500.
tbm4.nominalThrustForce=20826.
tbm4.auxiliaryThrustForce=27654.
tbm4.openingRatio=0.075
tbm4.cutterheadThickness=1 # in metri lo spessore della testa di scavo
#tbm4.dotationForProspection=0.75 # da 0 a 1 se e' per niente o molto dotata
tbms[tbm4.name] = tbm4

#TBM 5
tbm5=TBMConfig()
tbm5.name = 'HRK'
tbm5.alignmentCode='GLEST'
tbm5.manifacturer='Herrenknecht'
tbm5.type='DS' # O = open, S = single shield, DS = double shield
tbm5.dstype='O'
tbm5.shieldLength=12.26
tbm5.frontShieldLength=3.5
tbm5.frontShieldDiameter=5.07
tbm5.tailShieldDiameter=5.03
tbm5.excavationDiameter=5.07
tbm5.overcut=0.06
tbm5.loadPerCutter=267.
tbm5.cutterSize=17.*0.0254 #diameter
tbm5.cutterSpacing=0.085
tbm5.cutterThickness=0.02
tbm5.cutterCount=27
tbm5.referenceRpm=11.2
tbm5.totalContactThrust=tbm5.loadPerCutter*tbm5.cutterCount
tbm5.nominalTorque=2097.
tbm5.breakawayTorque=3146.
tbm5.backupDragForce=3500.
tbm5.nominalThrustForce=19704.
tbm5.auxiliaryThrustForce=28952.
tbm5.openingRatio=0.075
tbm5.cutterheadThickness=1. # in metri lo spessore della testa di scavo
#tbm5.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
tbms[tbm5.name] = tbm5

#TBM 6
tbm6=TBMConfig()
tbm6.name = 'SLI'
tbm6.alignmentCode='GLEST'
tbm6.manifacturer='Seli'
tbm6.type='DS' # O = open, S = single shield, DS = double shield
tbm6.dstype='O'
tbm6.shieldLength=11.38
tbm6.frontShieldLength=1.6
tbm6.frontShieldDiameter=5.13
tbm6.tailShieldDiameter=5.04
tbm6.excavationDiameter=5.13
tbm6.overcut=0.07
tbm6.loadPerCutter=267.
tbm6.cutterSize=17.*0.0254 #diameter
tbm6.cutterSpacing=0.08
tbm6.cutterThickness=0.02
tbm6.cutterCount=35
tbm6.referenceRpm=7.
tbm6.totalContactThrust=tbm6.loadPerCutter*tbm6.cutterCount
tbm6.nominalTorque=4981.
tbm6.breakawayTorque=6475.
tbm6.backupDragForce=3500.
tbm6.nominalThrustForce=17700.
tbm6.auxiliaryThrustForce=23266.
tbm6.openingRatio=0.075
tbm6.cutterheadThickness=1. # in metri lo spessore della testa di scavo
#tbm6.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
tbms[tbm6.name] = tbm6

#TBM7
tbm7=TBMConfig()
tbm7.name = 'RBS_DM'
tbm7.alignmentCode='GLEST'
tbm7.manifacturer='Robbins'
tbm7.type='DS' # O = open, S = single shield, DS = double shield
tbm7.dstype='DM'
tbm7.shieldLength=12.26
tbm7.frontShieldLength=3.5
tbm7.frontShieldDiameter=5.06
tbm7.tailShieldDiameter=4.98
tbm7.excavationDiameter=5.06
tbm7.overcut=0.04
tbm7.loadPerCutter=267.
tbm7.cutterCount=33
tbm7.cutterSize=17.*0.0254 #diameter
tbm7.cutterSpacing=0.0732
tbm7.cutterThickness=0.02
tbm7.totalContactThrust=tbm7.loadPerCutter*tbm7.cutterCount
tbm7.referenceRpm=11.4
tbm7.nominalTorque=3475.
tbm7.breakawayTorque=5212.
tbm7.backupDragForce=3500.
tbm7.nominalThrustForce=20826.
tbm7.auxiliaryThrustForce=27654.
tbm7.openingRatio=0.075
tbm7.cutterheadThickness=1 # in metri lo spessore della testa di scavo
#tbm7.dotationForProspection=0.75 # da 0 a 1 se e' per niente o molto dotata
tbms[tbm7.name] = tbm7

#TBM 8
tbm8=TBMConfig()
tbm8.name = 'HRK_DM'
tbm8.alignmentCode='GLEST'
tbm8.manifacturer='Herrenknecht'
tbm8.type='DS' # O = open, S = single shield, DS = double shield
tbm8.dstype='DM'
tbm8.shieldLength=12.26
tbm8.frontShieldLength=3.5
tbm8.frontShieldDiameter=5.07
tbm8.tailShieldDiameter=5.03
tbm8.excavationDiameter=5.07
tbm8.overcut=0.06
tbm8.loadPerCutter=267.
tbm8.cutterSize=17.*0.0254 #diameter
tbm8.cutterSpacing=0.085
tbm8.cutterThickness=0.02
tbm8.cutterCount=27
tbm8.referenceRpm=11.2
tbm8.totalContactThrust=tbm8.loadPerCutter*tbm8.cutterCount
tbm8.nominalTorque=2097.
tbm8.breakawayTorque=3146.
tbm8.backupDragForce=3500.
tbm8.nominalThrustForce=19704.
tbm8.auxiliaryThrustForce=28952.
tbm8.openingRatio=0.075
tbm8.cutterheadThickness=1. # in metri lo spessore della testa di scavo
#tbm8.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
tbms[tbm8.name] = tbm8

#TBM 9
tbm9=TBMConfig()
tbm9.name = 'SLI_DM'
tbm9.alignmentCode='GLEST'
tbm9.manifacturer='Seli'
tbm9.type='DS' # O = open, S = single shield, DS = double shield
tbm9.dstype='DM'
tbm9.shieldLength=11.38
tbm9.frontShieldLength=1.6
tbm9.frontShieldDiameter=5.13
tbm9.tailShieldDiameter=5.04
tbm9.excavationDiameter=5.13
tbm9.overcut=0.07
tbm9.loadPerCutter=267.
tbm9.cutterSize=17.*0.0254 #diameter
tbm9.cutterSpacing=0.08
tbm9.cutterThickness=0.02
tbm9.cutterCount=35
tbm9.referenceRpm=7.
tbm9.totalContactThrust=tbm9.loadPerCutter*tbm9.cutterCount
tbm9.nominalTorque=4981.
tbm9.breakawayTorque=6475.
tbm9.backupDragForce=3500.
tbm9.nominalThrustForce=17700.
tbm9.auxiliaryThrustForce=23266.
tbm9.openingRatio=0.075
tbm9.cutterheadThickness=1. # in metri lo spessore della testa di scavo
#tbm9.dotationForProspection=1. # da 0 a 1 se e' per niente o molto dotata
tbms[tbm9.name] = tbm9