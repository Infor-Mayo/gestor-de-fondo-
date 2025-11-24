@echo off
echo 🚀 Probando EXE en Segundo Plano
echo ================================
echo.
echo Ejecutando: dist\CambiadorFondoSinConsola.exe
echo.
echo ✅ Características a verificar:
echo    1. NO debe aparecer ventana de consola
echo    2. Debe aparecer icono en la bandeja del sistema (área de notificaciones)
echo    3. Al cerrar la ventana (X), debe minimizar a la bandeja
echo    4. Clic derecho en el icono de la bandeja debe mostrar menú
echo.
start "" "dist\CambiadorFondoSinConsola.exe"
echo.
echo 💡 La aplicación se ejecutó en segundo plano.
echo    Busca el icono en la bandeja del sistema (esquina inferior derecha).
echo.
pause
