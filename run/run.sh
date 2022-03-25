#!/bin/bash
possible_ver=(python3.10\ py\ python3\ python)
pyupdate=" -m pip install --upgrade -r requirements.txt"
pyargs=" -m src.main.main"

# debería de pararse en la carpeta raíz del proyecto
if [[ $PWD == *run ]]
then
    cd ..
fi

for ver in $possible_ver
do
    echo -e "\n\ntrying with '$ver'...\n"
    $ver$pyupdate
    $ver$pyargs
    if [[ $? == 0 ]]
    then
        break
    fi
done
