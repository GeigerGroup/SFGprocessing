#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:04:26 2017

Class to hold data for a compilation of DFGs making up a whole spectrum. Methods
in this class make up the majority of processing that occurs. 

The class gets initialized with the path to a folder with a set of DFGs, both
of the sample and of the background. The initializion reads in all of the DFGs,
and seperates them into a list of backgrounds (self.bgs) and actual sample DFGs 
(self.dfgs).

Once an object is created, many methods on it can be called to output details
of the object to the command line, to plot data, to process it, and to write
data to text files to be further worked with or plotted using an individual's
preferred plotting program. 

Description of methods:
    
Print information to output:

-printDFGs(): prints a list of sample DFGs to the output

-printBGs(): prints a list of BG DFGs to the output

Plot data:

-plotDFGs(): creates a plot of all the sample DFGs on one plot

-plotBGs(): creates a plot of all the background DFGs on one plot

-plotIndDFGs(): creates individual plots of each sample DFG

-plotIndBGs(): creates individual plots of each background DFG

-plotFullDFGs(): creates a plot of each DFG that has been padded against the 
full wn array. padDFGs() must have been called prior to calling this.

-plotSumDFGs(): creates a plot of the sum of every padded DFG. sumFullDFGs()
must have been called prior to calling this.

-plotSmoothRawDFGs(): creates a plot of the smoothed and pre-smoothed 
padded DFGs. smoothDFGs() must have been called prior to calling this.

-plotTruncatedDFGs(): creates a plot of the truncated DFGs. A gold reference
spectra must have been created and truncated.

-plotSumTruncatedDFGs(): creates a plot of the sum of the truncated DFGs. 
truncateFullDFGs() must have been called prior to calling this.

Write data to file:
    
-writeDFGs(name): writes each of the individual sample DFGs to a file of the
name specified.

-writeFullDFGs(name): writes each of the fullDFGs that have been padded with
zeros to file. padDFGs() must have been called prior to calling this.

-writeSumDFG(name): writes the sum of the fullDFGs to file. sumFullDFGs() must 
have been called prior to calling this.

-writeSmoothedDFGs(name): writes the smoothed fullDFGs to file. smoothDFGs() 
must have been called prior to calling this.

-writeTruncatedDFGs(name): writes the truncated DFGs to file. A gold reference
spectra must have been created and truncated, and truncateFullDFGs() must have
been called prior to calling this.

-writeSumTruncatedDFG(name): writes the sum of the truncated DFGs to file. 
sumTruncatedDFGs() must have been called prior to calling this.

Processing data:
    
removeCRs(threshold): finds and removes cosmic rays from the sample and background
DFGs. Cosmic rays produce spurious spikes in the spectrum that are 1 or 2 points
wide and frequently outnumber all surrounding points by 100s or 1000s of counts.
By using a rolling median filter, these outlying points are detected and replaced
with the average of the non-outlying points to their immediate left and right. 
The method leaves the lists bgs and dfgs in place and simply replaces the spurious
points.

subtractBGs(): subtracts each background spectrum from the sample spectra.
The method goes through the list of sample DFGs, identifies the correct background
DFG by going through the list and finding the one that is centered around the same
wavelength, and then subtracts the background spectrum from the sample.

padDFGs(): pads each sample DFG with zeros on either side so that each DFG aligns with
the others. This allows them to be plotted against the same array, summed up, etc.
A future iteration could automatically calculate how many zeros to pad on either
side by looking at the wavenumber arrays; currently this number is preset.

sumFullDFGs(): sums up all of the sample DFGs that have been padded with zeros. 
padDFGs() must be called before calling this method. 

smoothDFGs(sigma): smooths the full DFGs using a guassian filter with width sigma,
the default is five and seems to be appropriate to smooth without using significant
resolution. The method copies the pre-smoothed DFGs into another list to save them
and then smooths the DFGs in the list dfgsFull.

findTruncateIndices(threshold): finds the location of where individual DFGs
should be truncated. The threshold determines at what value of the max intensity
the truncation should happen, the default is 0.05 (5%). The method saves these indices
in a list that gets attached the spectrum object, it should only be called on a
gold reference spectrum; that gold reference spectrum is then passed to other
sample spectrum which use the indices created by this method to truncate its
spectra.

truncateFullDFGs(gold): truncates a sample spectrum at the positions determined by
a gold reference spectrum. A gold reference spectrum must exist and have had the
findTruncateIndices() method called on it. This gets passed to the sample spectrum
and its indices are used to truncate the sample spectrum. 

