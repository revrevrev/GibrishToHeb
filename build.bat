@echo off
echo Installing dependencies...
pip install pyinstaller pystray Pillow

echo.
echo Building exe...
pyinstaller GibrishToHeb.spec
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo Building installer...
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    echo ERROR: Inno Setup not found.
    echo Download it from: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

%ISCC% installer.iss
if errorlevel 1 (
    echo ERROR: Installer build failed.
    pause
    exit /b 1
)

echo.
echo Cleaning up intermediate files...
del /q dist\GibrishToHeb.exe

echo.
echo Done! Installer is at: dist\GibrishToHeb_Setup.exe
