from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import json
import math
import csv
import time
from diagnoseasy_backend.settings import get_relevant_data,kb_diabetic_patients_list,kb_diabetic_multipliers,kb_coronary_heart_disease_patients_list,kb_coronary_heart_disease_multipliers

@csrf_exempt
def get_correlations(request):

    request_body = json.loads(request.body)
    person_info = request_body['info']

    print(person_info)

    # Could use some library, but it's 4:30AM so I'm not doing that

    person_data = []
    for f in person_info:
        person_data.append(person_info[f])

    print(person_data)

    result = diagnose(person_data)

    # Execute function based on condition, get and return results (i.e. possible correlations/conditions)

    return JsonResponse(result)




def mdcalc_probability_diabetes(diabetic_patient, diabetic_multiplier):
    exp = -6.322
    for i in range(0, len(diabetic_multiplier)):
        exp += diabetic_patient[i] * diabetic_multiplier[i]
    return 1 / (1 + (math.e) ** -(exp))


def mdcalc_probability_heart_disease(coronary_heart_disease_patient, coronary_heart_disease_multiplier):
    L = 0
    for i in range(0, len(coronary_heart_disease_multiplier)):
        L += coronary_heart_disease_patient[i] * coronary_heart_disease_multiplier[i]
    P = 0
    if coronary_heart_disease_patient[-2] == 0:
        # Male
        L -= 172.300168
        P = 1 - 0.9402 ** L
    else:
        L -= 146.5933061
        P = 1 - 0.98767 ** L
    return P



# Example: values = [ int ] , multipliers = [ int ]
def euclidean_distance(set1, set2, multiplier1, multiplier2):
    # print(set1)
    # print(set2)
    # print(multiplier1)
    # print(multiplier2)
    # if len(set1)-1 != len(multiplier1) or len(set1)-1 != len(set2)-1 or len(set1)-1 != len(multiplier2):
    #     raise Exception("Values and multipliers are not the same length")
    rtn = 0
    for i in range(len(multiplier1)):
        rtn += ((set1[i] * multiplier1[i] - set2[i] * multiplier2[i]) ** 2)
    rtn = math.sqrt(rtn)
    return rtn


def knn(new_sample, dataset, multipliers, k):
    neighbors_distance = []
    neighbors = []
    threshold = None
    counter = 1
    for sample in dataset:
        ed = euclidean_distance(new_sample, sample, multipliers[0], multipliers[counter])
        if threshold is None:
            threshold = ed
            neighbors_distance.append(ed)
            neighbors.append(sample)
        elif ed < threshold:
            neighbors_distance.append(ed)
            neighbors.append(sample)
            if len(neighbors) > k:
                tmp_max = max(neighbors_distance)
                neighbors.pop(neighbors_distance.index(tmp_max))
                neighbors_distance.remove(tmp_max)
        counter += 1
    return neighbors, neighbors_distance


def risk_score(patients):
    positives = 0
    for patient in patients:
        if patient[-1] == 1:
            positives += 1
    return positives / len(patients) * 100


def get_score(sample, sample_multipliers, diabetic_patients, diabetic_multipliers, k_neighbors=200):

    diabetic_multipliers = sample_multipliers + diabetic_multipliers

    # sample = diabetic_patients[-delta]

    result = knn(sample, diabetic_patients, diabetic_multipliers, k_neighbors)

    risk = risk_score(result[0])
    # correctness += abs(new_sample[-1] - risk / 100)

    return risk


