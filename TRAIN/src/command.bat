@echo off
cd "TRAIN\src\"
g++ targuess1_train.cpp person.cpp timer.cpp -o targuess1_train
echo Waiting for 5 seconds...
timeout /t 15 /nobreak
targuess1_train.exe
cd ..
cd ..
pause