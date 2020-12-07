@echo off

echo    DVS requires eceld-wireshark to work properly
echo    Please follow accept the prompt that will appear in your screen
echo    Please install using default configurations
echo    Install in C:\Program Files\Wireshark
pause
eceld-wireshark-installer\Wireshark-win64-3.2.5.exe
echo    Wireshark installation completed
echo    Installing Python's Virtual Environment Builder...
pip install virtualenv
echo    Creating virtual environment...
set VENV_NAME=dvs-venv
virtualenv "%VENV_NAME%"
echo    Activating virtual environment and installing python dependencies
%VENV_NAME%\Scripts\activate & pip install -r requirements.txt & echo ************************ & echo All dependencies where installed successfully & echo run 'main.py --no-sandbox' to start DVS