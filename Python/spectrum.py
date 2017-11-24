#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:04:26 2017

Class to hold data for a compilation of DFGs making up a whole spectrum.

@author: pohno
"""
#import os to get list of files
import os

#import dfg class to hold individual dfg acquisition
from dfg import DFG

#import matplotlib for plotting
import matplotlib.pyplot as plt

#import pandas for rolling median function
import pandas

#import numpy
import numpy as np

#import math
import math

#import fullwn array
from fullwn import FullWN

#import scipy 
from scipy.ndimage.filters import gaussian_filter1d

#import copy for deep copying
import copy

class Spectrum():
    
    def __init__(self,path):
        
        #store path of this sets of DFG positions
        self.path = path
        
        #initialize empty lists for DFGs and backgrounds
        self.dfgs = []
        self.bgs = []
        
        #change the directory to the specified directory
        os.chdir(path)

        #go through each file/directory
        for f in os.listdir():
            
            #check if its a .txt file
            if f[-4:] == '.txt':
                #look at name of file/folder
                name = f.split('.')[0]
        
                if name.isdigit():
                
                    self.dfgs = self.dfgs + [DFG(path + '/' + f,name)]
                elif name[-2:] == 'bg':
                
                    self.bgs = self.bgs + [DFG(path + '/' + f,name)]
                
        #sort by name
        self.dfgs.sort(key=lambda x: x.name)
        self.bgs.sort(key=lambda x: x.name)
        
        #create array for fullwn
        fullwn = FullWN()
        
        self.fullwn = fullwn.fullwn
        
        
    #print each DFG    
    def printDFGs(self):
        for dfg in self.dfgs:
            print(dfg.name)
    
    #print each BG        
    def printBGs(self):
        for bg in self.bgs:
            print(bg.name)
    
    #plot each DFG        
    def plotDFGs(self):
        plt.figure()
        for dfg in self.dfgs:
            plt.plot(dfg.wn,dfg.counts)          
            
    def plotIndDFGs(self):     
        for dfg in self.dfgs:
            plt.figure()
            plt.plot(dfg.wn,dfg.counts)
            plt.title(dfg.name)
         
    #plot each BG            
    def plotBGs(self):
        plt.figure()
        for bg in self.bgs:
            plt.plot(bg.wn,bg.counts)
            
    def plotIndBGs(self):        
        for bg in self.bgs:
            plt.figure()
            plt.plot(bg.wn,bg.counts)
            plt.title(bg.name)
            
                
    def plotDFGsum(self):
        plt.figure()
        plt.plot(self.fullwn,self.dfgSum)
        
    def plotFullDFGs(self):
        
        plt.figure()
        for dfg in self.dfgsFull:
            plt.plot(self.fullwn,dfg.counts)
            
            
    def plotSmoothRawDFGs(self):
        
        plt.figure()

            
        for dfg in self.dfgsFull:
            plt.plot(self.fullwn,dfg.counts,'ro')
            
        for dfg in self.dfgsSmoothedFull:
            plt.plot(self.fullwn,dfg.counts,'b')
        
        

    #find and subtract correct background        
    def subtractBGs(self):
        
        #create list to hold pre-bg subtracted dfgs
        self.dfgsRaw = copy.deepcopy(self.dfgs)
        
        #go through each dfg
        for dfg in self.dfgs:
            
            #identify background by finding median wavelength
            dfgMedian = int(np.median(dfg.wl))
            
            #tracker for seeing if you found background
            foundBG = False
            
            #go through each background, see if one with matching median is there
            for bg in self.bgs:
                if dfgMedian == int(np.median(bg.wl)):
                    print("For dfg",dfg.name,"found",bg.name)
                    dfg.counts = dfg.counts - bg.counts
                    foundBG = True
            
            #if one wasn't found, print that        
            if not foundBG:
                print("No bg found for dfg",dfg.name)
                   
            
            
    def smoothDFGs(self,sigma=5):
        self.dfgsSmoothedFull = copy.deepcopy(self.dfgsFull)
        
        for dfg in self.dfgsSmoothedFull:
            dfg.counts = gaussian_filter1d(dfg.counts,sigma)
    
    def findTruncateIndices(self,threshold=0.05):
        
        #create list to hold indices
        self.truncateIndices = []
        
        #go through each dfg
        for dfg in self.dfgsSmoothedFull:
            
            #find max
            maxVal = dfg.counts.max()
            
            #find index of the max
            maxIndex = dfg.counts.argmax()
            
            #find left and right indexes
            leftIndex = (np.abs(dfg.counts[:maxIndex] - maxVal*threshold)).argmin()
            rightIndex = maxIndex+(np.abs(dfg.counts[maxIndex:] - maxVal*threshold)).argmin()
            
            #add the found values to the list
            self.truncateIndices = self.truncateIndices + [[leftIndex,rightIndex]]
            
    def truncateFullDFGs(self):
        for i,dfg in enumerate(self.dfgsSmoothedFull):
            
            dfg.counts[:self.truncateIndices[i][0]] = 0
            dfg.counts[self.truncateIndices[i][1]:] = 0
            
    def plotTruncatedDFGs(self):
        plt.figure()
        for dfg in self.dfgsSmoothedFull:
            plt.plot(self.fullwn,dfg.counts,'b')
        
            

    #remove all CRs for each         
    def removeCRs(self,threshold=200):

        #function that uses a median filter to identify a CR in a single DFG
        def removeCRindDFG(dfg,threshold):
            
            #choose how big of a window for the rolling median
            windowSize = 7
            medians = pandas.Series(dfg.counts).rolling(window = windowSize,center=True).median()
                    
            #number of nan at beginning and end to replace
            numRep = math.floor(windowSize/2)
            
            #replace beginning and end nan with the first/last computed value
            for i in range(numRep):
                medians[i] = medians[numRep]
                medians[len(medians)-i-1] = medians[len(medians)-numRep-1]
            
            #find difference of each point with the median of its window
            differences = dfg.counts-medians
            
            
            #empty array to hold zero or one if point is a spike
            spike = np.zeros(len(differences),)
            for i in range(len(differences)):
                if differences[i] > threshold:
                    spike[i] = 1
                    print("Spike found at point index",i,"with wavenumber",dfg.wn[i],"cm^-1")
                  
            #if there any spikes found
            if np.sum(spike) > 0:
                
                #go through and replace the spike with the average on both sides
                for i in range(len(spike)):          
                    
                    #if the point needs to be replaced
                    if spike[i] == 1:
                        
                        #check up to five points to the left for the edge or for an ok point
                        for j in range(5):
                            if (i-1-j) < 0:
                                left = [] #if its edge only take from right point
                                break
                            else:
                                if spike[i-1-j] == 0:
                                    left = dfg.counts[i-1-j] #or get the first acceptable point
                                    break
                        
                        #check up to five points to the right for the edge or for an ok point        
                        for j in range(5):
                            if (i+j+1) >= len(spike):
                                right = [] #if its edge only take from the left point
                                break
                            else:
                                if spike[i+1+j] == 0:
                                    right = dfg.counts[i+1+j] #or get the first acceptable point
                                    break
                        
                        #get the average of the two or the value if its only one
                        tempValArray = np.array([])
                        tempValArray = np.append(tempValArray,left)
                        tempValArray = np.append(tempValArray,right)
                        ave = tempValArray.mean()
                        
                        #round down to integer number of counts
                        dfg.counts[i] = math.floor(ave)
            else:
                print("No spikes found in " + dfg.name)
            return
        
        #go through each dfg and remove CRs
        for dfg in self.dfgs:
            removeCRindDFG(dfg,threshold)
             
        #go through each bg and remove CRs
        for bg in self.bgs:
            removeCRindDFG(bg,threshold)
            
    def padDFGs(self):
        
        #dictionary to hold number of zeros to pad on either side
        padding = dict(det620=[0,409],det625=[58,351],det630=[116,293],
                       det635=[174,235],det640=[232,177],det645=[291,118],
                       det655=[409,0])
        #for 620 add 409 after
        #for 625 add 58 before and 351 after
        #for 630 add 116 before and 293 after
        #for 635 add 174 before and 235 after
        #for 640 add 232 before and 177 after
        #for 645 add 291 before and 118 after
        #for 655 add 409 before
        
        #copy dfgs into new list
        self.dfgsFull = copy.deepcopy(self.dfgs)
        
        for dfg in self.dfgsFull:
            
            key = 'det' + str(int(np.median(dfg.wl)))
            dfg.counts = np.append(np.append(np.zeros(padding[key][0]),dfg.counts),
                                   np.zeros(padding[key][1]))

        

            
    def sumDFGs(self):
        
        self.dfgSum = np.zeros(853)
        
        for dfg in self.dfgsFull:
            self.dfgSum = self.dfgSum + dfg.counts

            
        
    

            
                
                
