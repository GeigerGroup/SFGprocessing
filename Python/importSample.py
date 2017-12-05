#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 20:45:30 2017

Script that creates and processes a sample spectrum. The overallpath
is the folder where any of the processed files are written out to. The path
is the folder where all of the individual sample and background DFGs are saved.

Various lines can be commented/uncommented to write the data to file and/or
plot it.

1. Initialization imports the individual sample and background DFGs.

2. Any cosmic rays are removed from the sample or background DFGs (see header of 
spectrum.py for details)

3. The appropriate background dfg is subtracted from each sample DFG.

4. Each individual DFG is padded with zeros. This occurs since they are all
horizontally shifted with respect to one another (the whole point of taking 
multiple is to cover more frequency space), so they can be then be summed.

5. These padded DFGs are then summed.

6. The individual DFGs are then truncated according to the positions determined
by the gold reference.

7. These truncated DFGs are then summed.

@author: pohno
"""

from spectrum import Spectrum

import os

#path to where files are written to
overallpath = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017'

#name where summedTruncatedData is written to
name = 'flowrun2.txt'

#path where the data is stored
path = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017/caf2_water/run2'

#create object, loads each sample and background DFG
spec = Spectrum(path)

#change directory in case files are written 
os.chdir(overallpath)

#plot pre cosmic ray removal
spec.plotDFGs()
spec.plotBGs()

#remove cosmic rays
spec.removeCRs(50)

#plot after cosmic ray removal
spec.plotDFGs()
spec.plotBGs()

#change directory in case files are written 
spec.subtractBGs()

#plot after background subtraction
spec.plotDFGs()

#pad the dfgs with zeros so they align and can be summed up
spec.padDFGs()

#plot the full DFGs
spec.plotFullDFGs()

#sum the padded DFGs
spec.sumFullDFGs()

#write sum of padded DFGs to file
#spec.writeSumDFG('flowrun2Raw.txt')

#plot the sum of the DFGs
spec.plotSumDFG()

#truncate the DFGs according to the gold reference spectrum
spec.truncateFullDFGs(gold)

#plot the truncated DFGs
spec.plotTruncatedDFGs()

#summ the truncated DFGs
spec.sumTruncatedDFGs()

#plot the summed, truncated spectrum
spec.plotSumTruncatedDFG()

#write the summed, truncated spectrum to file
spec.writeSumTruncatedDFG(name)