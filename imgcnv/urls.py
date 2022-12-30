from django.urls import path
from . import views

app_name='imgcnv'
urlpatterns=[
    path('index/',views.index,name='index'),
]