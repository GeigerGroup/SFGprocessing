#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 19:38:56 2017

Script that creates and processes a gold reference spectrum. The outputpath
is the folder where any of the processed files are written out to. The inputpath
is the folder where all of the individual sample and background DFGs are saved.

Various lines can be commented/uncommented to write the data to file and/or
plot it.

1. Initialization imports the individual sample and background DFGs.

2. The appropriate background dfg is subtracted from each sample DFG.

3. Each individual DFG is padded with zeros. This occurs since they are all
horizontally shifted with respect to one another (the whole point of taking 
multiple is to cover more frequency space), so they can be then be summed.

4. These padded DFGs are then summed.

5. They are then smoothed according to a gaussian filter.

6. The positions where the individual files should be truncated is then found.
Gold produces a nonresonant signal, thus the shape of the signal matches the 
shape of the IR beam. For each DFG, the input IR energy does not cover the whole 
detector range. By locating where the IR energy falls off to some value of its 
threshold, we truncate the spectra their to avoid simply summing noise into
our summed spectra at the tails where there is no IR energy to detect anything
anyway.

7. The individual DFGs are then truncated according to these positions.

8. These truncated DFGs are then summed.
                        
@author: pohno
"""

from spectrum import Spectrum

import os

#path to where files are written to
outputpath = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017'

#path where the data is stored
inputpath = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017/goldend'

#create object, loads each sample and background DFG
gold = Spectrum(inputpath)

#change directory in case files are written 
os.chdir(outputpath)

#subtract the appropriate background DFG from each sample DFG
gold.subtractBGs()

#plot the imported sample DFGs
gold.plotDFGs()

#plot the imported background DFGs
gold.plotBGs()

#write background subtracted DFGs to file
#gold.writeDFGs('goldIndDFGs.txt')

#pad the dfgs with zeros so they align and can be summed up
gold.padDFGs()

#write padded DFGs to file
#gold.writeFullDFGs('goldFullDFGs.txt')

#plot the full DFGs
gold.plotFullDFGs()

#sum the padded DFGs
gold.sumFullDFGs()

#write sum of padded DFGs to file
#gold.writeSumDFG('goldSumDFG.txt')

#smooth the DFGs with a gaussian filter
gold.smoothDFGs(5)

#write smoothed padded DFGs to file
#gold.writeSmoothedDFGs('goldSmoothedDFGs.txt')

#plot the smoothed and raw DFGs
gold.plotSmoothRawDFGs()

#find the indices of where the reference signal falls off to guide truncation
gold.findTruncateIndices()

#truncate 
gold.truncateFullDFGs(gold)

#write smoothed, padded, truncated DFGs to file
#gold.writeTruncatedDFGs('goldTruncatedDFGs.txt')

#plot the truncated DFGs
gold.plotTruncatedDFGs()

#sum the truncated DFGs
gold.sumTruncatedDFGs()

#plot the summed, truncated DFGS
gold.plotSumTruncatedDFG()

#write final summed, smoothed, padded, truncated spectrum to file
#gold.writeSumTruncatedDFG('goldSumTruncated.txt')