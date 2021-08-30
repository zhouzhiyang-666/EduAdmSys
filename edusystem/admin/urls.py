from django.urls import path
from admin import views

urlpatterns = [
    path('login/', views.login),
    path('getDptName/', views.getDptName),
    path('getStuData/', views.getStuData),
    path('getAllClass/', views.getAllClass),
    path('editStu/', views.editStu),
    path('addStu/', views.addStu),
    path('delStu/', views.delStu),
    path('batchDelStu/', views.batchDelStu),
    path('uploadStuFiles/', views.uploadStuFiles),

    path('getTeaData/', views.getTeaData),
    path('editTea/', views.editTea),
    path('addTea/', views.addTea),
    path('delTea/', views.delTea),
    path('batchDelTea/', views.batchDelTea),
    path('uploadTeaFiles/', views.uploadTeaFiles),

    path('getCourseInfo/', views.getCourseInfo),
    path('addCourse/', views.addCourse),
    path('editCourse/', views.editCourse),
    path('delCourse/', views.delCourse),
    path('batchDelCourse/', views.batchDelCourse),
    path('uploadCourse/', views.uploadCourse),

    path('getRoleData/', views.getRoleData),
    path('addAdmin/', views.addAdmin),
    path('delAdmin/', views.delAdmin),
    path('batchDelAdm/', views.batchDelAdm),
    path('upToSuperAdmin/', views.upToSuperAdmin),
    path('upToAdmin/', views.upToAdmin),

    path('getCrsArrange/', views.getCrsArrange),
    path('uploadCourseArrange/', views.uploadCourseArrange),
    path('loadButton/', views.loadButton),
    path('getTeaName/', views.getTeaName),
    path('getCourseName/', views.getCourseName),
    path('editCrsArrange/', views.editCrsArrange),
    path('delCrsArrange/', views.delCrsArrange),
    path('batchDelCourseArrange/', views.batchDelCourseArrange),
    path('openOrCloseStuSelect/', views.openOrCloseStuSelect),
    path('getActiveSelect/', views.getActiveSelect),

    path('addClass/', views.addClass),
    path('delClass/', views.delClass),
    path('editClass/', views.editClass),
    path('batchDelClass/', views.batchDelClass),
    path('uploadClass/', views.uploadClass),

    path('test/', views.test),

]