def diagnose(patient):
    st = time.time()
    with open("starter.txt", "w") as fd:
        fd.write(
            'cf,x0_age,x0_ager,x0_birthd,x0_birthm,x0_birthy,x0_birthpc,x0_examd,x0_examm,x0_examy,x0_residp,x0_sex,x0ge00,x0ge01a,x0ge01b,x0ge02a,x0ge02b,x0ge03a,x0ge03b,x0ge04a,x0ge04b,x0ge05a,x0ge05b,x0ge06a,x0ge06b,x0_geno,x0_wes,x0_micros,x0_nafld,x0_paregen,x0_familyla,x0lp02a,x0lp02aq,x0lp02b,x0lp02c,x0lp02d,x0lp03,x0lp04,x0lp04q,x0lp05,x0lp06a,x0lp06b,x0lp07,x0lp08,x0lp09,x0lp10,x0lp11,x0lp11q,x0lp12,x0lp12q,x0lp13,x0lp14a,x0lp14b,x0lp14bq,x0lp15,x0lp15q,x0lp16,x0lp17,x0lp18,x0lp19,x0lp20,x0lp21,x0lp22,x0lp23,x0lp23a,x0lp24,x0lp25,x0lp25a,x0lp25q,x0lp25aq,x0lp26,x0lp26a,x0lp27,x0lp28,x0lp28q,x0lp29,x0lp30,x0lp31,x0lp32,x0lp32q,x0lp33,x0lp33q,x0lp35,x0lp36,x0lp36a,x0lp36q,x0lp36aq,x0lp37,x0lp37q,x0lp38,x0lp39,x0lp40,x0lp41,x0lp42,x0lp43,x0lp44,x0lp45,x0lp46,x0lp47,x0lp48,x0lp50a,x0lp50b,x0lp50c,x0lp50d,x0lp50e,x0lp50f,x0lp50g,x0lp50h,x0lp50i,x0lp50j,x0lp51a,x0lp51c,x0lp51e,x0lp51f,x0lp51g,x0lp52,x0lp52q,x0lp82,x0lp83,x0lp84,x0lp85,x0lp86a,x0lp86b,x0bc01,x0bc02,x0bc03a,x0bc04,x0bc05,x0bc06a,x0bc07a,x0bc07b,x0bc07c,x0bc07d,x0bc08,x0bc09,x0bc09a,x0bc09b,x0bc09c,x0bc10,x0bc11,x0bc12,x0bc12a,x0bc13,x0bc13a,x0bcver,x0lp01,x0lp53,x0lp54,x0lp54q,x0lp55,x0lp55q,x0lp56,x0lp56q,x0lp58,x0lp58q,x0lp59,x0lp59q,x0lp60,x0lp60q,x0lp61a,x0lp61aq,x0lp61c,x0lp61d,x0lp63,x0lp63q,x0lp64,x0lp64q,x0cs01,x0cs01a,x0cs01b,x0cs02,x0cs02a,x0cs02b,x0cs03,x0cs03a,x0cs03b,x0cs05,x0cs06,x0cs07,x0cs08,x0cs08a,x0cs08b,x0cs08c,x0cs08d,x0cs09,x0cs09a,x0cs09b,x0cs09c,x0cs09d,x0cs10,x0cs10a,x0cs10b,x0cs10c,x0cs10d,x0cs11,x0cs12,x0cs13a,x0cs13b,x0mt01,x0mt01a,x0mt02,x0mt02a,x0mt05,x0mt06,x0mt06a,x0he01,x0he02,x0he03,x0he04,x0an01,x0an02,x0an02q,x0an03a,x0an03b,x0an03c,x0an03q,x0an04,x0an04q,x0an05,x0an10a,x0an11,x0an06,x0an07,x0an08,x0an09,x0bp01,x0bp01a,x0bp01b,x0bp01c,x0bp01m,x0bp02,x0bp02a,x0bp02b,x0bp02c,x0bp02m,x0bp03,x0bp03a,x0bp03b,x0bp03c,x0bp03m,x0bp04a,x0bp05,x0bp05a,x0bp05b,x0bp08a,x0bp08b,x0bp08c,x0bp09a,x0bp09b,x0bp09c,x0bp10,x0bp10a,x0bp10b,x0bpver,x0ec101,x0ec102,x0ec103,x0ec104,x0ec104a,x0ec104b,x0ec104c,x0ec104d,x0ec104e,x0ec104f,x0ec104g,x0ec104h,x0ec104i,x0ec104j,x0ec104k,x0ec104l,x0ec105a,x0ec105b,x0ec105c,x0ec105d,x0ec105e,x0ec105f,x0ec105g,x0ec105h,x0ec105i,x0ec105j,x0ec105k,x0ec105l,x0ec106a,x0ec106b,x0ec106c,x0ec106d,x0ec106e,x0ec106f,x0ec106g,x0ec106h,x0ec106i,x0ec106j,x0ec106k,x0ec106l,x0ec107,x0ec108,x0ec108a,x0ec108b,x0ec108c,x0ec108d,x0ec108e,x0ec108f,x0ec108g,x0ec108h,x0ec108i,x0ec108j,x0ec108k,x0ec108l,x0ec109a,x0ec109b,x0ec109c,x0ec109d,x0ec109e,x0ec109f,x0ec109g,x0ec109h,x0ec109i,x0ec109j,x0ec109k,x0ec109l,x0ec110a,x0ec110b,x0ec110c,x0ec110d,x0ec110e,x0ec110f,x0ec110g,x0ec110h,x0ec110i,x0ec110j,x0ec110k,x0ec110l,x0ec111,x0ec112,x0ec113,x0ec113a,x0ec113b,x0ec113c,x0ec113d,x0ec113e,x0ec113f,x0ec113g,x0ec113h,x0ec113i,x0ec113j,x0ec113k,x0ec113l,x0ec114,x0ec115,x0ec115a,x0ec115b,x0ec115c,x0ec115d,x0ec115e,x0ec115f,x0ec115g,x0ec115h,x0ec115i,x0ec115j,x0ec115k,x0ec115l,x0ec116,x0ec117,x0ec117a,x0ec117b,x0ec117c,x0ec117d,x0ec117e,x0ec117f,x0ec117g,x0ec117h,x0ec117i,x0ec117j,x0ec117k,x0ec117l,x0ec118a,x0ec118b,x0ec119,x0ec120a,x0ec120b,x0ec120c,x0ec120d,x0ec120e,x0ec120f,x0ec120g,x0ec120h,x0ec120i,x0ec120j,x0ec120k,x0ec120l,x0ec121a,x0ec121b,x0ec121c,x0ec121d,x0ec121e,x0ec121f,x0ec121g,x0ec121h,x0ec121i,x0ec121j,x0ec121k,x0ec121l,x0ec122a,x0ec122b,x0ec122c,x0ec122d,x0ec122e,x0ec122f,x0ec122g,x0ec122h,x0ec122i,x0ec122j,x0ec122k,x0ec122l,x0ec123a,x0ec123b,x0ec123c,x0ec123d,x0ec123e,x0ec123f,x0ec123g,x0ec123h,x0ec123i,x0ec123j,x0ec123k,x0ec123l,x0ec124a,x0ec124b,x0ec125a,x0ec125b,x0ec125c,x0ec125d,x0ec125e,x0ec125f,x0ec125g,x0ec125h,x0ec125i,x0ec125j,x0ec125k,x0ec125l,x0ec126a,x0ec126b,x0ec126c,x0ec126d,x0ec126e,x0ec126f,x0ec126g,x0ec126h,x0ec126i,x0ec126j,x0ec126k,x0ec126l,x0ec127a,x0ec127b,x0ec127c,x0ec127d,x0ec127e,x0ec127f,x0ec127g,x0ec127h,x0ec127i,x0ec127j,x0ec127k,x0ec127l,x0ec128a,x0ec128b,x0ec128c,x0ec128d,x0ec128e,x0ec128f,x0ec128g,x0ec128h,x0ec128i,x0ec128j,x0ec128k,x0ec128l,x0ec129a,x0ec129b,x0ec129c,x0ec129d,x0ec129e,x0ec129f,x0ec129g,x0ec129h,x0ec129i,x0ec129j,x0ec129k,x0ec129l,x0ec130,x0ec130a,x0ec130b,x0ec130c,x0ec130d,x0ec130e,x0ec130f,x0ec130g,x0ec130h,x0ec130i,x0ec130j,x0ec130k,x0ec130l,x0ec131a,x0ec131b,x0ec131c,x0ec131d,x0ec131e,x0ec131f,x0ec131g,x0ec131h,x0ec131i,x0ec131j,x0ec131k,x0ec131l,x0ec132,x0ec133,x0ec133a,x0ec133b,x0ec133c,x0ec133d,x0ec133e,x0ec133f,x0ec133g,x0ec133h,x0ec133i,x0ec133j,x0ec133k,x0ec133l,x0ec134,x0ec135,x0ec135a,x0ec135b,x0ec135c,x0ec135d,x0ec135e,x0ec135f,x0ec135g,x0ec135h,x0ec135i,x0ec135j,x0ec135k,x0ec135l,x0ec136,x0ec137a,x0ec137b,x0ec137c,x0ec137d,x0ec137e,x0ec137f,x0ec137g,x0ec137h,x0ec137i,x0ec137j,x0ec137k,x0ec137l,x0ec138a,x0ec138b,x0ec138c,x0ec138d,x0ec138e,x0ec138f,x0ec138g,x0ec138h,x0ec138i,x0ec138j,x0ec138k,x0ec138l,x0ec139a,x0ec139b,x0ec139c,x0ec139d,x0ec139e,x0ec139f,x0ec139g,x0ec139h,x0ec139i,x0ec139j,x0ec139k,x0ec139l,x0ec140,x0ec141a,x0ec141b,x0ec141c,x0ec141d,x0ec141e,x0ec141f,x0ec141g,x0ec141h,x0ec141i,x0ec141j,x0ec141k,x0ec141l,x0ec142,x0ec143a,x0ec143b,x0ec143c,x0ec143d,x0ec143e,x0ec143f,x0ec143g,x0ec143h,x0ec143i,x0ec143j,x0ec143k,x0ec143l,x0ec01,x0ec02,x0ec03,x0ec04,x0ec05,x0ec06,x0ec07,x0ec08,x0ec09,x0ec10,x0ec11,x0ec13,x0ec15,x0ec16,x0ec17,x0ec18,x0ec19,x0ec20,x0ec21,x0ec22,x0ec23,x0ec24,x0ec25,x0ec26,x0ec27,x0ec28,x0ec29,x0ec30,x0ec31,x0ec32,x0ec33,x0ec34,x0ec35,x0ec36,x0ec37,x0ec38,x0ec39,x0ec40,x0ec41,x0ec42,x0ec43,x0ec46,x0ec49,x0ec52,x0ec55,x0ec56,x0ec57,x0ec58,x0ec59,x0ec62,x0ec65,x0ec77,x0ec78,x0ec78a,x0ec78b,x0ec78c,x0ec78d,x0ec78e,x0re01,x0re02,x0ec,exclude,x0ecver,x0am01,x0am02,x0am03,x0amver,x0_optestc,x0mm01,"x0mm02,",x0mm03,x0mm04,x0mm05,x0mm06,x0mm07,x0mm08,x0mm09,x0mm10,x0mm11,x0mm12,x0mm13,x0mm14,x0mm15,x0mm16,x0mm17,x0mm18,x0mm19,x0mm20,x0mm21,x0mm22,x0mm23,x0mm24,x0mm25,x0mm26,x0mm27,x0mm28,x0mm29,x0mm30,x0mm31,x0mm32,x0mm33,x0mmver,x0ol00,x0ol00a,x0ol00b,x0ol00c,x0ol01,x0ol01a,x0ol02,x0ol02a,x0ol03,x0ol03a,x0ol04,x0ol04a,x0ol05,x0ol05a,x0ol06,x0ol06a,x0ol07,x0ol07a,x0ol08,x0ol08a,x0ol09,x0ol09a,x0ol10,x0ol10a,x0ol11,x0ol11a,x0ol12,x0ol12a,x0ol13,x0ol13a,x0ol14,x0ol14a,x0ol15,x0ol15a,x0ol16,x0ol16a,x0ol17,x0ol22,x0ol22a,x0ol23a,x0ol23b,x0ol24,x0olcp,x0olver,x0dd01,x0dd02a,x0dd20,x0dd21,x0dd22,x0dd23,x0dd24,x0dd25,x0dd26,x0dd27,x0dd28,x0dd29,x0dd30,x0dd31,x0dd32,x0dd33,x0dd34,x0dd35,x0dd36,x0dd37,x0dd38,x0dd39,x0dd40,x0dd41,x0dd42,x0dd43,x0dd44,x0dd02,x0dd03,x0dd04,x0dd05,x0dd06,x0dd08,x0dd09,x0dd11,x0dd12,x0dd13,x0dd14,x0dd15,x0dd16,x0dd19,x0dd46,x0_opintc,x0pe02,x0pe02a,x0pe02b,x0pe02c,x0pe02d,x0pe03,x0pe04,x0pe05d,x0pe05e,x0pe06,x0pe07,x0pe08,x0pe09,x0pe10,x0pe11,x0pe11a,x0pe11b,x0pever,x0oc00,x0oc01,x0oc01a,x0oc02a,x0oc02c,x0oc02d,x0oc02e,x0oc03,x0oc03a,x0oc03c,x0oc03d,x0oc03e,x0oc04,x0oc04a,x0oc04c,x0oc04d,x0oc04e,x0oc05,x0oc05a,x0oc05c,x0oc05d,x0oc05e,x0oc06,x0oc06a,x0oc06c,x0oc06d,x0oc06e,x0oc07,x0oc07a,x0oc07c,x0oc07d,x0oc07e,x0oc08,x0oc10,x0oc11a,x0oc11b,x0oc12,x0oc13,x0oc13a,x0oc13b,x0oc13c,x0ocver,x0ex01,x0ex01a,x0ex02,x0ex02a,x0ex03,x0ex03a,x0ex04,x0ex04a,x0ex05,x0ex05a,x0ex06,x0ex06a,x0ex07,x0ex07a,x0ex08,x0ex08a,x0ex09,x0ex09a,x0ex10,x0ex11,x0ex11a,x0ex12,x0ex12a,x0ex13,x0ex13a,x0ex20,x0ex21,x0ex22,x0ex23,x0ex24,x0ex25,x0ex26,x0ex27,x0ex28,x0ex29,x0ex30,x0ex31,x0ex32,x0exver,x0bi01,x0bi01a,x0bi02,x0bi02a,x0bi03,x0bi04,x0bi05,x0bi05a,x0bi06,x0biver,x0wo01,x0wo01b,x0wo02,x0wo03,x0wo04b,x0wo05,x0wo05a,x0wo06,x0wo07,x0wo08,x0wo09,x0wo10,x0wo11a,x0wo12,x0wo12a,x0wover,x0fd01,x0fd02,x0fd03,x0fd04,x0fd05,x0fd06,x0fd07,x0fd08,x0fd09,x0fd10,x0fd11,x0fd12,x0fd13,x0fd14,x0fd15,x0fd16,x0fd17,x0fd18,x0fd19,x0fd20,x0fd21,x0fd22,x0fd23,x0fd24,x0fd25,x0fd26,x0fd27,x0fd28,x0fd29,x0fd30,x0fd31,x0fd31a,x0fd31b,x0fd31c,x0fd31d,x0fd31e,x0fd31f,x0fd32,x0fd32a,x0fd32b,x0fd32c,x0fd32d,x0fd32e,x0fd32f,x0fd33,x0fd33a,x0fd33b,x0fd33c,x0fd33d,x0fd33e,x0fd33f,x0fd34,x0fd34a,x0fd34b,x0fd34c,x0fd34d,x0fd34e,x0fd34f,x0fd35,x0fdver,x0al00,x0al01,x0al02a,x0al02b,x0al03a,x0al03b,x0al03c,x0al03d,x0al03e,x0al03f,x0al04a,x0al04b,x0al04c,x0al04d,x0al04e,x0al04f,x0al05a,x0al05b,x0al05c,x0al05d,x0al05e,x0al05f,x0al05g,x0al05h,x0al06b,x0al07b,x0al08,x0al08a,x0al08b,x0al08c,x0al08d,x0al09,x0al10,x0al10a,x0sm00,x0sm01b,x0sm02,x0sm03,x0sm04,x0sm05,x0sm06b,x0sm07,x0sm07b,x0sm08,x0sm10,x0sm11b,x0sm12b,x0sm12c,x0sm13,x0sm14,x0sm15b,x0sm16b,x0sm16c,x0sm17,x0sm18,x0sm19b,x0sm20b,x0sm20c,x0sm21,x0sm22,x0sm23b,x0sm24b,x0sm24c,x0sm25,x0sm26,x0sm26a,x0sm26b,x0sm27,x0sm27a,x0sm27b,x0sm28,x0sm28a,x0sm28b,x0sm29,x0sm29a,x0sm29b,x0sm30,x0sm30a,x0sm30b,x0sm31,x0sm31a,x0sm31b,x0sm32,x0sm33,x0sm34,x0sm34a,x0sm35,x0sm36,x0sm37,x0sm38,x0sm39,x0sm39a,x0sm40,x0sm41,x0sm42,x0sm43,x0sm44,x0sm45,x0sm46,x0sm47,x0sm48,x0sm49,x0sm49a,x0sm49b,x0sm49c,x0sm49d,x0sm51,x0sm52,x0sm53,x0sm54,x0sm55,x0sm56,x0sm57,x0sm58,x0sm59,x0sm60,x0sm61,x0smver,x0va01,x0va02,x0va03,x0va04,x0va05,x0va06,x0va07,x0va08,x0va09,x0va10,x0va11,x0va12,x0va13,x0vaver,x0cd01,x0cd01b,x0cd01c,x0cd01d,x0cd01e,x0cd02,x0cd02b,x0cd02c,x0cd02d,x0cd03,x0cd03b,x0cd03c,x0cd03d,x0cd04,x0cd04b,x0cd04c,x0cd04d,x0cd05,x0cd05b,x0cd05c,x0cd05d,x0cd06,x0cd06b,x0cd06c,x0cd06d,x0cd07,x0cd07b,x0cd07c,x0cd07d,x0cd08,x0cd08b,x0cd08c,x0cd08d,x0cd09,x0cd09b,x0cd09c,x0cd09d,x0cd10,x0cd10b,x0cd10c,x0cd10d,x0cd11,x0cd11b,x0cd11c,x0cd11d,x0cd12,x0cd12b,x0cd12c,x0cd12d,x0cd13,x0cd13b,x0cd13c,x0cd13d,x0cd14,x0cd14b,x0cd14c,x0cdver,x0ca00,x0ca00a,x0ca01a,x0ca01c,x0ca02a,x0ca02c,x0ca03a,x0ca03c,x0ca04a,x0ca04c,x0ca05a,x0ca05c,x0caver,x0dm00,x0dm01b,x0dm02,x0dm03,x0dm04b,x0dmver,x0th00,x0th01,x0th01a,x0th02,x0th02a,x0th03,x0th03a,x0th04,x0th04a,x0th05,x0th05a,x0th06,x0th06a,x0th07,x0th07a,x0th08,x0th09,x0th09a,x0th11,x0th11a,x0th12,x0th12a,x0th12b,x0th13,x0th13a,x0th13b,x0th13c,x0th14,x0th14a,x0th14b,x0th14c,x0th14d,x0th14e,x0th14f,x0thver,x0bl01,x0bl01b,x0bl01c,x0bl02,x0bl02a,x0bl02b,x0bl02c,x0bl11,x0bl11b,x0bl12,x0bl12a,x0bl12b,x0bl12c,x0blver,x0ki00,x0ki01,x0ki01b,x0ki01c,x0ki02,x0ki02b,x0ki02c,x0ki04,x0ki04b,x0ki04c,x0ki05,x0ki05b,x0ki05c,x0ki06,x0ki06b,x0ki06c,x0ki07,x0ki07b,x0ki07c,x0ki08,x0ki08b,x0ki08c,x0ki09,x0ki09b,x0ki09c,x0ki09d,x0ki10,x0ki10a,x0ki11b,x0ki12b,x0ki13b,x0ki14b,x0ki15b,x0ki16,x0ki17,x0ki17b,x0ki18,x0ki18b,x0ki19,x0ki19b,x0ki20,x0ki20b,x0ki21,x0ki21b,x0ki22,x0ki22b,x0ki23,x0ki23b,x0kiver,x0mi00,x0mi01,x0mi02,x0mi03,x0mi04,x0mi05a,x0mi05b,x0mi05c,x0mi05d,x0mi05e,x0mi06,x0mi07,x0mi08,x0mi08a,x0mi08c,x0mi08d,x0mi09,x0mi09a,x0mi10,x0mi11a,x0mi11b,x0mi12a,x0mi12b,x0mi13a,x0mi13b,x0mi14a,x0mi14b,x0mi15a,x0mi15b,x0mi16,x0mi17,x0mi18,x0mi19a,x0mi19b,x0mi20,x0mi21,x0mi22,x0mi23,x0mi24,x0mi25,x0mi26,x0miver,x0hf01,x0hf01b,x0hf02,x0hf02b,x0hf03,x0hf03b,x0hf04,x0hf04b,x0hf05,x0hf05b,x0hf06,x0hf07,x0hf07b,x0hf07c,x0hf08,x0hf08a,x0hf08b,x0hf08c,x0hf08d,x0hf09,x0hf10,x0hf11,x0hf12,x0hf13,x0hfver,x0af01,x0af01b,x0af01c,x0af01d,x0af02,x0af02a,x0af02c,x0af02d,x0af03,x0af03a,x0af03b,x0af03c,x0af03d,x0af03e,x0af03f,x0af03g,x0af03h,x0af04,x0af05,x0af06,x0af07,x0af07b,x0af08,x0af09,x0af09a,x0af10,x0af11,x0af12,x0af13,x0af13a,x0af14,x0af14a,x0af15,x0af16,x0af17,x0af18,x0af19,x0af20,x0af21,x0af22,x0af22a,x0af23,x0afver,x0ci01,x0ci02a,x0ci02b,x0ci02c,x0ci03,x0ci04,x0ci05,x0ci06,x0ci06a,x0ci06b,x0civer,x0st00,x0st00a,x0st01a,x0st01b,x0st02a,x0st02b,x0st03a,x0st03b,x0st04a,x0st04b,x0st05a,x0st05b,x0st06a,x0st06b,x0st07,x0st07a,x0st08,x0st08a,x0st09,x0st09a,x0st09b,x0st10,x0st10a,x0st10b,x0st11,x0st11a,x0st12,x0st12a,x0st20,x0st20b,x0st21,x0st21b,x0stver,x0ne01,x0ne01b,x0ne01c,x0ne01d,x0ne02,x0ne02a,x0ne02c,x0ne02d,x0ne03a1,x0ne03a2,x0ne03a3,x0ne03a4,x0ne03a5,x0ne03a6,x0ne03b,x0ne03c,x0ne04,x0ne04b,x0ne04c,x0ne05,x0ne05b,x0ne05c,x0ne05d,x0ne05e,x0ne06,x0ne06a,x0ne06c,x0ne06d,x0ne07,x0ne07b,x0ne07c,x0ne07d,x0ne07e,x0ne08,x0ne08b,x0ne09,x0ne09b,x0ne10,x0ne10b,x0ne11,x0ne11b,x0ne11c,x0ne11d,x0ne12,x0ne12a,x0ne12c,x0ne12d,x0ne13,x0ne13a,x0ne13c,x0ne13d,x0ne14a,x0ne14b,x0ne14c,x0ne14d,x0ne20,x0ne20a,x0ne20c,x0ne20d,x0ne21,x0ne21a,x0ne21c,x0ne21d,x0ne22,x0ne22a,x0ne22c,x0ne22d,x0never,x0pk01,x0pk02,x0pk03,x0pk04,x0pk05,x0pk06,x0pk07,x0pk08,x0pk09,x0pk10,x0pk11,x0pk12,x0pk12a,x0pk13,x0pk13a,x0pkver,x0mg01,x0mg01a,x0mg02,x0mg02a,x0mg03,x0mg04,x0mg05,x0mg06,x0mg07,x0mg08,x0mg09,x0mg10,x0mg11,x0mg12,x0mg13,x0mg14,x0mg15,x0mg16,x0mg17,x0mg18,x0mg19,x0mg20,x0mg21,x0mg22,x0mg23,x0mg24,x0mg25,x0mgver,x0pn00,x0pn01,x0pn02,x0pn03,x0pn04,x0pn05a,x0pn05b,x0pn05c,x0pn06a,x0pn06b,x0pn11,x0pn12,x0pn13,x0pn14,x0pn21,x0pn22,x0pn23,x0pn24,x0pn31,x0pnver,x0ot01,x0ot01c,x0ot02,x0ot02c,x0ot03,x0ot03c,x0ot04,x0ot04c,x0ot11,x0ot11c,x0ot12,x0ot12c,x0ot13,x0ot13c,x0ot14,x0ot14c,x0ot15,x0ot15c,x0ot16,x0ot16c,x0ot17,x0ot17c,x0ot18,x0ot18c,x0ot19,x0ot19c,x0ot20,x0ot20c,x0ot21,x0ot21c,x0ot22,x0ot22c,x0ot23,x0ot23c,x0ot24,x0ot24c,x0otver,x0_langself,x0ip01,x0ip01a,x0ip01b,x0ip01d,x0ip02,x0ip02a,x0ip02b,x0ip02d,x0ip03,x0ip03a,x0ip03b,x0ip03d,x0ip04a,x0ip04b,x0ip05,x0ip06,x0ip07,x0ip08,x0ip09,x0ipver,x0ps01,x0ps02,x0ps03,x0ps04,x0ps05,x0ps06,x0ps07,x0ps08,x0ps09,x0ps10,x0ps11,x0ps12,x0ps13,x0ps14,x0ps15,x0ps16,x0ps17,x0ps21,x0ps21a,x0ps22,x0ps22a,x0ps23,x0ps23a,x0ps24,x0ps24a,x0psver,x0mc01,x0mc02,x0mc03,x0mc04,x0mc05a,x0mc06a,x0mc07,x0mc08a,x0mc09,x0mc10,x0mc11a,x0mc12a,x0mc13,x0mc14a,x0mc15,x0mc16,x0mc21,x0mc22,x0mc23,x0mc24,x0mc25,x0mc26,x0mcver,x0sq01a,x0sq02,x0sq03a,x0sq04a,x0sq05,x0sq06,x0sq07,x0sq08,x0sq09,x0sq10,x0sq11,x0sq12,x0sq13,x0sq14,x0sq15,x0sq16,x0sq17,x0sq18,x0sq19,x0sq20,x0sq21,x0sq22,x0sq23,x0sq31,x0sq32,x0sq33,x0sq34,x0sq35,x0sq36,x0sq37,x0sq38,x0sq39,x0sqver,x0rb01,x0rb02,x0rb03,x0rb04,x0rb05,x0rb06,x0rb07,x0rb08,x0rb09,x0rb10,x0rb11,x0rb12,x0rb13,x0rb14,x0rb14a,x0rb15,x0rb15a,x0rbver,x0rd01,x0rd02,x0rd03,x0rd04,x0rd05,x0rd06,x0rd07,x0rd08,x0rd09,x0rd10,x0rdver,x0rr01,x0rr02,x0rr03,x0rr04,x0rr05,x0rr06,x0rr07,x0rr08,x0rr09,x0rr10,x0rr11,x0rr12,x0rrver,x0ds01,x0ds02,x0ds03,x0ds04,x0ds05,x0ds06,x0ds07,x0ds08,x0ds09,x0ds10,x0ds11,x0ds12,x0ds13,x0ds14,x0ds15,x0ds16,x0ds17,x0ds18,x0ds19,x0ds20,x0ds21,x0ds21a,x0ds22,x0ds22a,x0ds31,x0ds32,x0ds33,x0ds34,x0ds35,x0ds36,x0ds37,x0ds38,x0ds39,x0ds40,x0ds40a,x0dsver,x0au01,x0au02,x0au03,x0au04,x0au05,x0au06,x0au06a,x0au06b,x0au07,x0au08,x0au09,x0au10,x0au11,x0au12,x0au13,x0au14,x0au15,x0au16,x0au17,x0au18,x0au19,x0au20,x0au21,x0au22,x0au23,x0au24,x0au25,x0au26,x0au27,x0au28,x0au29,x0au30,x0au31,x0au32,x0au33,x0au34,x0au35,x0au35a,x0au35b,x0au35c,x0au36,x0au37,x0au38,x0auver,x0ff001,x0ff002,x0ff003,x0ff004,x0ff005,x0ff006,x0ff007,x0ff008,x0ff009,x0ff010,x0ff011,x0ff012,x0ff013,x0ff014,x0ff015,x0ff016,x0ff017,x0ff018,x0ff019,x0ff020,x0ff021,x0ff022,x0ff023,x0ff024,x0ff025,x0ff026,x0ff027,x0ff028,x0ff029,x0ff030,x0ff031,x0ff032,x0ff033,x0ff034,x0ff035,x0ff036,x0ff037,x0ff038,x0ff039,x0ff040,x0ff041,x0ff042,x0ff043,x0ff044,x0ff045,x0ff046,x0ff047,x0ff048,x0ff049,x0ff050,x0ff051,x0ff052,x0ff053,x0ff054,x0ff055,x0ff056,x0ff057,x0ff058,x0ff059,x0ff060,x0ff061,x0ff062,x0ff063,x0ff064,x0ff065,x0ff066,x0ff067,x0ff068,x0ff069,x0ff070,x0ff071,x0ff072,x0ff073,x0ff074,x0ff075,x0ff076,x0ff077,x0ff078,x0ff079,x0ff080,x0ff081,x0ff082,x0ff083,x0ff084,x0ff085,x0ff086,x0ff087,x0ff088,x0ff089,x0ff090,x0ff091,x0ff092,x0ff093,x0ff094,x0ff095,x0ff096,x0ff097,x0ff098,x0ff099,x0ff100,x0ff101,x0ff102,x0ff103,x0ff104,x0ff105,x0ff106,x0ff107,x0ff108,x0ff109,x0ff110,x0ff111,x0ff112,x0ff113,x0ff114,x0ff115,x0ff116,x0ff117,x0ff118,x0ff119,x0ff120,x0ff121,x0ff122,x0ff123,x0ff124,x0ff125,x0ff126,x0ff127,x0ff128,x0ff129,x0ff130,x0ff131,x0ff132,x0ff133,x0ff134,x0ff135,x0ff136,x0ff137,x0ff138,x0ff139,x0ff140,x0ff141,x0ff142,x0ff143,x0ff144,x0ff145,x0ff146,x0ff147,x0ff148,x0ff149,x0ff150,x0ff151,x0ff152,x0ff153,x0ff154,x0ff155,x0ff156,x0ff157,x0ff158,x0ff159,x0ff160,x0ff161,x0ff162,x0ff163,x0ff164,x0ff165,x0ff166,x0ff167,x0ff168,x0ff169,x0ff170,x0ff171,x0ff172,x0ff173,x0ff174,x0ff175,x0ff176,x0ff177,x0ff178,x0ff179,x0ff180,x0ff181,x0ff182,x0ff183,x0ff184,x0ff185,x0ff186,x0ff187,x0ff188,x0ff189,x0ff190,x0ff191,x0ff192,x0ff193,x0ff194,x0ff195,x0ff196,x0ff197,x0ff198,x0ff199,x0ff200,x0ff201,x0ff202,x0ff203,x0ff204,x0ff205,x0ff206,x0ff207,x0ff208,x0ff209,x0ff210,x0ff211,x0ff212,x0ff213,x0ff214,x0ff215,x0ff216,x0ff217,x0ff218,x0ff219,x0ff220,x0ff221,x0ff222,x0ff223,x0ff224,x0ff225,x0ff226,x0ff227,x0ff228,x0ff229,x0ff231,x0ff232,x0ff234,x0ff235,x0ff236,x0ff237,x0ff238,x0ff245,x0ff252,x0ff253,x0ff254,x0ff255,x0ff256,x0ff257,x0ff258,x0ff259,x0fflang,x0ffver,x0nu001,x0nu002,x0nu003,x0nu004,x0nu005,x0nu006a,x0nu006b,x0nu007,x0nu008,x0nu009,x0nu010,x0nu011,x0nu012,x0nu013,x0nu014,x0nu015,x0nu016,x0nu017,x0nu018,x0nu019a,x0nu019b,x0nu020a,x0nu020b,x0nu021a,x0nu021b,x0nu022a,x0nu022b,x0nu023a,x0nu023b,x0nu024a,x0nu024b,x0nu025a,x0nu025b,x0nu026a,x0nu026b,x0nu027a,x0nu027b,x0nu028a,x0nu028b,x0nu029,x0nu030,x0nu031,x0nu032,x0nu033,x0nu034,x0nu035,x0nu036,x0nu037,x0nu038,x0nu039,x0nu040,x0nu041,x0nu042,x0nu043,x0nu044,x0nu045,x0nu046,x0nu047,x0nu048,x0nu049,x0nu050,x0nu051,x0nu052,x0nu053,x0nu054,x0nu055,x0nu056,x0nu057,x0nu058,x0nu059,x0nu060,x0nu061,x0nu062,x0nu063,x0nu064,x0nu065,x0nu066,x0nu067,x0nu068,x0nu069,x0nu070,x0nu071,x0nu072,x0nu073,x0nu074,x0nu075,x0nu076,x0nu077,x0nu078,x0nu079,x0nu080,x0nu081,x0nu082,x0nu083,x0nu084,x0nu085,x0nu086,x0nu087,x0nu088,x0nu089,x0nu090,x0nu091,x0nu092,x0nu093,x0nu094,x0nu095,x0nu096,x0nu097,x0nu098,x0nu099,x0nu100,x0nu101,x0nu102,x0nu103,x0nu104,x0nu105,x0nu106,x0nu107,x0nu108,x0nu109,x0nu110,x0nu111,x0nu112,x0nu113,x0nu114,x0nu115,x0nu116,x0nu117,x0nu118,x0nu119,x0nu120,x0nu121,x0nu122,x0nu123,x0nu124,x0nu125,x0nu126,x0nu127,x0nu128,x0nu129,x0nu130,x0nu131,x0nu132,x0nu133,x0nu134,x0nu135,x0nu136,x0nu137,x0nu138,x0nu139,x0nu140,x0nu141,x0nu142,x0nu143,x0nu144,x0nu145,x0nu146,x0fl001,x0fl002,x0fl003,x0fl004,x0fl005,x0fl006,x0fl007,x0fl008,x0fl009,x0fl010,x0fl011,x0fl012,x0fl013,x0fl014,x0fl015,x0fl016,x0fl017,x0fl018,x0fl019,x0fl020,x0fl021,x0fl022,x0fl023,x0fl024,x0fl025,x0fl026,x0fl027,x0fl028,x0fl029,x0fl030,x0fl031,x0fl032,x0fl033,x0fl034,x0fl035,x0fl036,x0fl037,x0fl038,x0fl039,x0fl040,x0np00,x0np01,x0np02,x0np03,x0np03a,x0np03b,x0np03c,x0np03d,x0np04,x0np04a,x0np04b,x0np04c,x0np04d,x0np05,x0np05a,x0np05b,x0np06,x0np07,x0np07a,x0np07b,x0np08,x0np08a,x0np08b,x0np09,x0np09a,x0np09b,x0np09c,x0np09d,x0np10,x0np11,x0np12,x0np13,x0np14,x0np15,x0np16,x0np21,x0np22,x0np23,x0np24,x0np25,x0np26,x0np27,x0np28,x0np28a,x0np28b,x0np29,x0np30,x0np31,x0np32,x0np33,x0np34,x0np35,x0np36,x0npver,x0mp01,x0mp01a,x0mp01b,x0mp01c,x0mp02,x0mp02a,x0mp02b,x0mp02c,x0mp03,x0mp03a,x0mp03b,x0mp03c,x0mp04,x0mp04a,x0mp04b,x0mp04c,x0mp05,x0mp05a,x0mp05b,x0mp05c,x0mp06,x0mp06a,x0mp06b,x0mp06c,x0mp07,x0mp07a,x0mp07b,x0mp07c,x0mp08,x0mp08a,x0mp08b,x0mp08c,x0mp09,x0mp09a,x0mp09b,x0mp09c,x0mp10,x0mp10a,x0mp10b,x0mp10c,x0mp11,x0mp11a,x0mp11b,x0mp11c,x0mp12,x0mp12a,x0mp12b,x0mp12c,x0mp13,x0mp13a,x0mp13b,x0mp13c,x0mp14,x0mp14a,x0mp14b,x0mp14c,x0mp15,x0mp15a,x0mp15b,x0mp15c,x0mp16,x0mp16a,x0mp16b,x0mp16c,x0mp17,x0mp17a,x0mp17b,x0mp17c,x0mp18,x0mp18a,x0mp18b,x0mp18c,x0mp19,x0mp19a,x0mp19b,x0mp19c,x0mp20,x0mp20a,x0mp20b,x0mp20c,x0mp21,x0mp21a,x0mp21b,x0mp21c,x0mpver,x0hc01,x0hc02,x0hc03,x0hc04,x0hc05,x0hc06,x0hc07,x0hc08,x0hc09,x0hc10,x0hc11,x0hc12,x0hc13,x0hc14,x0hc15,x0hc16,x0hc17,x0hc18,x0hc19,x0hc20,x0hc21,x0hc22,x0hc23,x0hc24,x0hc25,x0hc26,x0hc27,x0hc28,x0hc29,x0hc30,x0hc31,x0hc32,x0hc33,x0hc34,x0hc35,x0hc36,x0hc37,x0hc38,x0hc39,x0hc40,x0hc41,x0hc42,x0hc43,x0hc44,x0hc45,x0hc46,x0hc47,x0hc48,x0hc49,x0hc50,x0hc51,x0hc52,x0hcver,x0bt01,x0bt02,x0bt03,x0bt04,x0bt05,x0bt06,x0bt07,x0bt08,x0bt09,x0bt10,x0bt11,x0bt12,x0bt13,x0bt14,x0bt15,x0bt16,x0bt17,x0bt18,x0bt19,x0bt20,x0bt21,x0bt22,x0bt23,x0bt24,x0bt25,x0bt26,x0bt27,x0bt28,x0bt29,x0bt30,x0bt31,x0bt32,x0bt33,x0bt34,x0bt35,x0bt36,x0bt37,x0bt38,x0bt39,x0bt40,x0btver,x0lo01,x0lo02,x0lo03,x0lo04,x0lo05,x0lo06,x0lo07,x0lo08,x0lo09,x0lo10,x0lo11,x0lo11a,x0lo11b,x0lo12,x0lover,x0pc01,x0pc02,x0pc03,x0pc04,x0pc05,x0pc06,x0pc07,x0pc08,x0pc09,x0pc10,x0pc11,x0pc12,x0pcver,x0ct07,x0ct11,x0ct18,x0ct24,x0ct26,x0ctver,x0md001,x0md002,x0md003,x0md004,x0md005,x0md006,x0md007,x0md008,x0md009,x0md010,x0md011,x0md012,x0md013,x0md014,x0md015,x0md015a,x0md016,x0md017,x0md018,x0md019,x0md020,x0md021,x0md022,x0md023,x0md024,x0md025,x0md026,x0md027,x0md028,x0md029,x0md030,x0md032,x0md033,x0md034,x0md035,x0md036,x0md037,x0md038,x0md039,x0md040,x0md041,x0md042,x0md043,x0md044,x0md045,x0md046,x0md047,x0md048,x0md049,x0md050,x0md051a,x0md051b,x0md051c,x0md051d,x0md051e,x0md058,x0md059,x0md060,x0md061,x0md062,x0md063,x0md064,x0md065,x0md066,x0md067,x0md073,x0md074,x0md075,x0md076,x0md081a,x0md081b,x0md081c,x0md081d,x0md081e,x0md081f,x0md081g,x0md081h,x0md081i,x0md083a,x0md083b,x0md083c,x0md083d,x0md083e,x0md084,x0md085,x0md086,x0md087,x0md088,x0md089,x0md090,x0md091,x0md092,x0md093,x0md094,x0md095,x0md096,x0md097,x0md098,x0md099,x0md100,x0md101,x0md102,x0md103,x0md104,x0md105,x0md106,x0md107,x0md108,x0md109,x0md110,x0md111,x0md112,x0md182,x0md183,x0md184,x0md185,x0md186,x0md187,x0md188,x0md189,x0md190,x0md191,x0md193,x0md194,x0md195,x0md197,x0md198,x0md199,x0md200,x0md201,x0md202,x0md203,x0md204,x0md205,x0md206,x0md207,x0md208,x0md209,x0md210,x0md211,x0md212,x0md213,x0md214,x0md215,x0md216,x0md217,x0md218,x0md219,x0md220,x0md221,x0md222,x0md223,x0md224,x0md225,x0md226,x0md227,x0md228,x0md229,x0md230,x0md231,x0md232,x0md233,x0md234,x0md235,x0md236,x0md237,x0md238,x0md239,x0md240,x0md241,x0md242,x0md243,x0md244,x0up01,x0up02,x0up03a,x0up03b,x0up03c,x0up03d,x0up03e,x0up04a,x0up04b,x0up05a,x0up05b,x0up05c,x0up05d,x0up05e,x0up06a,x0up06b,x0up07a,x0up07b,x0up08a,x0up08b,x0up09a,x0up09b,x0up10,x0up11,x0up12,x0up13,x0up14,x0up15,x0hy01,x0dc01,x0dc02,x0dc03,x0dc04,x0dc05,x0dc06,x0dc07,x0dclang,x0oh01,x0oh02a,x0oh02b,x0oh03a,x0oh03b,x0oh03c,x0oh03d,x0oh03e,x0oh03f,x0oh03g,x0oh03h,x0oh03i,x0oh03j,x0oh03k,x0oh03l,x0dd51,x0alver,firstname,lastname,lat,lon')


    with open("starter.txt", "a") as fd:
        fd.write('\n' + ','.join(patient))

    known_patients_csv = open("starter.txt", "r")

    #knowledge_base_csv = open(os.path.join(settings.BASE_DIR, 'diagnoseasy/db/generated_variables.csv'), "r")
    k_reader = csv.DictReader(known_patients_csv)
    #kb_reader = csv.DictReader(knowledge_base_csv)

    k_diabetic_patients, k_diabetic_multipliers, k_coronary_heart_disease_patients, k_coronary_heart_disease_multipliers = get_relevant_data(
        k_reader)


    # Turn dictionary into lists to make it like the format we had before
    k_diabetic_patients_list = [ [person['Sex'], person['Prescribed antihypertensive medication'],
                             person['Prescribed steroids'], person['Age'], person['BMI kg/m^2'],
                             person['Family history'], person['Smoking history'], person['Diabetic']] for person in k_diabetic_patients ]
    k_coronary_heart_disease_patients_list = [ [person['Age'], person['Total cholesterol mg/dL'],
                             person['HDL cholesterol mg/dL'], person['Systolic BP mm Hg'], person['Blood pressure being treated with medicines'],
                             person['Smoker'], person['ln(Age) x ln(Total cholesterol)'], person['ln(Age) x Smoker'],
                                                person['Sex'], person['Coronary heart disease']] for person in k_coronary_heart_disease_patients ]
    print("[+] Loaded known patients")

    diabetic_score = get_score(k_diabetic_patients_list[0], k_diabetic_multipliers, kb_diabetic_patients_list,
                               kb_diabetic_multipliers)
    coronary_heart_disease_score = get_score(k_coronary_heart_disease_patients_list[0], k_coronary_heart_disease_multipliers, kb_coronary_heart_disease_patients_list, kb_coronary_heart_disease_multipliers)
    #print("WARNING - Diabetic score: " + str(diabetic_score))
    #print("WARNING - Coronary Heart Disease score: " + str(coronary_heart_disease_score))

    data = {}
    person = k_diabetic_patients[0]
    if person['Sex'] == 0:
        person['Sex'] = 'Male'
    else:
        person['Sex'] = 'Female'

    if person['Prescribed antihypertensive medication'] == 0:
        person['Prescribed antihypertensive medication'] = 'No'
    else:
        person['Prescribed antihypertensive medication'] = 'Yes'

    if person['Prescribed steroids'] == 0:
        person['Prescribed steroids'] = 'No'
    else:
        person['Prescribed steroids'] = 'Yes'

    if person['Family history'] == 0:
        person['Family history'] = 'No diabetic 1st-degree relative'
    elif person['Family history'] == 0.728:
        person['Family history'] = 'Parent or sibling with diabetes'
    else:
        person['Family history'] = 'Parent and sibling with diabetes'

    if person['Smoking history'] == 0:
        person['Smoking history'] = 'Non-smoker'
    elif person['Smoking history'] == 0.728:
        person['Smoking history'] = 'Ex-smoker'
    else:
        person['Smoking history'] = 'Current smoker'


    data['info_diabetes'] = person
    person = k_coronary_heart_disease_patients[0]
    data['info_coronary_heart_disease'] = person
    data['diabetes'] = diabetic_score
    data['coronary_heart_disease'] = coronary_heart_disease_score

    print(data)
    et = time.time()
    print("Backend took: ",et-st)
    return data