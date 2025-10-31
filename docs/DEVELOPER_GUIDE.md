# 👨‍💻 Guía Completa para Desarrolladores

## 📋 Índice

1. [Introducción](#introducción)
2. [Arquitectura](#arquitectura)
3. [Módulos](#módulos)
4. [API Interna](#api-interna)
5. [Threading](#threading)
6. [Windows Integration](#windows-integration)
7. [Testing](#testing)
8. [Extensiones](#extensiones)

---

## 🎯 Introducción

### Propósito
Aplicación Windows para cambiar fondos de pantalla automáticamente por tiempo o día de la semana.

### Stack Tecnológico
- **Python 3.8+**
- **CustomTkinter 5.2+** - UI moderna
- **pystray 0.19+** - System tray
- **darkdetect 0.8+** - Detección de tema
- **Pillow 10.0+** - Imágenes
- **ctypes** - Windows API

### Principios
1. **Modularidad** - Un módulo, una responsabilidad
2. **Dependency Injection** - Componentes desacoplados
3. **Thread Safety** - Manejo seguro de concurrencia
4. **Persistencia** - Estado en JSON

---

## 🏗️ Arquitectura

```
main.py → WallpaperChangerGUI → ConfigManager
                               → WallpaperEngine
                               → SystemTrayManager
                               → StartupManager
```

### Capas
1. **Presentación** - `gui.py` (CustomTkinter)
2. **Lógica** - `wallpaper_engine.py`, `startup_manager.py`
3. **Datos** - `config_manager.py` (JSON)
4. **Sistema** - `system_tray.py`, Windows API

---

## 🔧 Módulos

### config_manager.py
Gestiona configuración en JSON.

```python
config = ConfigManager()
config.get("mode")  # "time" o "weekday"
config.set("interval_minutes", 60)
config.save_config()
```

### wallpaper_engine.py
Motor de cambio de fondos.

```python
engine = WallpaperEngine(config_manager)
engine.change_wallpaper()
engine.start_monitoring()
```

### system_tray.py
Icono en bandeja del sistema.

```python
tray = SystemTrayManager(on_show, on_change, on_quit)
tray.setup()
tray.update_countdown(28, 45)
```

### startup_manager.py
Inicio automático con Windows.

```python
StartupManager.enable()
StartupManager.is_enabled()
```

### gui.py
Interfaz gráfica completa con CustomTkinter.

---

## 📡 API Interna

Ver documentación completa en `API_REFERENCE.md`

---

## 🧵 Threading

### Threads Activos
- **Main Thread**: GUI (CustomTkinter)
- **Monitor Thread**: Verificación cada 1s
- **Tray Thread**: System tray (pystray)

### Thread Safety
```python
# ✅ Correcto - Actualizar UI desde thread
self.root.after(0, lambda: self.label.configure(text="..."))
```

---

## 🪟 Windows Integration

### Cambio de Fondo
```python
ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
```

### Registro (Startup)
```python
winreg.SetValueEx(key, "WallpaperChanger", 0, winreg.REG_SZ, path)
```

---

## 🧪 Testing

```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py
```

---

## 🚀 Extensiones

### Agregar Nuevo Modo
1. Crear método en `wallpaper_engine.py`
2. Actualizar `should_change_wallpaper()`
3. Agregar UI en `gui.py`

### Agregar Nueva Fuente
1. Implementar `get_images_from_X()` en engine
2. Actualizar `get_wallpaper_list()`
3. Agregar configuración en UI

---

Para más detalles, ver documentación completa en `/docs`
