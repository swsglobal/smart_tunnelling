# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:27:46 2016

@author: aghensi
"""
import bbtnamedtuples
import os

for param, values in bbtnamedtuples.parmDict.iteritems():
    os.system("python readparameters.py -p {}".format(param))