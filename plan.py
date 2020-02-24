# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:12:28 2019

@author: cruze
"""


class Workout:
    def __init__(self, pct, repScheme):
        self.pct = pct
        self.repScheme = repScheme
        
    def setWorkout(self, pct, repScheme):
        self.pct = pct
        self.repScheme = repScheme
    
    def getPct(self):
        return(self.pct)
        
    def getRepScheme(self):
        return(self.repScheme)
                 

        
        