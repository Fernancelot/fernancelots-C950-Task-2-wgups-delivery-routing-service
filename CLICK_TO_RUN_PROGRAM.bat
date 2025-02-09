@echo off
if not "%1" == "max" start /MAX cmd /c %0 max
python main.py
echo "test"
pause