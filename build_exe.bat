@echo off
echo ========================================
echo   Compilando Cambiador de Fondo a EXE
echo ========================================
echo.

REM Verificar si PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
)

echo.
echo Compilando aplicación (versión modular)...
echo.

REM Compilar con PyInstaller usando el spec file
pyinstaller build_simple.spec --distpath dist --workpath build --clean --noconfirm

echo.
echo ========================================
echo   Compilación completada!
echo   La aplicación está en: dist\CambiadorDeFondo\
echo   Ejecutable: dist\CambiadorDeFondo\CambiadorDeFondo.exe
echo   Tamaño total: ~50 MB
echo ========================================
echo.
echo Presiona cualquier tecla para abrir la carpeta dist...
pause >nul
explorer dist
