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
        
            #look at name of file/folder
            name = f.split('.')[0]
        
            if name.isdigit():
                
                self.dfgs = self.dfgs + [DFG(path + '/' + f,name)]
            elif name[:2] == 'bg':
                
                self.bgs = self.bgs + [DFG(path + '/' + f,name)]
                
        #sort by name
        self.dfgs.sort(key=lambda x: x.name)
        self.bgs.sort(key=lambda x: x.name)
        
        
        
    def printDFGs(self):
        for dfg in self.dfgs:
            print(dfg.name)
            
    def printBGs(self):
        for bg in self.bgs:
            print(bg.name)
            
    def plotDFGs(self):
        for dfg in self.dfgs:
            plt.figure()
            plt.plot(dfg.wn,dfg.counts)
            plt.title(dfg.name)
            
    def plotBGs(self):
        for bg in self.bgs:
            plt.figure()
            plt.plot(bg.wn,bg.counts)
            plt.title(bg.name)

            
#    def subtractBGs(self):
#        

            
#    def removeSpikes(self):    
#        windowSize = 7
#        medians = pandas.Series(counts).rolling(window = windowSize,center=True).median()
#    
#        
#        #number of nan at beginning and end to replace
#        numRep = math.floor(windowSize/2)
#        
#        #replace beginning and end nan with the first/last computed value
#        for i in range(numRep):
#            medians[i] = medians[numRep]
#            medians[len(medians)-i-1] = medians[len(medians)-numRep-1]
#        
#        #find difference of each point with the median of its window
#        differences = counts-medians
#        
#        
#        #threshold past which if it is further from median it will sense that it is a spike
#        threshold = 200
#        
#        #empty array to hold zero or one if point is a spike
#        spike = np.zeros(len(differences),)
#        for i in range(len(differences)):
#            if differences[i] > threshold:
#                spike[i] = 1
#                print("Spike found at point index",i,"with wavelength",wavelengths[i])
#        
#    
#        
#        #if a peak is found
#        if np.sum(spike) > 0:
#            
#            #read in datafile
#            origFile = open(name,'r')
#            
#            
#            #create new file to put modified
#            newFile = open("temp" + name,"w")
#            
#            
#            #create copy for new corrected array
#            countsCORR = counts.copy()
#        
#            for i in range(len(spike)):
#                
#                singleLine = origFile.readline()
#                
#                
#                #if the point needs to be replaced
#                if spike[i] == 1:
#                    
#                    #check up to five points to the left for the edge or for an ok point
#                    for j in range(5):
#                        if (i-1-j) < 0:
#                            left = [] #if its edge only take from right point
#                            break
#                        else:
#                            if spike[i-1-j] == 0:
#                                left = counts[i-1-j] #or get the first acceptable point
#                                break
#                    
#                    #check up to five points to the right for the edge or for an ok point        
#                    for j in range(5):
#                        if (i+j+1) >= len(spike):
#                            right = [] #if its edge only take from the left point
#                            break
#                        else:
#                            if spike[i+1+j] == 0:
#                                right = counts[i+1+j] #or get the first acceptable point
#                                break
#                    
#                    #get the average of the two or the value if its only one
#                    tempValArray = np.array([])
#                    tempValArray = np.append(tempValArray,left)
#                    tempValArray = np.append(tempValArray,right)
#                    ave = tempValArray.mean()
#                    
#                    #round down to integer number of counts
#                    countsCORR[i] = math.floor(ave)
#                    
#                    #get line from original file, modify
#                    singleLineList = singleLine.split()
#                    singleLineList[3] = str(int(ave))
#                    singleLine = (singleLineList[0] + "\t" + 
#                                  singleLineList[1] + "\t" + 
#                                  singleLineList[2] + "\t" + 
#                                  singleLineList[3] + "\n")
#               
#                #write original or modified line
#                newFile.write(singleLine)
#    
#            
#            
#            #close new file
#            newFile.close()
#            
#            #move original file to preSpikeCorr directory
#            shutil.copy2(name,"preSpikeCorr")
#            
#            #rename the new temp file to the original name
#            os.rename("temp"+name,name)
#            
#            #plot corrected value        
#            plt.plot(wavelengths,countsCORR)
#        else:
#            print("No spikes found")
#        return

            
                
                
