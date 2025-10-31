@echo off
echo Compilando CambiadorDeFondo...

REM Copiar pystray manualmente
set PYSTRAY_PATH=C:\Users\USUARIO\AppData\Roaming\Python\Python314\site-packages\pystray

pyinstaller --onedir ^
    --windowed ^
    --name=CambiadorDeFondo ^
    --icon=assets/icon.ico ^
    --collect-all=customtkinter ^
    --collect-all=darkdetect ^
    --collect-all=PIL ^
    --collect-submodules=six ^
    --add-data=assets;assets ^
    --add-data=modules;modules ^
    --add-data=%PYSTRAY_PATH%;pystray ^
    --distpath=dist ^
    --workpath=build ^
    --clean ^
    --noconfirm ^
    main.py

echo.
echo Copiando dependencias adicionales...
xcopy /E /I /Y "%PYSTRAY_PATH%" "dist\CambiadorDeFondo\_internal\pystray"

echo.
echo Compilacion completada!
echo Ejecutable en: dist\CambiadorDeFondo\CambiadorDeFondo.exe
pause
