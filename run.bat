@echo off
echo Setting up dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Running HoloWatcher...
cd HoloWatcher
cls
py main.py
pause
