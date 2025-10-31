# 🔧 Herramientas de Desarrollo

Esta carpeta contiene archivos de desarrollo, scripts de prueba y versiones legacy que no son necesarios para el uso normal de la aplicación.

## 📁 Contenido

### Scripts de Compilación Alternativos
- `compile_absolute.bat` - Compilación con rutas absolutas (experimental)
- `wallpaper_changer.spec` - Spec de PyInstaller (legacy)
- `CambiadorDeFondo.spec` - Spec generado automáticamente
- `build_simple.spec` - Spec simplificado

### Hooks de PyInstaller
- `hook-pystray.py` - Hook personalizado para pystray
- `hook-pystray-manual.py` - Hook manual para pystray

### Scripts de Prueba
- `check_pystray.py` - Verificar instalación de pystray
- `test_exe.bat` - Probar el ejecutable
- `run.bat` - Ejecutar versión legacy
- `run_exe.bat` - Ejecutar el .exe compilado

### Herramientas de Conversión
- `convert_icon.py` - Convertir icono a múltiples formatos
- `convert_to_ctk.py` - Script de conversión a CustomTkinter

### Versiones Legacy
- `wallpaper_changer.py` - Versión monolítica original (800 líneas)
- `wallpaper_changer_backup.py` - Backup de la versión original

### Recursos
- `icono/` - Icono original en formato WebP

## ⚠️ Nota

Estos archivos NO son necesarios para:
- Ejecutar la aplicación
- Compilar el proyecto (usar `compile.bat` en la raíz)
- Distribuir la aplicación

Se mantienen aquí solo para referencia y desarrollo futuro.
