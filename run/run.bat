@echo off
set possible_ver= python3.10 py python3 python
set pyupdate= -m pip install --upgrade -r requirements.txt
set pyargs= -m src.main.main

@REM debería de pararse en la carpeta raíz del proyecto
if %CD:~-3% == run (
    cd ..
)

for %%v in (%possible_ver%) do (
    echo: & echo: & echo Trying with '%%v'...& echo:
    %%v%pyupdate%%reqpath%
    %%v%pyargs%
    if not errorlevel 1 goto:EOF
)
