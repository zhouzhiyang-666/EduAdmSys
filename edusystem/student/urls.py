from django.urls import path
from student import views

urlpatterns = [
    path('test/', views.test),
    path('getScoreTable/', views.getScoreTable),
    path('getSelfInfo/', views.getSelfInfo),
    path('getNewCourseArrange/', views.getNewCourseArrange),
    path('addSelectCourse/', views.addSelectCourse),
    path('delSelectCourse/', views.delSelectCourse),
    path('getSelectedCourseArrange/', views.getSelectedCourseArrange),
    # path('delSelectCourse/', views.delSelectCourse),
    # path('delSelectCourse/', views.delSelectCourse),
    # path('delSelectCourse/', views.delSelectCourse),
    # path('delSelectCourse/', views.delSelectCourse),

]