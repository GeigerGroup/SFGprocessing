#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 19:38:56 2017

@author: pohno
"""

from spectrum import Spectrum

path = '/Users/pohno/Box Sync/Science/Data/SFG/Solstice/11192017/goldend'

gold = Spectrum(path)

gold.subtractBGs()

gold.plotDFGs()

gold.padDFGs()

gold.plotFullDFGs()

gold.sumDFGs()

gold.plotDFGsum()