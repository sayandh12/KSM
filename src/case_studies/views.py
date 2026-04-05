from django.shortcuts import render

def case_study_list(request):
    return render(request, 'case_studies/list.html')
