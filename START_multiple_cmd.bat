@echo off

REM Path to your Conda executable (adjust if necessary)
REM set CONDA_EXE=C:\Users\YourUsername\Anaconda3\Scripts\activate.bat

REM Path to your Conda environment
set current_dir=%~dp0
set CONDA_ENV_PATH=%current_dir%targuess_env
REM Path to your Python script
set SCRIPT_PATH_0=main.py
set SCRIPT_PATH_1=main_validate.py


start "main.py" cmd /k "call conda activate "%CONDA_ENV_PATH%" && python "%SCRIPT_PATH_0%""

REM Open second terminal
REM start "main_validate.py" cmd /k "call conda activate "%CONDA_ENV_PATH%" && python "%SCRIPT_PATH_1%""
