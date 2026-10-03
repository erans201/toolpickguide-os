@echo off
REM Launcher for Windows Task Scheduler. Runs auto_scheduler.py from this folder.
cd /d "%~dp0"
"C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe" auto_scheduler.py %*
