# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:49:07 2019

@author: cruze
"""

#import skfuzzy as fuzz
#from skfuzzy import control as ctrl

class Athlete:
        
    def __init__(self, n, s, b, d, fatigueLevel=0, stress=0, sleep=10, week=0):
        self.name = n
        
        self.s = s
        self.b = b
        self.d = d
        
        self.fatigue = fatigueLevel
        self.stress = stress
        self.sleep = sleep
        
        self.week = week
        
        self.multiplier = 1
    
    def setFatigue(self,f):
        self.fatigue = f
        
    def setStress(self,s):
        self.stress = s
        
    def setSleep(self,s):
        self.sleep = s

    def getSleep(self):
        return(self.sleep)
    
    def getStress(self):
        return(self.stress)
        
    def getFatigue(self):
        return(self.fatigue)
    
    def getSquat(self):
        return(self.s)
    
    def getBench(self):
        return(self.b)
        
    def getDeadlift(self):
        return(self.d)


        
    def getWeek(self):
        return(self.week)

    def getName(self):
        return(self.name)