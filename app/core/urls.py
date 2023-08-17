from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('tasks/<int:pk>/', DetailGlobalTask.as_view()),
    path('tasks/', ListGlobalTask.as_view()),
    
    #token auth
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    #unused
    path('tasks/create', CreateGlobalTask.as_view()),
    path('tasks/delete/<int:pk>', DeleteGlobalTask.as_view()),
]