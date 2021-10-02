from django.shortcuts import render
from django.http import HttpResponse

import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import csv
import json

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def get_info(request):

    request_body = json.loads(request.body)
    person_cf = request_body['cf']
    print (person_cf)

    person_info = {}
    with open(os.path.join(settings.BASE_DIR, 'ssn/db/ssn_dataset.csv'), mode='r') as f:
        csv_reader = csv.DictReader(f)
        lines_c = 0
        for row in csv_reader:
            if row['cf'].lower() == person_cf.strip().lower():
                person_info = row
                break
    return JsonResponse(person_info)
