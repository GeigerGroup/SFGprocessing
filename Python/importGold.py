#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 19:38:56 2017

@author: pohno
"""

from spectrum import Spectrum

overallpath = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017'

path = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017/goldend'

gold = Spectrum(path)

gold.subtractBGs()

gold.plotDFGs()

gold.plotBGs()

gold.padDFGs()

gold.plotFullDFGs()

gold.smoothDFGs(5)

gold.plotSmoothRawDFGs()

gold.findTruncateIndices()

gold.truncateFullDFGs(gold)

gold.plotTruncatedDFGs()

gold.sumTruncatedDFGs()

gold.plotSumTruncatedDFGs()

import os
os.chdir(overallpath)
gold.writeSumTruncatedWave('goldSummedTruncated.txt')