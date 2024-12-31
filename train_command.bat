@REM ---- train from raw csv of tailieu leak 
@REM # fill plain password (cracked md5) in new csv, 
@REM # refine csv (unicode), 
@REM # create txt file for training from csv , 
@REM # train, 
@REM # move file output to GUESS, 
@REM # re-order pattern in file
@REM Path to the config file



@echo off
del TRAIN\src\OUTPUT_TRAIN.txt
del GUESS\src\train_result\OUTPUT_TRAIN.txt
cd "TRAIN\src"
echo Compiling the program...
g++ targuess1_train.cpp person.cpp timer.cpp -o targuess1_train
echo Running the program...
targuess1_train.exe
echo write result in TRAIN/src/OUTPUT_TRAIN.txt
timeout /t 5 /nobreak
echo copy output file...
cd ..
cd ..
copy "TRAIN\src\OUTPUT_TRAIN.txt" "GUESS\src\train_result"
timeout /t 5 /nobreak
echo copy person.cpp to GUESS to apply new rule 
copy "TRAIN\src\person.cpp" "GUESS\src"
echo All Done. Please exit.
timeout /t 3 /nobreak

exit