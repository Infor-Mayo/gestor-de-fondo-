@echo off
echo 🔍 PROBANDO ICONO EN BANDEJA DEL SISTEMA
echo ========================================
echo.
echo Ejecutando: dist\CambiadorFondoConTray.exe
echo.
echo ✅ Verificar:
echo    1. NO debe aparecer consola
echo    2. Debe aparecer ICONO en la bandeja del sistema (esquina inferior derecha)
echo    3. Al cerrar ventana (X) debe minimizar a la bandeja
echo    4. Clic derecho en icono debe mostrar menu
echo    5. Doble clic en icono debe mostrar/ocultar ventana
echo.
echo 🚀 Iniciando aplicación...
start "" "dist\CambiadorFondoConTray.exe"
echo.
echo 💡 IMPORTANTE: Busca el icono en la bandeja del sistema
echo    (área de notificaciones, esquina inferior derecha)
echo.
echo    Si no aparece inmediatamente, puede estar oculto.
echo    Haz clic en la flecha "^" para mostrar iconos ocultos.
echo.
pause
