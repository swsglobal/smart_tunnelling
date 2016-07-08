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

tbms={}

#TBM 4
tbm4=TBMConfig()
tbm4.name = 'GL_RBS'
tbm4.alignmentCode='GLSUD'
tbm4.manifacturer='Robbins'
tbm4.type='DS' # O = open, S = single shield, DS = double shield
tbm4.shieldLength=11.3 # non lo trovo
tbm4.frontShieldDiameter=7.01
tbm4.tailShieldDiameter=6.86 # NON LO TROVO
tbm4.excavationDiameter=7.01 # NON LO TROVO
tbm4.overcut=0.03
tbm4.loadPerCutter=311.38
tbm4.cutterCount=45
tbm4.cutterSize=19.*0.0254 #diameter
tbm4.cutterSpacing=0.085 # NON LA TROVO
tbm4.cutterThickness=0.02 # NON LA TROVO
tbm4.totalContactThrust=tbm4.loadPerCutter*tbm4.cutterCount
tbm4.referenceRpm=8.4 #o 4.7?
tbm4.nominalTorque=2631. # a 8.4rpm
tbm4.breakawayTorque=4735. #da 0 a 4.7RPM
tbm4.backupDragForce=400*9.81*0.1 #peso del backup, ok? - troppo elevato, va moltiplicato per il coefficiente di attrito, facciamo 0.1
tbm4.nominalThrustForce=14012.
tbm4.auxiliaryThrustForce=36024.
tbm4.openingRatio=0.075 # NON LA TROVO
tbm4.cutterheadThickness=1 # in metri lo spessore della testa di scavo # NON LA TROVO
tbm4.weight = 575*9.81
tbms[tbm4.name] = tbm4


