from django.urls import path
from . import views

urlpatterns = [
    path('admin-list/', views.gallery_list_admin, name='gallery_admin_list'),
    path('create/', views.gallery_create, name='gallery_create'),
    path('<int:pk>/update/', views.gallery_update, name='gallery_update'),
    path('<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
]
