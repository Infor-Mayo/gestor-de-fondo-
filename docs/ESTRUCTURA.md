# 📐 Estructura Modular del Proyecto

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                  (Punto de Entrada)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                       gui.py                                 │
│              (Interfaz Gráfica Principal)                    │
│  - CustomTkinter UI                                          │
│  - Pestañas y controles                                      │
│  - Eventos de usuario                                        │
└──┬────────┬──────────┬──────────┬─────────────┬─────────────┘
   │        │          │          │             │
   │        │          │          │             │
   ▼        ▼          ▼          ▼             ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────────┐
│Config│ │Engine│ │Tray  │ │Startup   │ │ Windows API  │
│Mgr   │ │      │ │      │ │Manager   │ │ (ctypes)     │
└──────┘ └──────┘ └──────┘ └──────────┘ └──────────────┘
   │        │          │          │
   │        │          │          │
   ▼        ▼          ▼          ▼
┌──────────────────────────────────────┐
│      Sistema de Archivos             │
│  - config.json                       │
│  - Imágenes                          │
│  - Registro de Windows               │
└──────────────────────────────────────┘
```

## Flujo de Datos

### 1. Inicio de la Aplicación

```
main.py
  └─> Crea CTk root
  └─> Inicializa WallpaperChangerGUI
      └─> Crea ConfigManager
      └─> Crea WallpaperEngine
      └─> Crea SystemTrayManager
      └─> Inicia monitoreo automático
      └─> Configura UI
```

### 2. Cambio de Fondo Automático

```
WallpaperEngine (thread)
  └─> Verifica si debe cambiar (cada 60s)
      └─> ConfigManager.get("mode")
      └─> ConfigManager.get("interval_minutes")
      └─> Calcula si es tiempo de cambiar
      └─> Obtiene siguiente wallpaper
          └─> get_wallpaper_list()
              └─> Si use_folder: get_images_from_folder()
              └─> Si no: ConfigManager.get("wallpapers")
      └─> set_wallpaper() via Windows API
      └─> ConfigManager.save_config()
```

### 3. Interacción del Usuario

```
Usuario hace clic en botón
  └─> gui.py captura evento
      └─> Llama método correspondiente
          └─> Actualiza ConfigManager
          └─> Ejecuta acción en WallpaperEngine
          └─> Actualiza UI
          └─> Guarda configuración
```

## Responsabilidades por Módulo

### 📋 config_manager.py
```python
Responsabilidades:
├─ Cargar configuración desde JSON
├─ Guardar configuración a JSON
├─ Proporcionar valores por defecto
├─ Métodos get/set para acceso
└─ Validación de configuración

Dependencias:
├─ json (stdlib)
├─ pathlib (stdlib)
└─ typing (stdlib)

Usado por:
├─ wallpaper_engine.py
└─ gui.py
```

### 🖼️ wallpaper_engine.py
```python
Responsabilidades:
├─ Cambiar fondo de pantalla (Windows API)
├─ Obtener lista de imágenes
├─ Leer imágenes de carpeta
├─ Determinar cuándo cambiar
├─ Monitoreo automático (threading)
└─ Lógica de rotación

Dependencias:
├─ os, ctypes (stdlib)
├─ threading, time (stdlib)
├─ datetime, pathlib (stdlib)
└─ config_manager (local)

Usado por:
└─ gui.py
```

### 🔔 system_tray.py
```python
Responsabilidades:
├─ Crear icono en bandeja
├─ Menú contextual
├─ Notificaciones
└─ Callbacks a GUI

Dependencias:
├─ pystray (external)
├─ PIL (external)
└─ threading (stdlib)

Usado por:
└─ gui.py
```

### 🚀 startup_manager.py
```python
Responsabilidades:
├─ Verificar estado de inicio automático
├─ Habilitar inicio automático
├─ Deshabilitar inicio automático
└─ Gestión del registro de Windows

Dependencias:
├─ winreg (stdlib)
├─ os, sys (stdlib)
└─ typing (stdlib)

