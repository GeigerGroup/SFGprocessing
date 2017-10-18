# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import numpy for array functionality
import numpy as np


#read in datafile
datafile = open('3400test.txt','r')

#initialize array for wavelengths and counts
wavelengths = np.array([])
counts = np.array([])

#go through each line in datafile and append to arrays
for line in datafile:
    fields = line.split()
    wavelengths = np.append(wavelengths,[float(fields[0])])
    counts = np.append(counts,[float(fields[3])])

#import matplotlib for plotting
import matplotlib.pyplot as plt


#plot
plt.plot(wavelengths,counts)


#import pandas for rolling median function
import pandas

windowSize = 7
medians = pandas.Series(counts).rolling(window = windowSize,center=True).median()

#import math for floor
import math

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

countsCORR = counts.copy()

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
        
        countsCORR[i] = ave

#plot corrected value        
plt.plot(wavelengths,countsCORR)
    



        
    
    





