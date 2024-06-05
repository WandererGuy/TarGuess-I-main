@echo off
cd "GUESS\src\"
g++ targuess1_guess.cpp person.cpp timer.cpp personTran.cpp -o targuess1_guess

targuess1_guess.exe
exit