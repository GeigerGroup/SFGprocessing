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

import os
os.chdir(overallpath)

gold.subtractBGs()

gold.plotDFGs()

gold.plotBGs()

#uncomment to write background subtracted DFGs to file
#gold.writeDFGs('goldIndDFGs.txt')

gold.padDFGs()

#uncomment to write padded DFGs to file
#gold.writePaddedDFGs('goldPaddedDFGs.txt')

gold.plotFullDFGs()

gold.sumFullDFGs()

#uncomment to write sum of padded DFGs to file
#gold.writeSummedDFGs('goldSummedDFGs.txt')

gold.smoothDFGs(5)

#uncomment to write smoothed padded DFGs to file
#gold.writeSmoothedDFGs('goldSmoothedDFGs.txt')

gold.plotSmoothRawDFGs()

gold.findTruncateIndices()

gold.truncateFullDFGs(gold)

#uncomment to write smoothed, padded, truncated DFGs to file
#gold.writeTruncatedDFGs('goldTruncatedDFGs.txt')

gold.plotTruncatedDFGs()

gold.sumTruncatedDFGs()

gold.plotSumTruncatedDFGs()

#write final summed, smoothed, padded, truncated spectrum to file
gold.writeSumTruncatedWave('goldSummedTruncated.txt')