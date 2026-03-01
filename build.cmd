@echo off

echo ----- Starting build -----

pyinstaller --onefile sif.py
if %ERRORLEVEL% neq 0 goto :error
echo ----- Build completed -----
exit

:error
echo ----- Build failed -----
exit
> [!NOTE]
> Quotations are only necessary if the path contains spaces.