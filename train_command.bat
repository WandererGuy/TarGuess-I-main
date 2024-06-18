@REM ---- train from raw csv of tailieu leak 
@REM # fill plain password (cracked md5) in new csv, 
@REM # refine csv (unicode), 
@REM # create txt file for training from csv , 
@REM # train, 
@REM # move file output to GUESS, 
@REM # re-order pattern in file>


@echo off
cd "TRAIN\src"
echo Compiling the program...
g++ targuess1_train.cpp person.cpp timer.cpp -o targuess1_train
echo Running the program...
targuess1_train.exe
echo Moving output file...
cd ..
cd ..
move "TRAIN\src\OUTPUT_TRAIN.txt" "GUESS\src\result_folder"
echo re-order pattern file output...
timeout /t 5 /nobreak
call conda activate D:\_work_\2024\MANH\current-project\PASS-GUESS-project\targuess\TarGuess-I-main\targuess_env
python GUESS\src\b_create_new_rule.py
echo copy person.cpp to GUESS to apply new rule 
copy "TRAIN\src\person.cpp" "GUESS\src"
echo All Done. Please exit.
pause