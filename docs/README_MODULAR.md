# Cambiador de Fondo de Pantalla - Versión Modular 2.0

Aplicación de escritorio para Windows que cambia automáticamente el fondo de pantalla según el tiempo transcurrido o el día de la semana.

## 🏗️ Estructura Modular

La aplicación está organizada en módulos independientes para facilitar el mantenimiento y extensión:

```
cambiador de fondo/
│
├── main.py                          # Archivo principal de ejecución
├── wallpaper_changer.py            # Versión monolítica (legacy)
│
├── modules/                         # Módulos de la aplicación
│   ├── __init__.py                 # Inicializador del paquete
│   ├── config_manager.py           # Gestión de configuración
│   ├── wallpaper_engine.py         # Motor de cambio de fondos
│   ├── system_tray.py              # Gestión de bandeja del sistema
│   ├── startup_manager.py          # Gestión de inicio automático
│   └── gui.py                      # Interfaz gráfica
│
├── requirements.txt                 # Dependencias
├── install.bat                      # Instalador
├── run.bat                          # Ejecutor rápido
└── build_exe.bat                    # Compilador a .exe
```

## 📦 Módulos

### 1. `config_manager.py`
**Responsabilidad:** Gestión de configuración
- Carga y guarda configuración en JSON
- Proporciona valores por defecto
- Métodos get/set para acceso a configuración

### 2. `wallpaper_engine.py`
**Responsabilidad:** Motor de cambio de fondos
- Cambia el fondo de pantalla en Windows
- Gestiona lista de fondos y carpetas
- Monitoreo automático con threading
- Lógica de cambio por tiempo o día

### 3. `system_tray.py`
**Responsabilidad:** Icono en bandeja del sistema
- Crea y gestiona icono en system tray
- Menú contextual con opciones
- Notificaciones al usuario

### 4. `startup_manager.py`
**Responsabilidad:** Inicio automático con Windows
- Habilita/deshabilita inicio automático
- Gestión del registro de Windows
- Verificación de estado

### 5. `gui.py`
**Responsabilidad:** Interfaz gráfica
- Interfaz con CustomTkinter
- Pestañas organizadas
- Selector de tema (claro/oscuro)
- Eventos y callbacks

### 6. `main.py`
**Responsabilidad:** Punto de entrada
- Inicializa la aplicación
- Manejo de errores globales
- Configuración inicial

## 🚀 Ejecución

### Versión Modular (Recomendada)
```bash
python main.py
```

### Versión Monolítica (Legacy)
```bash
python wallpaper_changer.py
```

## 📥 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# O usar el instalador
install.bat
```

## 🔧 Ventajas de la Estructura Modular

### ✅ Mantenibilidad
- Cada módulo tiene una responsabilidad clara
- Fácil localizar y corregir bugs
- Código más legible y organizado

### ✅ Escalabilidad
- Agregar nuevas funcionalidades sin afectar otros módulos
- Fácil extensión de características
- Módulos reutilizables

### ✅ Testabilidad
- Cada módulo puede probarse independientemente
- Facilita pruebas unitarias
- Mejor cobertura de código

### ✅ Colaboración
- Múltiples desarrolladores pueden trabajar en paralelo
- Menos conflictos en control de versiones
- Revisiones de código más sencillas

## 🎯 Uso de Módulos

### Ejemplo: Usar solo el motor de fondos

```python
from modules.config_manager import ConfigManager
from modules.wallpaper_engine import WallpaperEngine

# Crear gestor de configuración
config = ConfigManager()

# Crear motor de fondos
engine = WallpaperEngine(config)

# Cambiar fondo manualmente
engine.change_wallpaper()

# Iniciar monitoreo automático
engine.start_monitoring()
```

### Ejemplo: Gestionar inicio automático

```python
from modules.startup_manager import StartupManager

# Verificar estado
is_enabled = StartupManager.is_enabled()

# Habilitar
success, message = StartupManager.enable()

# Deshabilitar
success, message = StartupManager.disable()
```

## 🔄 Migración desde Versión Monolítica

La versión monolítica (`wallpaper_changer.py`) sigue disponible para compatibilidad. Para migrar a la versión modular:

1. Usa `main.py` en lugar de `wallpaper_changer.py`
2. La configuración se mantiene compatible
3. Todas las funcionalidades están disponibles

## 🛠️ Desarrollo

### Agregar un Nuevo Módulo

1. Crear archivo en `modules/`
2. Definir clase con responsabilidad clara
3. Importar en `gui.py` o `main.py` según necesidad
4. Documentar en este README

### Modificar un Módulo Existente

1. Identificar el módulo responsable
2. Modificar solo ese módulo
3. Verificar que las interfaces no cambien
4. Probar independientemente

## 📚 Documentación de Módulos

Cada módulo incluye:
- Docstrings en clases y métodos
- Type hints para mejor IDE support
- Comentarios explicativos
- Manejo de errores

## 🐛 Debugging

Para debug de módulos específicos:

```python
# Activar logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Importar módulo
from modules.wallpaper_engine import WallpaperEngine

# Usar normalmente
```

## 📝 Notas de Versión

### v2.0.0 - Versión Modular
- ✨ Estructura modular completa
- 🎨 Interfaz con CustomTkinter
- 🌓 Modo claro/oscuro
- 📁 Carpeta persistente
- 🔔 Bandeja del sistema
- 🚀 Inicio automático

### v1.0.0 - Versión Inicial
- Funcionalidad básica monolítica

## 🤝 Contribuir

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Modifica el módulo correspondiente
4. Agrega tests si es posible
5. Crea un Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles
