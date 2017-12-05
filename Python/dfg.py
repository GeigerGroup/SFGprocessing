#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:04:26 2017

Class to hold data from a single DFG acquisition. A set of DFGs may or may not
make up a full spectrum from spectrum.py. 

DFG stands for 'difference frequency generation'. When collecting a broad SFG 
vibrational spectrum, the IR wavelength and detector wavelength need to be 
shifted across frequency space as they are too narrow to do everything at one 
time. The IR wavelength is shifted by changing the position of something called 
the DFG crystal, hence the name of a single one of these acquisitions.

The name property holds the name of the file. The wl property is an array of 
the wavelength values that are read in. The counts property is the number of 
photons that are read in. The wn property is the wl array converted to wavelengths.

@author: pohno
"""

#import numpy
import numpy as np

class DFG():
    
    def __init__(self,path,name):
        
        #add name
        self.name = name
        
        #read in file
        file = open(path,'r')
        
        #initialize array for wavelengths and counts
        wavelengths = np.array([])
        counts = np.array([])
        
        #go through each line in datafile and append to arrays
        for line in file:
            fields = line.split()
            wavelengths = np.append(wavelengths,[float(fields[0])])
            counts = np.append(counts,[float(fields[3])])
            
        #set attributes of object    
        self.wl = wavelengths
        self.counts = counts
        
        #convert wavelength values to wavenumber
        self.wn = self.convertWLtoWN(self.wl,795)
        
    #function to convert wavelength values to wavenumber based on upconvert wl
    def convertWLtoWN(self,wlArray,visWL):
        visWN = 10**7/visWL
        return 10**7/wlArray - visWN
    
    