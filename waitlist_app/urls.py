from django.urls import path
from . import views

urlpatterns = [
    path('', views.waitlist_list, name='waitlist_list'),
    path('add/', views.waitlist_create, name='waitlist_create'),
    path('edit/<int:pk>/', views.waitlist_update, name='waitlist_update'),
    path('delete/<int:pk>/', views.waitlist_delete, name='waitlist_delete'),
]