Usado por:
└─ gui.py
```

### 🎨 gui.py
```python
Responsabilidades:
├─ Interfaz gráfica completa
├─ Pestañas y controles
├─ Eventos de usuario
├─ Actualización de UI
├─ Coordinación de módulos
└─ Detección de tema

Dependencias:
├─ tkinter, customtkinter (external)
├─ darkdetect (external)
├─ config_manager (local)
├─ wallpaper_engine (local)
├─ system_tray (local)
└─ startup_manager (local)

Usado por:
└─ main.py
```

### 🎯 main.py
```python
Responsabilidades:
├─ Punto de entrada
├─ Inicialización
├─ Manejo de errores globales
└─ Loop principal

Dependencias:
├─ customtkinter (external)
└─ gui (local)

Ejecutado por:
└─ Usuario o sistema
```

## Comunicación entre Módulos

### Patrón de Diseño: Dependency Injection

```python
# ConfigManager es inyectado en WallpaperEngine
config_manager = ConfigManager()
engine = WallpaperEngine(config_manager)

# Callbacks son inyectados en SystemTrayManager
tray = SystemTrayManager(
    on_show=self.show_window,
    on_change_now=self.change_now,
    on_quit=self.quit_app
)
```

### Ventajas:
- ✅ Bajo acoplamiento
- ✅ Alta cohesión
- ✅ Fácil testing
- ✅ Reutilización de código

## Extensibilidad

### Agregar un Nuevo Tipo de Cambio

```python
# 1. Crear nuevo módulo
modules/schedule_manager.py

# 2. Implementar lógica
class ScheduleManager:
    def should_change_at_time(self, hour, minute):
        # Lógica personalizada
        pass

# 3. Integrar en wallpaper_engine.py
def should_change_wallpaper(self):
    if self.config_manager.get("mode") == "schedule":
        return self.schedule_manager.should_change_at_time(...)
```

### Agregar Nueva Fuente de Imágenes

```python
# En wallpaper_engine.py
def get_images_from_url(self, url):
    # Descargar imágenes de internet
    pass

def get_wallpaper_list(self):
    mode = self.config_manager.get("source_mode")
    if mode == "folder":
        return self.get_images_from_folder()
    elif mode == "url":
        return self.get_images_from_url()
    elif mode == "manual":
        return self.config_manager.get("wallpapers")
```

## Testing

### Estructura de Tests (Recomendada)

```
tests/
├── test_config_manager.py
├── test_wallpaper_engine.py
├── test_startup_manager.py
└── test_integration.py
```

### Ejemplo de Test

```python
# tests/test_config_manager.py
import unittest
from modules.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def test_default_config(self):
        config = ConfigManager()
        self.assertEqual(config.get("mode"), "time")
    
    def test_save_and_load(self):
        config = ConfigManager()
        config.set("interval_minutes", 60)
        config.save_config()
        
        config2 = ConfigManager()
        self.assertEqual(config2.get("interval_minutes"), 60)
```

## Métricas de Código

### Complejidad por Módulo

| Módulo | Líneas | Clases | Métodos | Complejidad |
|--------|--------|--------|---------|-------------|
| config_manager.py | ~100 | 1 | 7 | Baja |
| wallpaper_engine.py | ~200 | 1 | 12 | Media |
| system_tray.py | ~80 | 1 | 5 | Baja |
| startup_manager.py | ~120 | 1 | 6 | Baja |
| gui.py | ~600 | 1 | 35 | Alta |
| main.py | ~40 | 0 | 1 | Muy Baja |

### Total: ~1140 líneas vs ~800 líneas (monolítico)

**Nota:** Aunque hay más líneas totales, cada archivo es más pequeño y manejable.

## Conclusión

La estructura modular proporciona:

✅ **Separación de responsabilidades**
✅ **Código más mantenible**
✅ **Fácil extensión**
✅ **Mejor organización**
✅ **Testing simplificado**
✅ **Colaboración eficiente**

Cada módulo puede evolucionar independientemente sin afectar al resto del sistema.
