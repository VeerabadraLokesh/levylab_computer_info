@setlocal enableextensions
@cd /d "%~dp0"

python -m pip install -r requirements.txt

mkdir "%ProgramFiles%\system_info\"

copy "pgpass.conf" "%ProgramFiles%\system_info\"
copy "system_info.py" "%ProgramFiles%\system_info\"

copy "system_info.bat" "%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup\"

pause
