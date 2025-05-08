@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Building executable...
pyinstaller --onefile --windowed --icon=icon.ico file_blocker.py

echo Done! The executable is in the 'dist' folder.
