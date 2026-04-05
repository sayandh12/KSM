from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_study_list, name='case_studies_list'),
]
