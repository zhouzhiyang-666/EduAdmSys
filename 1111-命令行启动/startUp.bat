@echo off 

cd /d %~dp0

start cmd /k "python tools/infer/predict_system.py"
