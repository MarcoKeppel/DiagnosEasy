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
    antihypertensive_medication =  random.randint(0,1)
    prescribed_steroids =  random.randint(0,1)
    smoking = 'x0sm00'
    family_history = random.choice([0,0.728,0.753])

    coronary_heart_disease_patient_data = []
    
    for row in reader:
        diabetic_patient_data = [int(row[sex])-1, antihypertensive_medication,prescribed_steroids,float(row[age]),float(row[bmi]),family_history,int(row[smoking])-1, int(row[diabetes])]
        for x in diabetic_patient_data:
            if x < 0:
                continue
        

        diabetic_patients.append(patient_data)
    '''
    total_cholesterol = 'x0lp16'
    cholesterol_HDL = 'x0lp17'
    systolic_BP = 'x0bp01'
    treated_for_blood_pressure = 'x0bl02'

    coronary_heart_disease_patient_data = [float(row[age]),row[total_cholesterol],row[cholesterol_HDL],row[systolic_BP], row[treated_for_blood_pressure], row[smoking],row[age]]

    '''

    #coronary_heart_disease = 'x0mi08'
    diabetic_patients, diabetic_multipliers = normalize_diabetics_parameters(diabetic_patients)

    

    

# https://www.mdcalc.com/cambridge-diabetes-risk-score#evidence
def normalize_diabetics_parameters(diabetic_patients):
    
    multipliers = []
    
    for person in diabetic_patients:
        
        tmp_mult = []
        
        # Gender
        if person[0] == 0:
            tmp_mult.append(0)
        else:
            tmp_mult.append(1)

        # Prescribed antihypertensive medication
        if person[1] == 0:
            tmp_mult.append(0)
        else:
            tmp_mult.append(1)
        
        # Prescribed steroids
        if person[2] == 0:
            tmp_mult.append(0)
        else:
            tmp_mult.append(1)

        #Age

        tmp_mult.append(0.063)

        #BMI

        if person[4] < 25:
            tmp_mult.append(0)
        elif person[4] >= 25 and person[4] <27.5:
            tmp_mult.append(0.699)
        elif person[4] >= 27.5 and person[4] < 30:
            tmp_mult.append(1.97)
        else:
            tmp_mult.append(2.518)

        #Family history
        if person[5] == 0:
            tmp_mult.append(0)
        elif person[5] == 1:
            tmp_mult.append(0.728)
        else:
            tmp_mult.append(0.753)

        #Smoking history
        if person[6] == 0:
            tmp_mult.append(0.855)
        else:
            tmp_mult.append(0)
        multipliers.append(tmp_mult)
    
        if person[7] == 2:
            person[7] = 1
        else:
            person[7] = 0
    return diabetic_patients, multipliers





if __name__ == '__main__':
    
    csvfile = open("./Hackathon/EURAC_Challenge/Eurac_CHRIS_Data/generated_variables.csv","r")
    reader = csv.DictReader(csvfile)
    get_relevant_data() 
    #persons, multipliers = calc_score_diabetes()