@echo off
git add .
git commit -m "v2.0-Version-modular-completa"
git branch -M main
git remote remove origin
git remote add origin https://github.com/Infor-Mayo/gestor-de-fondo.git
git push -u origin main
pause
