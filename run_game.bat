@echo off
chcp 65001 >nul
echo =========================================
echo       Super Mario AI Visualizer 
echo =========================================

:: 1. Tim lenh Python hop le tren may
set PYTHON_CMD=

:: Uu tien kiem tra Microsoft Store Python truoc (nham tranh loi xung dot moi truong khac nhu MSYS2)
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD="%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
        goto :found_python
    )
)

:: Neu khong co ban Store, tim trong PATH cua he thong
for %%p in (py python python3) do (
    %%p --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=%%p
        goto :found_python
    )
)

:found_python
if "%PYTHON_CMD%"=="" (
    echo [X] LOI: Khong tim thay Python tren he thong!
    echo Vui long tai va cai dat Python tai: https://www.python.org/downloads/
    echo ^(Luu y: Nho tich vao o "Add Python to PATH" khi cai dat^)
    pause
    exit /b 1
)

echo [i] Su dung Python: %PYTHON_CMD%

:: 2. Tao moi truong ao (Virtual Environment)
if not exist "venv" (
    echo [i] Dang tao moi truong ao ^(venv^) de khong anh huong den he thong...
    %PYTHON_CMD% -m venv venv
)

:: 3. Tim duong dan Python cua moi truong ao
set VENV_PYTHON=
if exist "venv\Scripts\python.exe" (
    set VENV_PYTHON=venv\Scripts\python.exe
) else if exist "venv\bin\python.exe" (
    set VENV_PYTHON=venv\bin\python.exe
) else (
    echo [X] LOI: Moi truong ao duoc tao ra bi loi ^(Khong tim thay python.exe^).
    echo Vui long xoa thu muc "venv" va chay lai file nay.
    pause
    exit /b 1
)

:: 4. Cai dat cac thu vien can thiet tu requirements.txt
echo [i] Dang kiem tra va cai dat thu vien can thiet...
set PYTHONHTTPSVERIFY=0
"%VENV_PYTHON%" -m pip install --upgrade pip >nul 2>&1
"%VENV_PYTHON%" -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
set PYTHONHTTPSVERIFY=1

:: 5. Chay chuong trinh
echo.
echo [i] Dang khoi dong game...
"%VENV_PYTHON%" main.py

pause
