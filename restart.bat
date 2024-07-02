@echo off

set /p ip = Insert your ip: 



cd %USERPROFILE%\Documents\YTAuto\ytauto

start "YTListener" /min poetry run python listener.py --host=%ip%
