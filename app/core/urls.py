from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('<int:pk>/', DetailToDo.as_view()),
    path('', ListToDo.as_view()),
    path('create', CreateToDo.as_view()),
    path('delete/<int:pk>', DeleteToDo.as_view()),
    #token auth
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]