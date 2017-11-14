#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:04:26 2017

Class to hold data for a compilation of DFGs making up a whole spectrum.

@author: pohno
"""

class Spectrum():
    
    def __init__(self,path):
        
        #store path of this sets of DFG positions
        self.path = path
        
        #initialize empty lists for DFGs and backgrounds
        self.dfgs = []
        self.bgs = []
