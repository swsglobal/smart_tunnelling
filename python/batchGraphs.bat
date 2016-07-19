@echo off
echo Scatterplot con percentili...
REM python readparameters.py -p gamma
REM python readparameters.py -p sigma
REM python readparameters.py -p mi
REM python readparameters.py -p ei
REM python readparameters.py -p cai
REM python readparameters.py -p gsi
REM python readparameters.py -p rmr
REM python readparameters.py -p inSituConditionSigmaV
REM python readparameters.py -p rockE
REM python readparameters.py -p rockUcs
REM python readparameters.py -p pkgl
REM python readparameters.py -p penetrationRate
REM python readparameters.py -p LocFt


REM python readparameters.py -p closure
REM python readparameters.py -p contactThrust
REM python readparameters.py -p frictionForce
REM python readparameters.py -p requiredThrustForce
REM python readparameters.py -p availableThrust
REM python readparameters.py -p dailyAdvanceRate
echo sigma v max tailskin...
python readparameters.py -p sigma_v_max_tail_skin
echo sigma h max tailskin...
python readparameters.py -p sigma_h_max_tail_skin
echo sigma v max front shield...
python readparameters.py -p sigma_v_max_front_shield
echo sigma h max front shield...
python readparameters.py -p sigma_h_max_front_shield
REM echo overcut required...
REM python readparameters.py -p overcut_required
echo auxiliary thrust required...
python readparameters.py -p auxiliary_thrust_required
echo consolidation required...
python readparameters.py -p consolidation_required
echo sigma v max lining...
python readparameters.py -p sigma_h_max_lining
echo sigma h max lining...
python readparameters.py -p sigma_v_max_lining
REM echo Istogrammi Probabilità...
REM echo Consolidation required...
REM python readparameters.py -o consolidation_required
REM echo Overcut required...
REM python readparameters.py -o overcut_required
REM echo Auxiliary Thrust required...
REM python readparameters.py -o auxiliary_thrust_required
echo Fatto.
pause