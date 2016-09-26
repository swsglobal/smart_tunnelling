echo off
echo closure...
python readparameters.py -p closure
rem echo sigma v max tailskin...
rem python readparameters.py -p sigma_v_max_tail_skin
rem python readparameters.py -p sigma_v_max_tail_skin -g 1
rem python readparameters.py -p sigma_v_max_tail_skin -g 1.5
rem python readparameters.py -p sigma_v_max_tail_skin -g 2
echo sigma v max front shield...
python readparameters.py -p sigma_v_max_front_shield
python readparameters.py -p sigma_v_max_front_shield -g 1
python readparameters.py -p sigma_v_max_front_shield -g 1.5
python readparameters.py -p sigma_v_max_front_shield -g 2
echo sigma v max lining...
python readparameters.py -p sigma_v_max_lining
python readparameters.py -p sigma_v_max_lining -g 1
python readparameters.py -p sigma_v_max_lining -g 1.5
python readparameters.py -p sigma_v_max_lining -g 2
echo terminato.
pause