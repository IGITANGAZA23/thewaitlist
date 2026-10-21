from django.urls import path
from .views import hello, second_method

urlpatterns = [
    path('', hello, name='hello'),
    path('second/', second_method, name='second_method'),
]