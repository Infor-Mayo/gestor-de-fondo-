@echo off
echo ========================================
echo Instalador de Cambiador de Fondo
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo Python detectado correctamente
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalación completada exitosamente!
echo ========================================
echo.
echo Para ejecutar la aplicación, usa:
echo   python wallpaper_changer.py
echo.
echo O haz doble clic en: run.bat
echo.
pause
