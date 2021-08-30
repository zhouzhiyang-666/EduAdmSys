@echo off 

start cmd /k "cd /d D:\software\ResidServer\Redis-x64-3.2.100 (1)&&redis-server.exe"

TIMEOUT /T 2 /NOBREAK

start cmd /k "cd /d D:\bishe\EduAdmSys\edumanage\edusystem&&python manage.py runserver 9090"