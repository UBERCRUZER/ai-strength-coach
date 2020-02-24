# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:12:20 2019

@author: cruze
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


import athlete
import plan

def getMultiplier():
    # Generate universe variables
    
    x_fatigue = np.arange(0, 11, 1)
    x_stress = np.arange(0, 11, 1)
    x_multip  = np.arange(.9, 1.06, .03)
    
    # Generate fuzzy membership functions
    fatigue_lo = fuzz.trimf(x_fatigue, [0, 0, 8])
    fatigue_md = fuzz.trimf(x_fatigue, [4, 7, 9])
    fatigue_hi = fuzz.trimf(x_fatigue, [7, 10, 10])
    
    stress_lo = fuzz.trimf(x_stress, [0, 0, 7])
    stress_md = fuzz.trimf(x_stress, [4, 7, 9])
    stress_hi = fuzz.trimf(x_stress, [8, 10, 10])
    
    multip_lo = fuzz.trimf(x_multip, [.9, .9, 1])
    multip_md = fuzz.trimf(x_multip, [.93, 1, 1.03])
    multip_hi = fuzz.trimf(x_multip, [1, 1.06, 1.06])
    
    ## -------------------------- UNCOMMENT FOR VISUALIZATION----------------------
    ## Visualize these universes and membership functions
    #fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    #
    #ax0.plot(x_fatigue, fatigue_lo, 'b', linewidth=1.5, label='Low')
    #ax0.plot(x_fatigue, fatigue_md, 'g', linewidth=1.5, label='Medium')
    #ax0.plot(x_fatigue, fatigue_hi, 'r', linewidth=1.5, label='High')
    #ax0.set_title('Fatigue Level')
    #ax0.legend()
    #
    #ax1.plot(x_stress, stress_lo, 'b', linewidth=1.5, label='Low')
    #ax1.plot(x_stress, stress_md, 'g', linewidth=1.5, label='Medium')
    #ax1.plot(x_stress, stress_hi, 'r', linewidth=1.5, label='High')
    #ax1.set_title('Stress Level')
    #ax1.legend()
    #
    #ax2.plot(x_multip, multip_lo, 'b', linewidth=1.5, label='Low')
    #ax2.plot(x_multip, multip_md, 'g', linewidth=1.5, label='Medium')
    #ax2.plot(x_multip, multip_hi, 'r', linewidth=1.5, label='High')
    #ax2.set_title('Multiplier')
    #ax2.legend()
    #
    ## Turn off top/right axes
    #for ax in (ax0, ax1, ax2):
    #    ax.spines['top'].set_visible(False)
    #    ax.spines['right'].set_visible(False)
    #    ax.get_xaxis().tick_bottom()
    #    ax.get_yaxis().tick_left()
    #
    #plt.tight_layout()
    ## ----------------------------------------------------------------------------
    
    # We need the activation of our fuzzy membership functions at these values.
    # This is what fuzz.interp_membership exists for!
    
    
    fatigue = 10-float(input("Please rate your fatigue level 1-10 (10 = extreme fatigue and missing reps): "))
    sleep = float(input("Please rate your quality of sleep 1-10 (10 = excellent, plentiful sleep): "))
    tmp_stress = 10-float(input("Please rate your stress level 1-10 (10 = incredibly stressed): "))
    
    stress = (sleep + tmp_stress) / 2
    
    fatigue_level_lo = fuzz.interp_membership(x_fatigue, fatigue_lo, fatigue)
    fatigue_level_md = fuzz.interp_membership(x_fatigue, fatigue_md, fatigue)
    fatigue_level_hi = fuzz.interp_membership(x_fatigue, fatigue_hi, fatigue)
    
    stress_level_lo = fuzz.interp_membership(x_stress, stress_lo, stress)
    stress_level_md = fuzz.interp_membership(x_stress, stress_md, stress)
    stress_level_hi = fuzz.interp_membership(x_stress, stress_hi, stress)
    
    # Connecting rules
    active_rule1 = np.fmax(fatigue_level_lo, stress_level_lo)
    multip_activation_lo = np.fmin(active_rule1, multip_lo)  
    multip_activation_md = np.fmin(stress_level_md, multip_md)
    active_rule3 = np.fmax(fatigue_level_hi, stress_level_hi)
    
    multip_activation_hi = np.fmin(active_rule3, multip_hi)
    
    
    ## -------------------------- UNCOMMENT FOR VISUALIZATION----------------------
    #
    #multip0 = np.zeros_like(x_multip)
    ## Visualize this 
    #fig, ax0 = plt.subplots(figsize=(8, 3))
    #
    #ax0.fill_between(x_multip, multip0, multip_activation_lo, facecolor='b', alpha=0.7)
    #ax0.plot(x_multip, multip_lo, 'b', linewidth=0.5, linestyle='--', )
    #ax0.fill_between(x_multip, multip0, multip_activation_md, facecolor='g', alpha=0.7)
    #ax0.plot(x_multip, multip_md, 'g', linewidth=0.5, linestyle='--')
    #ax0.fill_between(x_multip, multip0, multip_activation_hi, facecolor='r', alpha=0.7)
    #ax0.plot(x_multip, multip_hi, 'r', linewidth=0.5, linestyle='--')
    #ax0.set_title('Output membership activity')
    #
    ## Turn off top/right axes
    #for ax in (ax0,):
    #    ax.spines['top'].set_visible(False)
    #    ax.spines['right'].set_visible(False)
    #    ax.get_xaxis().tick_bottom()
    #    ax.get_yaxis().tick_left()
    #
    #plt.tight_layout()
    #
    ##-----------------------------------------------------------------------------
    
    # Aggregate all three output membership functions together
    aggregated = np.fmax(multip_activation_lo,
                         np.fmax(multip_activation_md, multip_activation_hi))
    
    # Calculate defuzzified result
    multip = fuzz.defuzz(x_multip, aggregated, 'centroid')
