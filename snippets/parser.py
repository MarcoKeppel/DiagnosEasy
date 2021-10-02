import requests
import json
import time
import math
import random
import csv

def get_relevant_data():
    diabetic_patients = []

    # Diabetic data
    age = 'x0_age'
    bmi = 'x0an03a'
    sex = 'x0_sex'
    diabetes = 'x0md030'
    antihypertensive_medication =   1 #random.randint(0,1)
    prescribed_steroids = 1 # random.randint(0,1)
    smoking = 'x0sm00'
    family_history = 0.753 #random.choice([0,0.728,0.753])

    coronary_heart_disease_patients = []
    total_cholesterol = 'x0lp16'
    cholesterol_HDL = 'x0lp17'
    systolic_BP = 'x0bp01'
    treated_for_blood_pressure = 'x0bl02'
    coronary_heart_disease = 'x0mi08'

    for row in reader:
        diabetic_patient_data = [int(row[sex])-1, antihypertensive_medication,prescribed_steroids,float(row[age]),float(row[bmi]),family_history,int(row[smoking])-1, int(row[diabetes])]
        insert = True
        for x in diabetic_patient_data:
            if x < 0:
                insert = False
                break
        
        if insert:
            diabetic_patients.append(diabetic_patient_data)
        
        
        coronary_heart_disease_patient_data = [float(row[age]),
                                                int(row[total_cholesterol]),
                                                int(row[cholesterol_HDL]),
                                                int(row[systolic_BP]), 
                                                int(row[treated_for_blood_pressure]), 
                                                int(row[smoking]),
                                                0,
                                                0,
                                                0,
                                                int(row[sex])-1,
                                                int(row[coronary_heart_disease])]
        insert = True
        for x in coronary_heart_disease_patient_data:
            if x < 0:
                insert = False
                break
        if insert:
            if coronary_heart_disease_patient_data[4] == 2:
                coronary_heart_disease_patient_data[4] = 0

            if coronary_heart_disease_patient_data[5] == 2:
                coronary_heart_disease_patient_data[5] = 0
            else : 
                coronary_heart_disease_patient_data[5] = 1

            coronary_heart_disease_patient_data[7] = math.log(coronary_heart_disease_patient_data[0]) * coronary_heart_disease_patient_data[5]
            
            if coronary_heart_disease_patient_data[0] > 70 and coronary_heart_disease_patient_data[-2] == 0:
                coronary_heart_disease_patient_data[7] = math.log(70) * coronary_heart_disease_patient_data[5]
            if coronary_heart_disease_patient_data[0] > 78 and coronary_heart_disease_patient_data[-2] == 1:
                coronary_heart_disease_patient_data[7] = math.log(78) * coronary_heart_disease_patient_data[5]
            

            coronary_heart_disease_patient_data[0] = math.log(coronary_heart_disease_patient_data[0])
            coronary_heart_disease_patient_data[1] = math.log(coronary_heart_disease_patient_data[1])
            coronary_heart_disease_patient_data[2] = math.log(coronary_heart_disease_patient_data[2])
            coronary_heart_disease_patient_data[3] = math.log(coronary_heart_disease_patient_data[3])
            coronary_heart_disease_patient_data[6] = coronary_heart_disease_patient_data[0] * coronary_heart_disease_patient_data[1]
            
            
            coronary_heart_disease_patient_data[8] = coronary_heart_disease_patient_data[0] * coronary_heart_disease_patient_data[0]
            
            
            coronary_heart_disease_patients.append(coronary_heart_disease_patient_data)
    
    
    diabetic_patients, diabetic_multipliers = normalize_diabetics_parameters(diabetic_patients)
    
    
    coronary_heart_disease_patients, coronary_heart_disease_multipliers = normalize_coronary_heart_parameters(coronary_heart_disease_patients)

    return diabetic_patients, diabetic_multipliers, coronary_heart_disease_patients, coronary_heart_disease_multipliers

def mdcalc_probability_diabetes(diabetic_patient,diabetic_multiplier):
    exp = -6.322
    for i in range(0,len(diabetic_multiplier)):        
        exp += diabetic_patient[i] * diabetic_multiplier[i]
    return 1/(1+(math.e) ** -(exp))

