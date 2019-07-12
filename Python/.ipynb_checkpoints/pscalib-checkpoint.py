#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:42:16 2018

@author: geiger
"""

#import dfg class to hold individual dfg acquisition
from dfg import DFG

#import numpy
import numpy as np

from scipy.optimize import curve_fit
from scipy import exp


#import matplotlib for plotting
import matplotlib.pyplot as plt

class PScalib():
    
    def __init__(self,path):
        
        #store path of file
        self.path = path 
        
        self.dfg = DFG(path,'pscalib')
        
        self.shifts = np.array([0.0,0.0])
        
    def plot(self):
        plt.figure()
        plt.plot(self.dfg.wn,self.dfg.counts)
        plt.xlim([2750,3150])   
        plt.title('PS Calibration')
        plt.show()
        
        
    def fitPeak(self,val1,val2,peak):
        #peak equals 0 or 1, with different theoretical centers
        peakCenters = np.array([2850.3,3060.7])
        
        #indexes for the values entered that bound the peak
        idx1 = (np.abs(self.dfg.wn - val1)).argmin()
        idx2 = (np.abs(self.dfg.wn - val2)).argmin()
        
        #segments within bounds
        xShort = self.dfg.wn[idx2:idx1+1]
        yShort = self.dfg.counts[idx2:idx1+1]
        
        #gaussian function to fit the segment
        def gauss(x,a,x0,sigma,y0):
            return a*exp(-(x-x0)**2/(2*sigma**2))+y0
        
        #initial guesses for the fit                        
        x0 = xShort[int(len(xShort)/2)-1] #guess mean is middle point in range
        #guess width is 25% to 57% of range
        sigma = xShort[int(len(xShort)*(3/4))] - xShort[int(len(xShort)*(1/4))]
        y0 = yShort[0] #guess y0 is first point
        a = y0-yShort[int(len(xShort)/2)] #guess amplitude
        
        #fit 
        popt,pcov = curve_fit(gauss,xShort,yShort,p0=[a,x0,sigma,y0])
        
        #plot with fit and points
        plt.figure()
        plt.plot(self.dfg.wn[idx2-5:idx1+5],self.dfg.counts[idx2-5:idx1+5])
        plt.plot(xShort,gauss(xShort,*popt),'ro:',label='fit')
        plt.plot(self.dfg.wn[idx2],self.dfg.counts[idx2],'o',markersize=5)
        plt.plot(self.dfg.wn[idx1],self.dfg.counts[idx1],'o',markersize=5)
        plt.show()
        
        #set shift for this peak
        self.shifts[peak] = popt[1]-peakCenters[peak]
        
        print('Peak shift from peak',str(peak),'is',"%.2f" % self.shifts[peak])
        
    def evaluateShift(self):
        print('Average shift is ', "%.2f" % np.mean(self.shifts))
        return np.mean(self.shifts)
        
        

        
    
