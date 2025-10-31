@echo off
echo ========================================
echo   Compilando con rutas absolutas
echo ========================================
echo.

REM Obtener la ruta actual
set CURRENT_DIR=%CD%

echo Directorio actual: %CURRENT_DIR%
echo.

REM Compilar con rutas absolutas
pyinstaller --onedir ^
    --windowed ^
    --name=CambiadorDeFondo ^
    --icon=%CURRENT_DIR%\assets\icon.ico ^
    --paths=%CURRENT_DIR% ^
    --paths=%CURRENT_DIR%\modules ^
    --collect-all=pystray ^
    --collect-all=customtkinter ^
    --collect-all=darkdetect ^
    --collect-all=PIL ^
    --collect-submodules=pystray ^
    --hidden-import=six ^
    --hidden-import=pystray ^
    --hidden-import=pystray._win32 ^
    --hidden-import=pystray._util ^
    --hidden-import=pystray._util.win32 ^
    --add-data=%CURRENT_DIR%\assets;assets ^
    --add-data=%CURRENT_DIR%\modules;modules ^
    --distpath=%CURRENT_DIR%\dist ^
    --workpath=%CURRENT_DIR%\build ^
    --specpath=%CURRENT_DIR% ^
    --clean ^
    --noconfirm ^
    %CURRENT_DIR%\main.py

echo.
echo ========================================
echo   Compilacion completada!
echo   Ejecutable: %CURRENT_DIR%\dist\CambiadorDeFondo\CambiadorDeFondo.exe
echo ========================================
echo.
pause
