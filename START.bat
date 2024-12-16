@echo off
setlocal
set current_dir=%~dp0
call conda activate "%current_dir%targuess_env"
python main.py
