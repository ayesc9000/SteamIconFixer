@echo off

echo ----- Starting build -----

pyinstaller --onefile sif.py
if %ERRORLEVEL% neq 0 goto :error
echo ----- Build completed -----
exit

:error
echo ----- Build failed -----
echo If you got an unrecognized command error, make sure your Python scripts directory is in your PATH. Refer to the pyinstaller documentation for more information:
echo https://pyinstaller.org/en/stable/installation.html#pyinstaller-not-in-path
exit