sumTruncatedDFGs(): sums up all of the truncated DFGs. truncateFullDFGs() must
have been called prior to calling this method.

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
    
    def __init__(self,path,shift = 0):
        
        #store path of this sets of DFG positions
        self.path = path
        
        #initialize empty lists for DFGs and backgrounds
        self.dfgs = []
        self.bgs = []
        
        print('Importing DFGs and BGs...')

        #go through each file/directory
        for f in os.listdir(path):
            
            #check if its a .txt file
            if f[-4:] == '.SPE':
                #look at first part of name of text files
                name = f.split('.')[0]
        
                if name.isdigit():
                    #if it is numbers assume it is DFG
                    self.dfgs = self.dfgs + [DFG(path + '/' + f,name)]
                elif name[-2:] == 'bg':
                    #if it ends it bg assume it is a bg
                    self.bgs = self.bgs + [DFG(path + '/' + f,name)]
                
        #sort by name
        self.dfgs.sort(key=lambda x: x.name)
        self.bgs.sort(key=lambda x: x.name)
        
        #create array for fullwn
        fullwn = FullWN()
        
        #give the fullwn array to itself, calibrate
        self.fullwn = fullwn.fullwn - shift
        
        #calibrate dfg wns
        for dfg in self.dfgs:
            dfg.wn = dfg.wn - shift
        
        #calibrate bg wns
        for bg in self.bgs:
            bg.wn = bg.wn - shift
        
        #output the DFGs that have been imported
        print('Has dfgs:')
        self.printDFGs()
        
        #output the background DFGs that have been imported
        print('Has bgs:')
        self.printBGs()
     
        
    #OUTPUT INFO METHODS    
        
    
    #print each sample DFG    
    def printDFGs(self):
        for dfg in self.dfgs:
            print(dfg.name)
    
    #print each background DFG        
    def printBGs(self):
        for bg in self.bgs:
            print(bg.name)
    
    
    #PLOTTING METHODS
    
    
    #plot all sample DFGs   
    def plotDFGs(self):
        plt.figure()
        for dfg in self.dfgs:
            plt.plot(dfg.wn,dfg.counts)  
        plt.title('DFGs')
        plt.show()
            
    #plot all background DFGs           
    def plotBGs(self):
        plt.figure()
        for bg in self.bgs:
            plt.plot(bg.wn,bg.counts)
        plt.title('BGs')
        plt.show()
            
    #plot each sample DFG individually
    def plotIndDFGs(self):     
        for dfg in self.dfgs:
            plt.figure()
            plt.plot(dfg.wn,dfg.counts)
            plt.title(dfg.name)
            plt.show()
    
    #plot each background DFG individually       
    def plotIndBGs(self):        
        for bg in self.bgs:
            plt.figure()
            plt.plot(bg.wn,bg.counts)
            plt.title(bg.name)
            plt.show()
            
    #plot each sample DFG with its associated bg dfg
    def plotDFGandBGsandGold(self,gold):
        for dfg in self.dfgs:
            plt.figure()
            plt.plot(dfg.wn,dfg.counts)
            plt.show()
            
            #identify background by finding median wavelength
            dfgMedian = int(np.median(dfg.wl))
            
            #tracker for seeing if you found background
            foundBG = False
            
            #go through each background, see if one with matching median is there
            for bg in self.bgs:
                if dfgMedian == int(np.median(bg.wl)):
                    print("For dfg",dfg.name,"found",bg.name)
                    plt.plot(bg.wn,bg.counts)
                    foundBG = True
            
            #if one wasn't found, print that        
            if not foundBG:
                print("No bg found for dfg",dfg.name)
                
            #for dfgGold in gold.dfgs:
            #   if dfgMedian == int(np.median(dfgGold.wl)):
            #       plt.plot(dfgGold.wn,dfgGold.counts)
            
            plt.title(dfg.name)
            
    
            
    def plotIndPaddedDFGs(self):
        plt.figure()
        for dfg in self.dfgs:
            plt.plot(dfg.wn,dfg.counts,'b.')
        for dfg in self.dfgsFull:
            plt.plot(self.fullwn,dfg.counts,'r')
        plt.title('Padded and Ind DFGs')
        plt.show()
            
    #plot each DFG that has been padded with zeros against fullwn
    def plotFullDFGs(self):   
        plt.figure()
        for dfg in self.dfgsFull:
            plt.plot(self.fullwn,dfg.counts)  
        plt.title('Padded DFGs')
        plt.show()
        
    #plot each DFG that has been padded with zeros against fullwn
    def plotFullBGs(self):   
        plt.figure()
        for bg in self.bgsFull:
            plt.plot(self.fullwn,bg.counts)  
        plt.title('Padded BGs')
        plt.show()
    
    #plot the sum of all the padded DFGs against fullwn    
    def plotSumDFG(self):
        plt.figure()
        plt.plot(self.fullwn,self.dfgSum)
        plt.title('Sum of DFGs')
        plt.show()
    
    #plot the smoothed and the raw padded DFGs against fullwn    
    def plotSmoothRawDFGs(self):   
        plt.figure()        
        for dfg in self.dfgsPreSmoothed:
            plt.plot(self.fullwn,dfg.counts,'ro')
        plt.show()
            
        for dfg in self.dfgsFull:
            plt.plot(self.fullwn,dfg.counts,'b')
        plt.title('Smoothed and Raw DFGs')
        plt.show()
        
    #plot the DFGs that have been truncated according to the gold reference
    def plotTruncatedDFGs(self):
        plt.figure()
        for dfg in self.dfgsFullTruncated:
            plt.plot(self.fullwn,dfg.counts)  
        plt.title('Truncated DFGs')
        plt.show()
        
    #plot the sum of the truncated DFGs
    def plotSumTruncatedDFG(self):
        plt.figure()
        plt.plot(self.fullwn,self.dfgTruncatedSum)
        plt.title('Sum of truncated DFGs')
        plt.show()
        
        
    #WRITING METHODS
    
    
    #write each individual sample DFG to file
    def writeDFGs(self,name):
        data = np.zeros(444)
        for dfg in self.dfgs:
            data = np.vstack((data,dfg.wn))
            data = np.vstack((data,dfg.counts))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
        
    def writeBGs(self,name):
        data = np.zeros(444)
        for bg in self.bgs:
            data = np.vstack((data,bg.wn))
            data = np.vstack((data,bg.counts))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
    
    #write each padded DFG to file    
    def writeFullDFGs(self,name):
        data = self.fullwn
        for dfg in self.dfgsFull:
            data = np.vstack((data,dfg.counts))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
        
    #write each padded BG to file    
    def writeFullBGs(self,name):
        data = self.fullwn
        for bg in self.bgsFull:
            data = np.vstack((data,bg.counts))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
        
    #write the sum of the padded DFGs to file 
    def writeSumDFG(self,name):
        data = np.vstack((self.fullwn,self.dfgSum))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
    
    #write the smoothed DFGs to file    
    def writeSmoothedDFGs(self,name):
        data = self.fullwn
        for dfg in self.dfgsFull:
            data = np.vstack((data,dfg.counts))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
    
    #write the truncated DFGs to file    
    def writeTruncatedDFGs(self,name):
        data = self.fullwn
        for dfg in self.dfgsFullTruncated:
            data = np.vstack((data,dfg.counts))
        data = data.transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',')
     
    #write the sum of the truncated DFGs to file
    def writeSumTruncatedDFG(self,name):
        print('Truncated, summed wave written to',name)
        data = np.vstack((self.fullwn,self.dfgTruncatedSum)).transpose()
        fmt = '%.5f'
        np.savetxt(name,data,fmt,delimiter=',',header='wn,counts',comments='')
        
        
    #ACTUAL DATA PROCESSING METHODS
    
            
    #remove all cosmic rays for each DFG and BG      
    def removeCRs(self,threshold=200): 
        print('Removing cosmic rays from spectra...')
        
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
            
    #find and subtract correct background        
    def subtractBGs(self):
        
        print('Subtracting BGs from DFGs...')
        
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
    
    #pad each DFG with zeros before and/or after so they align and can be summed up
    def padDFGs(self):
        
        print('Padding DFGs with Zeros...')
        #dictionary to hold number of zeros to pad on either side
        padding = dict(det615=[0,467],det620=[58,409],det625=[116,351],det630=[174,293],
                       det635=[232,235],det640=[290,177],det645=[349,118],
                       det650=[407,60],det655=[467,0])
        
        #length of fullwn is 911
        
        #for 615 add 467 after
        #for 620 add 58 before and 409 after
        #for 625 add 116 before and 351 after
        #for 630 add 174 before and 293 after
        #for 635 add 232 before and 235 after
        #for 640 add 290 before adn 177 after
        #for 645 add 349 before adn 118 after
        #for 655 add 467 before
        
        #copy dfgs into new list
        self.dfgsFull = copy.deepcopy(self.dfgs)
        
        for dfg in self.dfgsFull:
            
            key = 'det' + str(int(np.median(dfg.wl)))
            dfg.counts = np.append(np.append(np.zeros(padding[key][0]),dfg.counts),
                                   np.zeros(padding[key][1]))
            
    #pad each DFG with zeros before and/or after so they align and can be summed up
    def padBGs(self):
        
        print('Padding ΒGs with Zeros...')
        #dictionary to hold number of zeros to pad on either side
        padding = dict(det615=[0,467],det620=[58,409],det625=[116,351],det630=[174,293],
                       det635=[232,235],det640=[290,177],det645=[349,118],det650=[407,60],
                       det655=[467,0])
        
        #length of fullwn is 911
        
        #for 615 add 467 after
        #for 620 add 58 before and 409 after
        #for 625 add 116 before and 351 after
        #for 630 add 174 before and 293 after
        #for 635 add 232 before and 235 after
        #for 640 add 290 before adn 177 after
        #for 645 add 349 before adn 118 after
        #for 655 add 467 before
        
        #copy dfgs into new list
        self.bgsFull = copy.deepcopy(self.bgs)
        
        for bg in self.bgsFull:
            
            key = 'det' + str(int(np.median(bg.wl)))
            bg.counts = np.append(np.append(np.zeros(padding[key][0]),bg.counts),
                                   np.zeros(padding[key][1]))
            
    #sum up the padded DFGs
    def sumFullDFGs(self):
        print('Summing full DFGs...')
        self.dfgSum = np.zeros(911)
        for dfg in self.dfgsFull:
            self.dfgSum = self.dfgSum + dfg.counts
            
    #smooth each DFG with a Gaussian window
    def smoothDFGs(self,sigma=5):
        print('Smoothing DFGs...')
        self.dfgsPreSmoothed = copy.deepcopy(self.dfgsFull)
        
        for dfg in self.dfgsFull:
            #use gaussian filter imported from scipy.ndimage.filters
            dfg.counts = gaussian_filter1d(dfg.counts,sigma)
            
    #find indices of reference spectra where the signal falls off to 5% of max
    def findTruncateIndices(self,threshold=0.05):
        print('Finding truncation thresholds at',threshold,'...')
        #create list to hold indices
        self.truncateIndices = []
        
        #go through each dfg
        for dfg in self.dfgsFull:
            
            #find max
            maxVal = dfg.counts.max()
            
            #find index of the max
            maxIndex = dfg.counts.argmax()
            
            #find left and right indexes
            #set both as zero to start
            leftIndex = []
            rightIndex = []
            
            #go through one half
            for i in np.arange(maxIndex,len(dfg.counts)-1,1):
                #find first point less than threshold and choose
                if dfg.counts[i]-maxVal*threshold < 0:
                    rightIndex = i
                    break
            #if nothing chosen use minimum
            if not rightIndex:
                rightIndex = dfg.counts[maxIndex:].argmin()
            
            #go through other half
            for i in np.arange(maxIndex,0,-1):
                #find first point less than threshold and choose
                if dfg.counts[i]-maxVal*threshold < 0:
                    leftIndex = i
                    break
            if not leftIndex:
                leftIndex = dfg.counts[:maxIndex].argmin()
            
            #add the found values to the list
            self.truncateIndices = self.truncateIndices + [[leftIndex,rightIndex]]
            
    #truncate padded DFGs according to indices set according to gold spectrum
    def truncateFullDFGs(self,gold):
        print('Truncating DFGs...')
        #copy dfgs into new list
        self.dfgsFullTruncated = copy.deepcopy(self.dfgsFull)
        
        #set all the values equal to zero not within the indices determined by
        #the gold reference spectrum
        for i,dfg in enumerate(self.dfgsFullTruncated):       
            dfg.counts[:gold.truncateIndices[i][0]] = 0
            dfg.counts[gold.truncateIndices[i][1]:] = 0
            
    #sum up these truncated DFGs
    def sumTruncatedDFGs(self):
        print('Summing truncated DFGs...')
        self.dfgTruncatedSum = np.zeros(len(self.fullwn))
        
        for dfg in self.dfgsFullTruncated:
            self.dfgTruncatedSum = self.dfgTruncatedSum + dfg.counts