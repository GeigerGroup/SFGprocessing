#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:04:26 2017

Class to hold data for a compilation of DFGs making up a whole spectrum.

@author: pohno
"""
import os

from dfg import DFG

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

            
                
                
