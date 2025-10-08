@echo off
echo ========================================
echo   Tagging PERSONS (PER)
echo ========================================
call venv_per\Scripts\activate
python tag_entities_direct.py %1 %2 PER
call deactivate
pause