# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 14:25:35 2016

@author: aghensi
"""
from bbtnamedtuples import BbtParameter4Seg
import tbmconfig
from TunnelSegment import TBM, InfoAlignment, TBMSegment

a = BbtParameter4Seg(inizio=36290.0, fine=36300.0, length=10.0, he=1750.0, hp=777.0, co=973.0,
                     gamma=24.0, sci=15.0, mi=7.0, ei=2.0, cai=-1.0, gsi=30.0, rmr=30.170605961039865,
                     profilo_id=421, geoitem_id=62, descr=u'GA-T-Q-2b', sti=0.0, k0=0.0, k0_min=0.8,
                     k0_max=1.3, wdepth=0.0, anidrite=0.49)
tbm = TBM(tbmconfig.tbms['CE_DS_HRK_6.82_09'], 'V')
alnCurr=InfoAlignment('CE', 'CE', 59305.0 - 27217., 59305.0 - 13290., 0.5, 0.5)

tbmsect = TBMSegment(a, tbm, alnCurr.fiRi, alnCurr.frictionCoeff, 0.25, 0.1)
print(tbmsect)