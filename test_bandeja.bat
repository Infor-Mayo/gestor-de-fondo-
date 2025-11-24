@echo off
echo 🎯 PROBANDO ICONO EN BANDEJA DEL SISTEMA
echo ========================================
echo.
echo Ejecutando: dist\CambiadorFondoConBandeja.exe
echo.
echo ✅ LO QUE DEBE PASAR:
echo    1. NO aparece consola
echo    2. Se abre la ventana de la aplicación
echo    3. Al cerrar (X) la ventana desaparece
echo    4. APARECE ICONO en la bandeja del sistema (área de notificaciones)
echo    5. Doble clic en el icono: muestra la ventana
echo    6. Clic derecho en el icono: menú con opciones
echo.
echo 🚀 Iniciando aplicación...
start "" "dist\CambiadorFondoConBandeja.exe"
echo.
echo 💡 BUSCA EL ICONO AQUÍ:
echo    ┌─────────────────────────────────────┐
echo    │  Área de notificaciones             │
echo    │  (esquina inferior derecha)         │
echo    │                                     │
echo    │  Si no lo ves, haz clic en la       │
echo    │  flecha "^" para mostrar iconos     │
echo    │  ocultos                            │
echo    └─────────────────────────────────────┘
echo.
pause
