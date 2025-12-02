@echo off
REM 1 generate and activate virtiual enviroment
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate

REM 2 install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM 3 start app
python app.py
pause
