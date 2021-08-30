from django.urls import path
from public import views

urlpatterns = [
    path('checkcode/', views.checkcode),
    path('getResetPwdCode/', views.getResetPwdCode),
    path('ResetPwdByInfo/', views.ResetPwdByInfo),

    path('test_term/', views.test_term),
    path('getStuScore/', views.getStuScore),
    path('getTermCourse/', views.getTermCourse),
    path('login/', views.login),
    path('getRoomCourse/', views.getRoomCourse),
    path('getRoomByArea/', views.getRoomByArea),
    path('logout/', views.logout),
    path('changePwd/', views.changePwd),
    path('getRoute/', views.getRoute),
    path('changePhone/', views.changePhone),
    path('getPhoneCode/', views.getPhoneCode),



]