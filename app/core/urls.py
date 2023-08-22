from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('tasks/status/', Ready.as_view()),
    path('tasks/<int:pk>/<int:sub_pk>', SubtaskReady.as_view()),
    path('tasks/', ListMainTask.as_view()),

    #http://localhost:5001/api/v1/tasks/status
    
    
    #token auth
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    #unused
    # path('tasks/create', CreateMainTask.as_view()),
    # path('tasks/delete/<int:pk>', DeleteMainTask.as_view()),
    # path('tasks/<int:pk>/<int:sub_pk>', DetailSubTask.as_view()),
]