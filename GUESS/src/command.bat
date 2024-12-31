@echo off
cd "GUESS"
cd "src"
setlocal
@REM read from config file 
@REM for /f "usebackq tokens=1,2 delims==" %%a in ("../../config/config_setup_cpp.txt") do (
@REM    if "%%a"=="PATH" set "PATH_VALUE=%%b"
@REM)
@REM echo The PATH value is: %PATH_VALUE%
@REM set PATH=%PATH_VALUE%
g++ targuess1_guess.cpp person.cpp timer.cpp personTran.cpp -o targuess1_guess
targuess1_guess.exe
exit 