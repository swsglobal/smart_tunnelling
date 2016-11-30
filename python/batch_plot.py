# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 18:22:55 2016

@author: aghensi
"""

import readparameters
import strata_summary

# lista di tuple del tipo nomeparmetro, greatherThan, lessThan, threshold
PARAMS_TO_PLOT = [
#    ("front_stability_lambda", False, True, (0.3,), "TEST_5"),
#    ("front_stability_ns", False, False, None, "TEST_5"), #(1, 2, 5)
    ("requiredThrustForce", False, False, None, ""),
#    ("torque", True, False, (30000), "TEST_5"),
#    ("closure", False, False, None, ""),
#    ("contact_on_shield", True, False, (0, ), "TEST_5"),
#    ("overcut_required", True, False, (0, ), "TEST_5"),
#    ("sigma_v_max_front_shield", True, False, (1, ), ""),
#    ("sigma_h_max_front_shield", True, False, (1, ), ""),
#    ("sigma_v_max_lining", True, False, (1,), ""),
#    ("sigma_h_max_lining", True, False, (1,), ""),
#    ("w_in", False, False, None, "TEST_5"),
#    ("dailyAdvanceRate", False, False, None, "TEST_5"),
#    ("rockburst", False, False, None, "TEST_5"),
    ]

for parm in PARAMS_TO_PLOT:
    readparameters.plotparams(sParameterToShow=parm[0], bShowProfile=True, sTbmCode=parm[4], frmt="dxf")
    if parm[1] or parm[2]:
        for threshold in parm[3]:
            readparameters.plotparams(sParameterToShow=parm[0], bShowProfile=True,
                                      greaterThan=parm[1], lessThan=parm[2],
                                      threshold=threshold, sTbmCode=parm[4], frmt="dxf")
strata_summary.get_strata_summary()
