from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_correlations(request):

    request_body = json.loads(request.body)
    person_info = request_body['info']

    print(person_info)

    # Could use some library, but it's 4:30AM so I'm not doing that
    csv_data = ''
    for f in person_info:
        csv_data += person_info[f] + ','
    csv_data = csv_data[:-1]

    print(csv_data)


    # Execute function based on condition, get and return results (i.e. possible correlations/conditions)

    return JsonResponse({})     # TODO: return useful data :)
