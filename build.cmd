@echo off

echo ----- Starting build -----

pyinstaller --onefile sif.py

if %ERRORLEVEL% neq 0 goto :error
goto :complete

:complete
echo ----- Build completed -----
exit

:error
echo ----- Build failed -----
exit
