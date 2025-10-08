@echo off
echo ========================================
echo   Tagging LOCATIONS (LOC)
echo ========================================
call venv_loc\Scripts\activate
python tag_entities_direct.py %1 %2 LOC
call deactivate
pause