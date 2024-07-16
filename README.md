# Abstraction triumphs all 
# project PASSWORD GUESSING FOR FORENSIC 
## Installation 
conda create targuess_env python==3.10  (or 3.10.14)
conda install conda-forge::gradio

conda install conda-forge::matplotlib

conda install conda-forge::unidecode

pip install fastapi, uvicorn, pydantic
## Usage 
### Training 
**training and move model trained to ./GUESS**
```
train_command.bat 
```
### Run app 
```
activate_app.bat
```
```
python api.py
```



python server_api.py

## Utilities 
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

### create txt for (training) from tailieu leak csv 
python TRAIN\src\tailieuvn_data\create_train_dataset.py



### before training:
**have a raw csv file**
**cd process_name**
**python process_name.py -> to create a process_name/output.txt**
**cd ..**
**with this txt file , below script create a dict to fix name and do stuffs**
**python TRAIN\src\tailieuvn_data\create_train_dataset.py**
