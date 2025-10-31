# 📚 Referencia de API - Cambiador de Fondo

## ConfigManager

### `__init__(config_file: Optional[Path] = None)`
Inicializa el gestor de configuración.

### `get(key: str, default: Any = None) -> Any`
Obtiene un valor de la configuración.

### `set(key: str, value: Any) -> None`
Establece un valor en la configuración.

### `save_config() -> bool`
Guarda la configuración en JSON.

---

## WallpaperEngine

### `__init__(config_manager: ConfigManager)`
Inicializa el motor con un gestor de configuración.

### `set_wallpaper(image_path: str) -> bool`
Cambia el fondo de pantalla en Windows.

### `change_wallpaper() -> bool`
Cambia el fondo según la configuración actual.

### `get_wallpaper_list() -> List[str]`
Obtiene la lista de fondos (carpeta o manual).

### `get_time_until_next_change() -> Optional[int]`
Retorna segundos hasta el próximo cambio (modo tiempo).

### `set_countdown_callback(callback: Callable) -> None`
Registra callback para el contador: `callback(minutes, seconds)`

### `start_monitoring() -> None`
Inicia el thread de monitoreo.

### `stop_monitoring() -> None`
Detiene el thread de monitoreo.

---

## SystemTrayManager

### `__init__(on_show, on_change_now, on_quit)`
Inicializa con callbacks para eventos.

### `setup() -> None`
Crea e inicia el icono en la bandeja.

### `update_countdown(minutes: int, seconds: int) -> None`
Actualiza el tooltip con el contador.

### `notify(title: str, message: str) -> None`
Muestra una notificación.

### `stop() -> None`
Detiene el icono de la bandeja.

---

## StartupManager

### `is_enabled() -> bool`
Verifica si el inicio automático está habilitado.

### `enable() -> Tuple[bool, str]`
Habilita el inicio automático. Retorna (éxito, mensaje).

### `disable() -> Tuple[bool, str]`
Deshabilita el inicio automático. Retorna (éxito, mensaje).

### `get_status() -> Tuple[bool, str, str]`
Retorna (habilitado, texto_estado, color).

---

## Configuración JSON

```json
{
  "mode": "time",
  "interval_minutes": 30,
  "wallpapers": [],
  "wallpaper_folder": null,
  "use_folder": false,
  "weekday_wallpapers": {"0": null, ..., "6": null},
  "last_change": null,
  "current_index": 0
}
```

Ubicación: `%USERPROFILE%\wallpaper_changer_config.json`
