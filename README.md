# project PASSWORD GUESSING FOR FORENSIC 
## Installation 
conda create -p ..... targuess_env python==3.10  (or 3.10.14)
conda install conda-forge::gradio matplotlib unidecode


pip install fastapi uvicorn pydantic



### set up C++ for VScode (don't need anymore since using python code)
install extension Code Runner + C++ in Vscode 
download msys2 and run ... add .. to become environment path (like https://code.visualstudio.com/docs/languages/cpp)
copy file libstdc++-6.dll file somewhere in /ucrt folder (usually in "C:\msys64\ucrt64\bin\libstdc++-6.dll")
then put it into C++ run code folder(GUESS/src/ and TRAIN/src) 
fix path in config/config_setup_cpp.txt (so that can use g++ in C++ session)


For reference:
https://code.visualstudio.com/docs/languages/cpp
Download msys2 MSYS2 on its website for newest
https://www.freecodecamp.org/news/how-to-install-c-and-cpp-compiler-on-windows/
C++ programming with Visual Studio Code

exe error 
place libstdc++-6.dll file somewhere in /ucrt folder into C++ run code folder(GUESS/src/)
https://stackoverflow.com/questions/74734500/cant-find-entry-point-zst28-throw-bad-array-new-lengthv-in-dll-filepath


## prepare env
```
conda env create -f environment.yml
```

## Usage 
### Training 
### RUN REAL (with produced weight aka a probility file GUESS\src\result_folder\new_order.txt with password have PII in it , and GUESS\src\result_folder\trawling.txt without PII )
```
conda activate path_to_targuess_env
python main.py
```
or <br>
```
START.bat
```


## Other Utilities 
### format_finder.py 
is for format translation, so change person.cpp rule , require change manually format_finder.py as well


### create pcfg my way , better (for fill in mask, remove clutter personal info)
cd my_pcfg_method
python my_extract_method.py

### clean and fix name from raw csv 
**this can also for create clue for password , disable remove duplicate**
**make fix name into output.txt, later for create dict to look up for create better csv from tailieu leak csv**
cd process_name 
python process_name.py





