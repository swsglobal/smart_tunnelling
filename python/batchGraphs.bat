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

REM python readparameters.py -p closure
REM python readparameters.py -p contactThrust
REM python readparameters.py -p requiredThrustForce

REM python readparameters.py -p LocFt
REM python readparameters.py -p frictionForce
REM python readparameters.py -p availableThrust
REM python readparameters.py -p dailyAdvanceRate
echo sigma v max tailskin...
python readparameters.py -p sigma_v_max_tail_skin
python readparameters.py -p sigma_v_max_tail_skin -g 0.4
python readparameters.py -p sigma_v_max_tail_skin -g 0.5
python readparameters.py -p sigma_v_max_tail_skin -g 0.6
echo sigma h max tailskin...
python readparameters.py -p sigma_h_max_tail_skin
echo sigma v max front shield...
python readparameters.py -p sigma_v_max_front_shield
python readparameters.py -p sigma_v_max_front_shield -g 0.4
python readparameters.py -p sigma_v_max_front_shield -g 0.5
python readparameters.py -p sigma_v_max_front_shield -g 0.6
echo sigma h max front shield...
python readparameters.py -p sigma_h_max_front_shield
echo sigma v max lining...
python readparameters.py -p sigma_h_max_lining
echo sigma h max lining...
python readparameters.py -p sigma_v_max_lining
python readparameters.py -p sigma_v_max_lining -g 0.4
python readparameters.py -p sigma_v_max_lining -g 0.5
python readparameters.py -p sigma_v_max_lining -g 0.6
REM echo overcut required...
REM python readparameters.py -p overcut_required
REM echo auxiliary thrust required...
REM python readparameters.py -p auxiliary_thrust_required
REM echo consolidation required...
REM python readparameters.py -p consolidation_required
echo Istogrammi Probabilità...
echo Consolidation required...
python readparameters.py -o consolidation_required
echo Overcut required...
python readparameters.py -o overcut_required
echo Auxiliary Thrust required...
python readparameters.py -o auxiliary_thrust_required
echo Fatto.
pause