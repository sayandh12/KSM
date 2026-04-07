from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_study_list, name='case_studies_list'),
    path('admin-list/', views.case_study_list_admin, name='case_studies_admin_list'),
    path('create/', views.case_study_create, name='case_study_create'),
    path('<int:pk>/update/', views.case_study_update, name='case_study_update'),
    path('<int:pk>/delete/', views.case_study_delete, name='case_study_delete'),
]
