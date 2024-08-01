@echo off
cd "GUESS/src/"
set PATH=%PATH%;"C:\msys64\ucrt64\bin";"C:\msys64\ucrt64"
g++ targuess1_guess.cpp person.cpp timer.cpp personTran.cpp -o targuess1_guess

targuess1_guess.exe


exit 