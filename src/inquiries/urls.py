from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.enquiry_list, name='enquiry_list'),
    path('<int:pk>/', views.enquiry_view, name='enquiry_view'),
    path('<int:pk>/delete/', views.enquiry_delete, name='enquiry_delete'),
]
