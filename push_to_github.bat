@echo off
echo ========================================
echo   Subiendo a GitHub
echo   Repositorio: Infor-Mayo/gestor-de-fondo
echo ========================================
echo.

REM Verificar si git está inicializado
if not exist .git (
    echo Inicializando repositorio Git...
    git init
    echo.
)

REM Configurar remote
echo Configurando repositorio remoto...
git remote remove origin 2>nul
git remote add origin https://github.com/Infor-Mayo/gestor-de-fondo.git
echo.

REM Agregar archivos
echo Agregando archivos...
git add .
echo.

REM Commit
echo Creando commit...
git commit -m "v2.0 - Version modular completa con documentacion y licencia CC BY-NC 4.0"
echo.

REM Verificar rama
echo Verificando rama principal...
git branch -M main
echo.

REM Push
echo Subiendo a GitHub...
echo NOTA: Se te pedira tu usuario y token de GitHub
echo.
git push -u origin main --force
echo.

echo ========================================
echo   Subida completada!
echo   Ver en: https://github.com/Infor-Mayo/gestor-de-fondo
echo ========================================
pause
