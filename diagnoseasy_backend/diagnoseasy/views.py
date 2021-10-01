from django.shortcuts import render

def get_correlations(request):

    person_condition = request.GET.get('condition', '')  # Field name might change, 'condition' is a placeholder
    person_info = request.POST.get('info', '')  # Field name might change, 'info' is a placeholder

    # Execute function based on condition, get and return results (i.e. possible correlations/conditions)
