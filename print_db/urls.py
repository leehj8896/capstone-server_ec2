from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('event/', views.event, name='event'),
        path('place/', views.place, name='place'),
        path('imply/', views.imply, name='imply'),
        path('insert_event/', views.insert_event, name='insert_event'),
        path('insert_place/', views.insert_place, name='insert_place'),
        path('participate_event/', views.participate_event, name='participate_event'),
        path("insert_user/", views.insert_user, name="insert_user"),        
        path("insert_user_direct/", views.insert_user_direct, name="insert_user_direct"),
        path("id_duplicate_check/", views.id_duplicate_check, name="id_duplicate_check"),
        path("login/", views.login, name="login"),
]
