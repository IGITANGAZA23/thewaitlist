from django.urls import path
from .views import view_one, view_two

urlpatterns = [
    path('one/', view_one, name='view_one'),
    path('two/', view_two, name='view_two'),
]
