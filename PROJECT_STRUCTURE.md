# 📂 Estructura del Proyecto

## 🎯 Archivos Principales (Raíz)

```
cambiador-de-fondo/
│
├── 📄 main.py                    # ⭐ Punto de entrada de la aplicación
├── 📄 README.md                  # Documentación principal
├── 📄 requirements.txt           # Dependencias Python
├── 📄 .gitignore                 # Archivos ignorados por Git
│
├── 🔧 compile.bat                # Script para compilar a .exe
├── 🔧 run_modular.bat            # Ejecutar versión de desarrollo
├── 🔧 install.bat                # Instalar dependencias
├── 🔧 build_exe.bat              # Compilar (alias de compile.bat)
│
├── 📂 modules/                   # ⭐ Código modular de la aplicación
├── 📂 assets/                    # ⭐ Iconos y recursos
├── 📂 docs/                      # ⭐ Documentación completa
└── 📂 dev_tools/                 # Herramientas de desarrollo
```

## 📦 Módulos (modules/)

```
modules/
├── __init__.py                   # Inicializador del paquete
├── config_manager.py             # Gestión de configuración
├── wallpaper_engine.py           # Motor de cambio de fondos
├── system_tray.py                # Icono en bandeja del sistema
├── startup_manager.py            # Inicio automático con Windows
└── gui.py                        # Interfaz gráfica (CustomTkinter)
```

## 🎨 Assets (assets/)

```
assets/
├── icon.ico                      # Icono Windows (múltiples tamaños)
├── icon.png                      # Icono PNG alta resolución
├── icon_64.png                   # Para system tray
├── icon_32.png                   # Tamaño mediano
└── icon_16.png                   # Tamaño pequeño
```

## 📚 Documentación (docs/)

```
docs/
├── INDEX.md                      # Índice de toda la documentación
├── DEVELOPER_GUIDE.md            # Guía para desarrolladores
├── API_REFERENCE.md              # Referencia de API
├── ESTRUCTURA.md                 # Arquitectura detallada
├── README_MODULAR.md             # Detalles de modularización
├── RESUMEN_MODULAR.md            # Comparación versiones
├── GUIA_RAPIDA.md                # Guía de usuario
├── CONTADOR_REGRESIVO.md         # Feature del contador
├── CHANGELOG.md                  # Historial de cambios
└── PROJECT_SUMMARY.md            # Resumen ejecutivo
```

## 🔧 Dev Tools (dev_tools/)

Herramientas de desarrollo, scripts de prueba y versiones legacy.
Ver `dev_tools/README.md` para más detalles.

## 🚫 Carpetas Ignoradas (no en Git)

```
build/                            # Archivos temporales de PyInstaller
dist/                             # Ejecutable compilado
__pycache__/                      # Cache de Python
*.pyc                             # Bytecode compilado
```

## 📋 Para Subir a GitHub

### Incluir:
- ✅ `main.py` y carpeta `modules/`
- ✅ `assets/` (iconos)
- ✅ `docs/` (documentación)
- ✅ `README.md`, `requirements.txt`, `.gitignore`
- ✅ Scripts de compilación (`.bat`)
- ✅ `dev_tools/` (opcional, para referencia)

### NO Incluir:
- ❌ `build/` (temporal)
- ❌ `dist/` (ejecutable compilado)
- ❌ `__pycache__/` (cache)
- ❌ Archivos de configuración personal

## 🚀 Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar (desarrollo)
python main.py

# O sin consola
pythonw main.py

# Compilar a .exe
.\compile.bat

# El ejecutable estará en: dist\CambiadorDeFondo\
```

## 📊 Tamaños Aproximados

| Elemento | Tamaño |
|----------|--------|
| Código fuente (modules/) | ~50 KB |
| Assets (iconos) | ~300 KB |
| Documentación (docs/) | ~50 KB |
| Dev tools | ~100 KB |
| **Total repositorio** | **~500 KB** |
| Ejecutable compilado | ~50 MB |

---

**Última actualización**: Octubre 2025 - v2.0
