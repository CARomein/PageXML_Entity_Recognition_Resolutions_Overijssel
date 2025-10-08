@echo off
echo ========================================
echo   Tagging DATES (DAT)
echo ========================================
call venv_dat\Scripts\activate
python tag_entities_direct.py %1 %2 DAT
call deactivate
pause