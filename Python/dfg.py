#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:04:26 2017

Class to hold data from a single DFG acquisition in winspec.

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
            
            
        self.wl = wavelengths
        self.counts = counts
        
        self.wn = self.convertWLtoWN(self.wl,795)
        

    def convertWLtoWN(self,wlArray,visWL):
        visWN = 10**7/visWL
        return 10**7/wlArray - visWN