#    multip_activation = fuzz.interp_membership(x_multip, aggregated, multip)  # for plot
       
    ## -------------------------- UNCOMMENT FOR VISUALIZATION----------------------
    ## Visualize this
    #fig, ax0 = plt.subplots(figsize=(8, 3))
    #
    #ax0.plot(x_multip, multip_lo, 'b', linewidth=0.5, linestyle='--', )
    #ax0.plot(x_multip, multip_md, 'g', linewidth=0.5, linestyle='--')
    #ax0.plot(x_multip, multip_hi, 'r', linewidth=0.5, linestyle='--')
    #ax0.fill_between(x_multip, multip0, aggregated, facecolor='Orange', alpha=0.7)
    #ax0.plot([multip, multip], [0, multip_activation], 'k', linewidth=1.5, alpha=0.9)
    #ax0.set_title('Aggregated membership and result (line)')
    #
    ## Turn off top/right axes
    #for ax in (ax0,):
    #    ax.spines['top'].set_visible(False)
    #    ax.spines['right'].set_visible(False)
    #    ax.get_xaxis().tick_bottom()
    #    ax.get_yaxis().tick_left()
    #
    #plt.tight_layout()
    ##-----------------------------------------------------------------------------
    
#    print("Raw: ", multip)
    return(multip)
    

def runPgrm(ath1, sPgrm, bPgrm, dPgrm, numWeeks, days):
    for wk in range(0,numWeeks):
        
        if wk > 0:
            current = getMultiplier()
            temp = ath1.multiplier
            ath1.multiplier = (current*2 + temp) / 3
#            print("Stored: ", ath1.multiplier)
            
        print("\n"+"\n"+"Athlete: ", ath1.getName())
        print("Week #",wk+1)
        
        for i in range(0,days):
            print("\n"+"Day ", i+1,":")
            print("Squat: ", sPgrm[wk][i].getRepScheme(), "@", round(sPgrm[wk][i].getPct()*100*ath1.multiplier,1),"%")
            print("Bench: ", bPgrm[wk][i].getRepScheme(), "@", round(bPgrm[wk][i].getPct()*100*ath1.multiplier,1),"%")
            print("Deadlift: ", dPgrm[wk][i].getRepScheme(), "@", round(dPgrm[wk][i].getPct()*100*ath1.multiplier,1),"%")


def main():
    

    days = 5
    weeks = 6
    
    #-------------------------------INPUTTING BASE PROGRAM---------------------
    
    squat = [[plan.Workout(0,"rest") for j in range(days)] for i in range(weeks)]
    
    squat[0][0].setWorkout(.7,"5x5")
    squat[0][2].setWorkout(.63,"2x5")
    squat[0][4].setWorkout(.8,"1x5")
    
    squat[1][0].setWorkout(.72,"5x5")
    squat[1][2].setWorkout(.65,"2x5")
    squat[1][4].setWorkout(.82,"1x5")
    
    squat[2][0].setWorkout(.74,"5x5")
    squat[2][2].setWorkout(.67,"2x5")
    squat[2][4].setWorkout(.84,"1x5")
    
    squat[3][0].setWorkout(.76,"5x5")
    squat[3][2].setWorkout(.69,"2x5")
    squat[3][4].setWorkout(.86,"1x5")
    
    squat[4][0].setWorkout(.78,"5x5")
    squat[4][2].setWorkout(.71,"2x5")
    squat[4][4].setWorkout(.88,"1x5")
    
    squat[5][0].setWorkout(.80,"5x5")
    squat[5][2].setWorkout(.73,"2x5")
    squat[5][4].setWorkout(.90,"1x5")
    
#    print("Squat: ", squat[0][0].getRepScheme(), squat[0][0].getPct())
#    print("Squat: ", squat[3][2].getRepScheme(), squat[3][2].getPct())
    
    bench = [[plan.Workout(0,"rest") for j in range(days)] for i in range(weeks)]

    bench[0][0].setWorkout(.8,"5x5")
    bench[0][4].setWorkout(1,"1x1")
    bench[1][2].setWorkout(.72,"3x5")
    
    bench[2][0].setWorkout(.825,"5x5")
    bench[2][4].setWorkout(1,"1x2")
    bench[3][2].setWorkout(.74,"3x5")
    
    bench[4][0].setWorkout(.85,"5x5")
    bench[4][4].setWorkout(1,"1x3")
    bench[5][2].setWorkout(.762,"3x5")
    
    deadlift = [[plan.Workout(0,"rest") for j in range(days)] for i in range(weeks)]

    deadlift[0][0].setWorkout(.8,"1x5")
    deadlift[1][0].setWorkout(.82,"1x5")
    
    deadlift[2][0].setWorkout(.84,"1x5")
    deadlift[3][0].setWorkout(.86,"1x5")
    
    deadlift[4][0].setWorkout(.88,"1x5")
    deadlift[5][0].setWorkout(.9,"1x5")
    
    #---------------------------END INPUTTING BASE PROGRAM---------------------

#    name = input("What's your name? ")
#    squat = input("What's your max squat? ")
#    bench = input("What's your max bench? ")
#    deadlift = input("What's your max deadlift? ")
    
    name = 'Mike'
    s = '485'
    b = '320'
    d = '545'

    ath1 = athlete.Athlete(name, s, b, d)
    
#    print(ath1.getName())
#    print(ath1.getSquat())
#    print(ath1.getBench())
#    print(ath1.getDeadlift())
    
    runPgrm(ath1, squat, bench, deadlift, weeks, days)

if __name__ == '__main__':
    main()