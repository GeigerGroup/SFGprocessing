# -*- coding: utf-8 -*-
"""
This script searches a directory and reads in the ASCII data files produced by 
WinSpec, corrects for cosmic ray spikes with a rolling median filter, and 
replaces the original file with the updated file if spikes are found. 
The original file is placed in a new directory called preSpikeCorr
"""
#import os
import os

#Set directory here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
os.chdir("/Users/pohno/Box Sync/Science/Data/SFG/Solstice/10162017/Low Salt/run2")

#import numpy for array functionality
import numpy as np

#import shutil for moving and copying files
import shutil

#import pandas for rolling median function
import pandas

#import matplotlib for plotting
import matplotlib.pyplot as plt

#import math for floor
import math

def correctSpectrum(name):

    
    #read in datafile
    origFile = open(name,'r')
    
    #initialize array for wavelengths and counts
    wavelengths = np.array([])
    counts = np.array([])
    
    #go through each line in datafile and append to arrays
    for line in origFile:
        fields = line.split()
        wavelengths = np.append(wavelengths,[float(fields[0])])
        counts = np.append(counts,[float(fields[3])])
    

    plt.figure()
    
    #plot
    plt.plot(wavelengths,counts)

    windowSize = 7
    medians = pandas.Series(counts).rolling(window = windowSize,center=True).median()

    
    #number of nan at beginning and end to replace
    numRep = math.floor(windowSize/2)
    
    #replace beginning and end nan with the first/last computed value
    for i in range(numRep):
        medians[i] = medians[numRep]
        medians[len(medians)-i-1] = medians[len(medians)-numRep-1]
    
    #find difference of each point with the median of its window
    differences = counts-medians
    
    
    #threshold past which if it is further from median it will sense that it is a spike
    threshold = 200
    
    #empty array to hold zero or one if point is a spike
    spike = np.zeros(len(differences),)
    for i in range(len(differences)):
        if differences[i] > threshold:
            spike[i] = 1
            print("Spike found at point index",i,"with wavelength",wavelengths[i])
    

    
    #if a peak is found
    if np.sum(spike) > 0:
        
        #read in datafile
        origFile = open(name,'r')
        
        
        #create new file to put modified
        newFile = open("temp" + name,"w")
        
        
        #create copy for new corrected array
        countsCORR = counts.copy()
    
        for i in range(len(spike)):
            
            singleLine = origFile.readline()
            
            
            #if the point needs to be replaced
            if spike[i] == 1:
                
                #check up to five points to the left for the edge or for an ok point
                for j in range(5):
                    if (i-1-j) < 0:
                        left = [] #if its edge only take from right point
                        break
                    else:
                        if spike[i-1-j] == 0:
                            left = counts[i-1-j] #or get the first acceptable point
                            break
                
                #check up to five points to the right for the edge or for an ok point        
                for j in range(5):
                    if (i+j+1) >= len(spike):
                        right = [] #if its edge only take from the left point
                        break
                    else:
                        if spike[i+1+j] == 0:
                            right = counts[i+1+j] #or get the first acceptable point
                            break
                
                #get the average of the two or the value if its only one
                tempValArray = np.array([])
                tempValArray = np.append(tempValArray,left)
                tempValArray = np.append(tempValArray,right)
                ave = tempValArray.mean()
                
                #round down to integer number of counts
                countsCORR[i] = math.floor(ave)
                
                #get line from original file, modify
                singleLineList = singleLine.split()
                singleLineList[3] = str(int(ave))
                singleLine = (singleLineList[0] + "\t" + 
                              singleLineList[1] + "\t" + 
                              singleLineList[2] + "\t" + 
                              singleLineList[3] + "\n")
           
            #write original or modified line
            newFile.write(singleLine)

        
        
        #close new file
        newFile.close()
        
        #move original file to preSpikeCorr directory
        shutil.copy2(name,"preSpikeCorr")
        
        #rename the new temp file to the original name
        os.rename("temp"+name,name)
        
        #plot corrected value        
        plt.plot(wavelengths,countsCORR)
    else:
        print("No spikes found")
    return

def correctSpectraInDir():
    
    #check if there is a folder to put pre spike corr data, and create if not
    if not os.path.exists("preSpikeCorr"):
        os.makedirs("preSpikeCorr")
    
    #get list of all filenames    
    filenames = os.listdir()
    
    #go through each file
    for filename in filenames:
        
        #make sure it is a textfile
        if ".txt" in filename:
            
            datafile = open(filename,"r")
            
            #make sure it has 4 data columns, then call correctSpectrum function
            if len(datafile.readline().split()) == 4:
                print("Searching for spikes in: ", filename)
                correctSpectrum(filename)
    
    
    return


#run it
correctSpectraInDir()



        
    
    