def mdcalc_probability_heart_disease(coronary_heart_disease_patient,coronary_heart_disease_multiplier):
    L = 0
    for i in range(0,len(coronary_heart_disease_multiplier)):
        L += coronary_heart_disease_patient[i] * coronary_heart_disease_multiplier[i]
    P = 0
    if coronary_heart_disease_patient[-2] == 0:
        # Male 
        L -= 172.300168
        P =  1 - 0.9402 ** L
    else:
        L -= 146.5933061
        P = 1 - 0.98767 ** L
    return P


# https://www.mdcalc.com/cambridge-diabetes-risk-score#evidence
def normalize_diabetics_parameters(diabetic_patients):
    
    multipliers = []
    
    for person in diabetic_patients:
        
        tmp_mult = []
        
        # Gender
        tmp_mult.append(-0.879)

        # Prescribed antihypertensive medication
        tmp_mult.append(1.222)
        
        
        # Prescribed steroids
        tmp_mult.append(2.191)
        
        #Age

        tmp_mult.append(0.063)

        #BMI
        tmp_mult.append(1)
        if person[4] < 25:
            person[4] = 0
        elif person[4] >= 25 and person[4] <27.5:
            person[4] = 0.699
        elif person[4] >= 27.5 and person[4] < 30:
            person[4] = 1.97 
        else:
             person[4] = 2.518

        #Family history
        tmp_mult.append(1)
        if person[5] == 0:
            person[5] = 0
        elif person[5] == 1:
            person[5] = 0.728
        else:
            person[5] = 0.753

        #Smoking history
        tmp_mult.append(1)
        if person[6] == 0:
            person[6] = 0.855
        else:
            person[6] = 0
        multipliers.append(tmp_mult)
        # Diabetic
        if person[7] == 2:
            person[7] = 1
        else:
            person[7] = 0
    return diabetic_patients, multipliers
# https://www.mdcalc.com/framingham-risk-score-hard-coronary-heart-disease#evidence
def normalize_coronary_heart_parameters(coronary_heart_disease_patients):
    multipliers = []
    male_mult = [52.00961,20.014077,-0.905964,1.305784,0.241549,12.096316,-4.605038,-2.84367,-2.93323]
    female_mult = [31.764001,22.465206,-1.187731,2.552905,0.420251,13.07543,-5.060998,-2.996945]
    for x in coronary_heart_disease_patients:
        if x[-2] == 0:
            # Male
            multipliers.append(male_mult)
        else:
            multipliers.append(female_mult)

    return coronary_heart_disease_patients, multipliers



if __name__ == '__main__':
    csvfile = open("snippets/our_dataset.txt","r")
    
    #csvfile = open("../EURAC_Challenge/Eurac_CHRIS_Data/generated_variables.csv","r")
    reader = csv.DictReader(csvfile)
    diabetic_patients, diabetic_multipliers, coronary_heart_disease_patients, coronary_heart_disease_multipliers = get_relevant_data()
    '''

    correct = 0
    
    for i in range(0,len(diabetic_patients)):
        prob = mdcalc_probability_diabetes(diabetic_patients[i],diabetic_multipliers[i])
        if (prob > 0.5 and diabetic_patients[i][-1] == 1) or (prob <= 0.5 and diabetic_patients[i][-1] == 0):
            correct += 1
    print(correct)
    print(correct/len(diabetic_patients))
    
    
    for i in range(0,len(coronary_heart_disease_patients)):
        prob = mdcalc_probability_heart_disease(coronary_heart_disease_patients[i],coronary_heart_disease_multipliers[i])
        print(prob,coronary_heart_disease_patients[i][-1])
        if (prob > 0.5 and coronary_heart_disease_patients[i][-1] == 1) or (prob <= 0.5 and coronary_heart_disease_patients[i][-1] == 0):
            correct += 1
    print(correct)
    print(correct/len(coronary_heart_disease_patients))
    '''
    #
    # print(coronary_heart_disease_patients, coronary_heart_disease_multipliers)