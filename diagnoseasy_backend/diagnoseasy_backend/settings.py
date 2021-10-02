"""
Django settings for diagnoseasy_backend project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import csv
import math
import time

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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

        # Age

        tmp_mult.append(0.063)

        # BMI
        tmp_mult.append(1)
        if person['BMI kg/m^2'] < 25:
            person['BMI kg/m^2'] = 0
        elif person['BMI kg/m^2'] >= 25 and person['BMI kg/m^2'] < 27.5:
            person['BMI kg/m^2'] = 0.699
        elif person['BMI kg/m^2'] >= 27.5 and person['BMI kg/m^2'] < 30:
            person['BMI kg/m^2'] = 1.97
        else:
            person['BMI kg/m^2'] = 2.518

        # Family history
        tmp_mult.append(1)
        if person['Family history'] == 0:
            person['Family history'] = 0
        elif person['Family history'] == 1:
            person['Family history'] = 0.728
        else:
            person['Family history'] = 0.753

        # Smoking history
        tmp_mult.append(1)
        if person['Smoking history'] == 0:
            person['Smoking history'] = 0.855
        else:
            person['Smoking history'] = 0
        multipliers.append(tmp_mult)
        # Diabetic
        if person['Diabetic'] == 2:
            person['Diabetic'] = 1
        else:
            person['Diabetic'] = 0
    return diabetic_patients, multipliers

# https://www.mdcalc.com/framingham-risk-score-hard-coronary-heart-disease#evidence
def normalize_coronary_heart_parameters(coronary_heart_disease_patients):
    multipliers = []
    male_mult = [52.00961, 20.014077, -0.905964, 1.305784, 0.241549, 12.096316, -4.605038, -2.84367, -2.93323]
    female_mult = [31.764001, 22.465206, -1.187731, 2.552905, 0.420251, 13.07543, -5.060998, -2.996945]
    for x in coronary_heart_disease_patients:
        if x['Age'] == 0:
            # Male
            multipliers.append(male_mult)
        else:
            multipliers.append(female_mult)

    return coronary_heart_disease_patients, multipliers



def get_relevant_data(reader):
    diabetic_patients = []

    # Diabetic data
    age = 'x0_age'
    bmi = 'x0an03a'
    sex = 'x0_sex'
    diabetes = 'x0md030'
    antihypertensive_medication = 1  # random.randint(0,1)
    prescribed_steroids = 1  # random.randint(0,1)
    smoking = 'x0sm00'
    family_history = 0.753  # random.choice([0,0.728,0.753])
    date_of_birth = 'x0_birthd'
    firstname = 'firstname'
    lastname = 'lastname'

    coronary_heart_disease_patients = []
    total_cholesterol = 'x0lp16'
    cholesterol_HDL = 'x0lp17'
    systolic_BP = 'x0bp01'
    treated_for_blood_pressure = 'x0bl02'
    coronary_heart_disease = 'x0mi08'

    for row in reader:

        diabetic_patient_data = {
            'Sex': int(row[sex]) - 1,
            'Prescribed antihypertensive medication': antihypertensive_medication,
            'Prescribed steroids': prescribed_steroids,
            'Age': float(row[age]),
            'BMI kg/m^2': float(row[bmi]),
            'Family history': family_history,
            'Smoking history': int(row[smoking]) - 1,
            'Diabetic': int(row[diabetes]),
            'Day of birth' : row[date_of_birth],
            'Firstname' : row[firstname],
            'Lastname' : row[lastname]
        }

        insert = True
        for x in diabetic_patient_data.keys():
            d = diabetic_patient_data[x]
            if (isinstance(d, int) or isinstance(d, float))  and d < 0:
                insert = False
                break

        if insert:
            diabetic_patients.append(diabetic_patient_data)


        coronary_heart_disease_patient_data = {
            'Age': float(row[age]),
            'Total cholesterol mg/dL': int(row[total_cholesterol]),
            'HDL cholesterol mg/dL': int(row[cholesterol_HDL]),
            'Systolic BP mm Hg': int(row[systolic_BP]),
            'Blood pressure being treated with medicines': int(row[treated_for_blood_pressure]),
            'Smoker': int(row[smoking]),
            'Sex': int(row[sex]) - 1,
            'Coronary heart disease': int(row[coronary_heart_disease]),
            'ln(Age) x ln(Total cholesterol)': 0,
            'ln(Age) x Smoker': 0,
            'ln(Age) x ln(Age)': 0,
            'Day of birth': row[date_of_birth],
            'Firstname': row[firstname],
            'Lastname': row[lastname]
        }

        insert = True
        for x in coronary_heart_disease_patient_data.keys():
            d = coronary_heart_disease_patient_data[x]
            if (isinstance(d, int) or isinstance(d, float))  and d < 0:
                insert = False
                break
        if insert:
            if coronary_heart_disease_patient_data['Blood pressure being treated with medicines'] == 2:
                coronary_heart_disease_patient_data['Blood pressure being treated with medicines'] = 0

            if coronary_heart_disease_patient_data['Smoker'] == 2:
                coronary_heart_disease_patient_data['Smoker'] = 0
            else:
                coronary_heart_disease_patient_data['Smoker'] = 1

            coronary_heart_disease_patient_data['ln(Age) x Smoker'] = math.log(
                coronary_heart_disease_patient_data['Age']) * coronary_heart_disease_patient_data['Smoker']

            if coronary_heart_disease_patient_data['Age'] > 70 and coronary_heart_disease_patient_data['Sex'] == 0:
                coronary_heart_disease_patient_data['ln(Age) x Smoker'] = math.log(70) * \
                                                                          coronary_heart_disease_patient_data['Smoker']
            if coronary_heart_disease_patient_data['Age'] > 78 and coronary_heart_disease_patient_data['Sex'] == 1:
                coronary_heart_disease_patient_data['ln(Age) x Smoker'] = math.log(78) * \
                                                                          coronary_heart_disease_patient_data['Smoker']

            coronary_heart_disease_patient_data['Age'] = math.log(coronary_heart_disease_patient_data['Age'])
            coronary_heart_disease_patient_data['Total cholesterol mg/dL'] = math.log(
                coronary_heart_disease_patient_data['Total cholesterol mg/dL'])
            coronary_heart_disease_patient_data['HDL cholesterol mg/dL'] = math.log(
                coronary_heart_disease_patient_data['HDL cholesterol mg/dL'])
            coronary_heart_disease_patient_data['Systolic BP mm Hg'] = math.log(
                coronary_heart_disease_patient_data['Systolic BP mm Hg'])
            coronary_heart_disease_patient_data['ln(Age) x ln(Total cholesterol)'] = \
            coronary_heart_disease_patient_data['Age'] * coronary_heart_disease_patient_data['Total cholesterol mg/dL']

            coronary_heart_disease_patient_data['ln(Age) x ln(Age)'] = coronary_heart_disease_patient_data['Age'] ** 2

            coronary_heart_disease_patients.append(coronary_heart_disease_patient_data)

    diabetic_patients, diabetic_multipliers = normalize_diabetics_parameters(diabetic_patients)

    coronary_heart_disease_patients, coronary_heart_disease_multipliers = normalize_coronary_heart_parameters(
        coronary_heart_disease_patients)

    return diabetic_patients, diabetic_multipliers, coronary_heart_disease_patients, coronary_heart_disease_multipliers

st = time.time()
knowledge_base_csv = open(os.path.join(BASE_DIR, 'diagnoseasy/db/generated_variables.csv'), "r")

kb_reader = csv.DictReader(knowledge_base_csv)

kb_diabetic_patients, kb_diabetic_multipliers, kb_coronary_heart_disease_patients, kb_coronary_heart_disease_multipliers = get_relevant_data(kb_reader)

print("[+] Loaded knowledgebase")
kb_diabetic_patients_list = [[person['Sex'], person['Prescribed antihypertensive medication'],
                              person['Prescribed steroids'], person['Age'], person['BMI kg/m^2'],
                              person['Family history'], person['Smoking history'], person['Diabetic']] for person in
                             kb_diabetic_patients]

kb_coronary_heart_disease_patients_list = [[person['Age'], person['Total cholesterol mg/dL'],
                                           person['HDL cholesterol mg/dL'], person['Systolic BP mm Hg'],
                                           person['Blood pressure being treated with medicines'],
                                           person['Smoker'], person['ln(Age) x ln(Total cholesterol)'],
                                           person['ln(Age) x Smoker'],
                                           person['Sex'], person['Coronary heart disease']] for person in
                                          kb_coronary_heart_disease_patients]
et = time.time()
print("Loading took: " , et-st)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^bjdo0!g&5guc)_2@fcr52(=+fbl(oqoo3pe$0_jp9rh2_25)o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'diagnoseasy_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'diagnoseasy_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
