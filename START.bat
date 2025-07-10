@echo off
python -m pip install pip --upgrade
python -m pip install pandas --upgrade
python -m pip install openpyxl --upgrade
cls
rem Starting program silently, please wait...
start "" pythonw "Main.py"