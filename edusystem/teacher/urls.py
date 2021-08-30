from django.urls import path
from teacher import views

urlpatterns = [
    path('course/', views.course),
    path('getStuScore/', views.getStuScore),
    path('getInfo/', views.getInfo),
    path('getCourse/', views.getCourse),
    path('getScoreData/', views.getScoreData),
    path('postScoreList/', views.postScoreList),
    # path('logout/', views.logout),
]