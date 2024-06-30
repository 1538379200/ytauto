@echo off

chcp 65001

set /p ip=请输入当前设备IPV4地址：

cd files
echo ======================== 开始安装python3.12 ===========================
call python-3.12.4-amd64.exe /passive InstallAllUsers=1 SimpleInstall=1
timeout /t 3 /nobreak
REM setx /M Path "%Path%;%ProgramFiles%\Python312"
setx /m Path "%Path%;C:\Program Files\Python312;C:\Program Files\Python312\Scripts"
timeout /t 3 /nobreak
echo ======================== 刷新环境变量 ==============================
cd ..
call refreshenv.bat
echo ======================== 开始安装poetry环境 ===========================
call pip install -i https://pypi.tuna.tsinghua.edu.cn/simple poetry
echo ======================== 开始项目环境安装 =============================
call poetry install
echo ======================== 开始启动Socket监听 ===========================
cd ytauto
call poetry run python listener.py --host=%ip%



