from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('event/', views.event, name='event'),
        path('place/', views.place, name='place'),
        path('event_has_place/', views.event_has_place, name='event_has_place')
]
