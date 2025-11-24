# 🚀 Sistema Dinámico de Menú Contextual

## ✨ ¿Qué es esto?

Un sistema **completamente dinámico** que funciona tanto en **scripts Python** como en **aplicaciones EXE compiladas**, permitiendo agregar imágenes y videos a la lista de fondos directamente desde el Explorador de Windows.

## 🎯 Características Dinámicas

### 🔧 **Detección Automática**
- ✅ **Script Python**: Detecta automáticamente la instalación de Python
- ✅ **Aplicación EXE**: Se adapta automáticamente al ejecutable compilado
- ✅ **Rutas Dinámicas**: No depende de rutas fijas o hardcodeadas

### 🖥️ **Compatibilidad Universal**
- ✅ **Windows 10/11**: Funciona en cualquier versión moderna
- ✅ **PCs Nuevas**: No requiere configuración previa
- ✅ **Diferentes Usuarios**: Se instala por usuario, no globalmente
- ✅ **Portabilidad**: El EXE funciona sin instalación de Python

## 🚀 Instalación

### Método 1: Desde la Aplicación (Recomendado)
1. **Abre la aplicación** (Python o EXE)
2. **Ve a "Modo Tiempo"**
3. **Clic en "⚙️ Instalar Menú Contextual"**
4. **Confirma la instalación**
5. **¡Listo!**

### Método 2: Script Manual
```bash
python install_context_menu.py
```

### Método 3: Batch Automático
```bash
install_menu.bat
```

## 🎬 Cómo Funciona

### 🔍 **Detección Inteligente**
```python
# Detecta si es EXE o script
if getattr(sys, 'frozen', False):
    # Modo EXE: usa el ejecutable directamente
    command = f'"{sys.executable}" --add-wallpaper "%1"'
else:
    # Modo Python: busca Python en el sistema
    python_exe = find_python_executable()
    command = f'"{python_exe}" "{main_script}" --add-wallpaper "%1"'
```

### 🎯 **Ejecución Dinámica**
1. **Clic derecho** en imagen/video
2. **Seleccionar** "🖼️ Agregar a Lista de Fondos"
3. **Sistema detecta** automáticamente el modo (EXE/Python)
4. **Ejecuta** el comando correcto
5. **Muestra** mensaje de confirmación

## 📦 Compilación a EXE

### Compilar Aplicación
```bash
python build_exe.py
```

### Lo que Incluye
- ✅ **Aplicación completa** en un solo EXE
- ✅ **Menú contextual dinámico** integrado
- ✅ **Todas las dependencias** incluidas
- ✅ **Configuración automática** del registro

## 🔧 Arquitectura Técnica

### 📁 **Estructura de Archivos**
```
cambiador-de-fondo/
├── main.py                     # Aplicación principal con soporte CLI
├── install_context_menu.py     # Instalador dinámico
├── build_exe.py               # Compilador a EXE
├── modules/
│   ├── gui.py                 # GUI con botón de instalación
│   ├── config_manager.py      # Gestión de configuración
│   └── video_wallpaper.py     # Soporte de video
└── dist/
    └── CambiadorFondo.exe     # EXE compilado
```

### 🔄 **Flujo de Ejecución**
```
Explorador → Clic Derecho → Registro Windows → 
Comando Dinámico → main.py --add-wallpaper → 
Agregar a Lista → Mensaje Confirmación
```

## 🛡️ Seguridad y Compatibilidad

### ✅ **Seguro**
- **Solo usuario actual**: No modifica sistema global
- **Reversible**: Desinstalación completa disponible
- **Sin privilegios**: No requiere permisos de administrador

### ✅ **Compatible**
- **Python 3.7+**: Cualquier versión moderna
- **Windows 10/11**: Todas las ediciones
- **Arquitecturas**: x64 y x86
- **Antivirus**: No genera falsos positivos

## 🎉 Ventajas del Sistema Dinámico

### 🚀 **Para Desarrolladores**
- **Sin hardcoding**: Rutas completamente dinámicas
- **Fácil distribución**: Un solo EXE funciona en cualquier PC
- **Mantenimiento**: Actualizaciones automáticas del registro

### 👥 **Para Usuarios**
- **Instalación simple**: Un clic desde la aplicación
- **Funciona siempre**: No importa cómo se ejecute
- **Sin configuración**: Todo automático

## 🔧 Solución de Problemas

### El menú no aparece
```bash
# Reiniciar Explorador de Windows
Ctrl+Shift+Esc → Procesos → Windows Explorer → Reiniciar
```

### Error de permisos
```bash
# Ejecutar como administrador (opcional)
# El sistema funciona sin privilegios especiales
```

### EXE no funciona
```bash
# Verificar que todas las dependencias estén incluidas
python build_exe.py
```

## 🎯 Casos de Uso

### 📱 **Desarrollo**
- Ejecutar como script Python durante desarrollo
- Menú contextual se adapta automáticamente

### 📦 **Distribución**
- Compilar a EXE para distribución
- Menú contextual funciona sin Python instalado

### 🏢 **Empresarial**
- Desplegar en múltiples PCs
- Instalación automática del menú contextual

## 🎉 ¡Resultado Final!

**Un sistema completamente dinámico que:**
- ✅ **Funciona en cualquier PC** sin configuración
- ✅ **Se adapta automáticamente** a Python o EXE
- ✅ **Instala fácilmente** desde la propia aplicación
- ✅ **Es completamente portable** y profesional

**¡La solución perfecta para un menú contextual que realmente funciona en cualquier situación!** 🚀
