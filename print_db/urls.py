from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('event/', views.event, name='event'),
        path('place/', views.place, name='place'),
        path('imply/', views.imply, name='imply'),
        path('insert_event/', views.insert_event, name='insert_event'),
        path('insert_place/', views.insert_place, name='insert_place'),
]
