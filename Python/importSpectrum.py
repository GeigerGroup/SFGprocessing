#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 20:45:30 2017

@author: pohno
"""

from spectrum import Spectrum

overallpath = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017'

name = 'flowrun2.txt'
path = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017/caf2_water/run2'

spec = Spectrum(path)

import os
os.chdir(overallpath)

spec.plotDFGs()

spec.plotBGs()

spec.removeCRs(50)

spec.plotDFGs()

spec.plotBGs()

spec.subtractBGs()

spec.plotDFGs()

spec.padDFGs()

spec.plotFullDFGs()

spec.sumFullDFGs()

#uncomment to write sum of padded DFGs to file
spec.writeSummedDFGs('flowrun2Raw.txt')

spec.plotSumDFGs()

spec.truncateFullDFGs(gold)

spec.plotTruncatedDFGs()

spec.sumTruncatedDFGs()

spec.plotSumTruncatedDFGs()

spec.writeSumTruncatedWave(name)