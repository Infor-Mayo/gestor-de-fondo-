@echo off
echo 🖼️ INSTALADOR DE MENU CONTEXTUAL (EXE)
echo =====================================
echo.
echo Este script instalará el menú contextual usando el EXE compilado.
echo Esto permitirá agregar imágenes y videos directamente desde el
echo Explorador de Windows haciendo clic derecho.
echo.

if not exist "dist\CambiadorFondo.exe" (
    echo ❌ Error: No se encontró CambiadorFondo.exe en la carpeta dist
    echo 💡 Primero compila la aplicación ejecutando: python build_exe.py
    pause
    exit /b 1
)

echo 🔧 Instalando menú contextual...
python install_context_menu.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ¡Menú contextual instalado exitosamente!
    echo.
    echo 💡 Ahora puedes:
    echo    1. Hacer clic derecho en cualquier imagen o video
    echo    2. Seleccionar "🖼️ Agregar a Lista de Fondos"
    echo    3. El archivo se agregará automáticamente
    echo.
    echo 🔄 Si no aparece inmediatamente, reinicia el Explorador:
    echo    Ctrl+Shift+Esc → Procesos → Windows Explorer → Reiniciar
) else (
    echo.
    echo ❌ Error instalando el menú contextual
    echo 💡 Intenta ejecutar como administrador
)

echo.
pause
