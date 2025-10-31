# ⏰ Contador Regresivo - Nueva Funcionalidad

## 📋 Descripción

Se ha agregado un **contador regresivo en tiempo real** que muestra cuánto tiempo falta para el próximo cambio de fondo de pantalla cuando está activo el **modo de intervalo de tiempo**.

## 🎯 Ubicaciones del Contador

### 1. 🖥️ En la Aplicación Principal

El contador aparece en la pestaña **"⚙️ General"**, en la sección de **"Estado Actual"**:

```
Estado Actual
─────────────
Modo actual: Tiempo
Fuente: Carpeta (46 imágenes)
Último cambio: 30/10/2025 22:30:15

⏰ Próximo cambio en: 28m 45s
```

**Características:**
- ✅ Actualización en tiempo real (cada segundo)
- ✅ Formato legible: `Xm Ys` cuando hay minutos, solo `Ys` cuando quedan menos de 60 segundos
- ✅ Color verde para mejor visibilidad
- ✅ Solo visible en modo "Tiempo"

### 2. 🔔 En el Icono de la Bandeja del Sistema

Al pasar el mouse sobre el icono en la bandeja del sistema (system tray), el tooltip muestra:

```
Cambiador de Fondo
⏰ Próximo cambio: 28m 45s
```

**Características:**
- ✅ Actualización automática cada segundo
- ✅ Visible sin abrir la aplicación
- ✅ Información siempre accesible

## 🔧 Funcionamiento Técnico

### Flujo de Datos

```
WallpaperEngine (thread)
    └─> Cada 1 segundo:
        ├─> Calcula tiempo restante
        ├─> Llama al callback con (minutos, segundos)
        └─> GUI actualiza:
            ├─> Label en la interfaz
            └─> Tooltip del system tray
```

### Cálculo del Tiempo Restante

```python
# Fórmula
tiempo_último_cambio + intervalo_configurado - tiempo_actual = tiempo_restante

# Ejemplo
Último cambio: 22:00:00
Intervalo: 30 minutos
Hora actual: 22:28:45
─────────────────────
Próximo cambio: 22:30:00
Tiempo restante: 1m 15s
```

## 📊 Comportamiento según el Modo

| Modo | Contador Visible | Actualización |
|------|------------------|---------------|
| **Tiempo** | ✅ Sí | Cada segundo |
| **Días de la semana** | ❌ No | N/A |

### Modo Tiempo
- El contador se muestra y actualiza constantemente
- Muestra el tiempo exacto hasta el próximo cambio
- Se resetea cuando cambia el fondo

### Modo Días de la Semana
- El contador NO se muestra
- El tooltip del system tray muestra solo el título base
- No hay intervalo de tiempo configurado

## 🎨 Diseño Visual

### En la Aplicación
```
┌─────────────────────────────────────┐
│ Estado Actual                       │
├─────────────────────────────────────┤
│ Modo actual: Tiempo                 │
│ Fuente: Carpeta (46 imágenes)       │
│ Último cambio: 30/10/2025 22:30:15  │
│                                      │
│ ⏰ Próximo cambio en: 28m 45s       │ ← Verde, negrita
└─────────────────────────────────────┘
```

### En el System Tray
```
┌─────────────────────────────┐
│ Cambiador de Fondo          │
│ ⏰ Próximo cambio: 28m 45s  │
└─────────────────────────────┘
```

## 💡 Casos de Uso

### Caso 1: Monitoreo Pasivo
```
Usuario: Trabaja con la aplicación minimizada
Sistema: El tooltip muestra el tiempo restante
Beneficio: Sabe cuándo cambiará sin abrir la app
```

### Caso 2: Planificación
```
Usuario: Quiere saber cuándo cambiará el fondo
Sistema: Abre la app y ve el contador en tiempo real
Beneficio: Puede planificar capturas de pantalla, etc.
```

### Caso 3: Verificación
```
Usuario: Cambió el intervalo a 5 minutos
Sistema: El contador muestra inmediatamente el nuevo tiempo
Beneficio: Confirmación visual del cambio
```

## 🔄 Actualización del Contador

### Frecuencia
- **Antes:** El motor verificaba cada 60 segundos
- **Ahora:** El motor verifica cada 1 segundo
- **Impacto:** Mínimo en rendimiento, contador preciso

### Optimización
```python
# Loop optimizado
while running:
    # Verificar cambio (solo cuando es necesario)
    if should_change_wallpaper():
        change_wallpaper()
    
    # Actualizar contador (cada segundo)
    if countdown_callback and mode == "time":
        update_countdown()
    
    time.sleep(1)  # 1 segundo para precisión
```

## 🎯 Ventajas

### Para el Usuario
- ✅ **Transparencia:** Sabe exactamente cuándo cambiará el fondo
- ✅ **Control:** Puede planificar según el tiempo restante
- ✅ **Feedback:** Confirmación visual de que la app funciona
- ✅ **Accesibilidad:** Información disponible sin abrir la app

### Técnicas
- ✅ **Modular:** Implementado con callbacks
- ✅ **Eficiente:** Actualización cada segundo sin impacto
- ✅ **Thread-safe:** Usa `root.after()` para UI updates
- ✅ **Escalable:** Fácil agregar más displays del contador

## 📝 Código Relevante

### Módulos Modificados

1. **`wallpaper_engine.py`**
   - `get_time_until_next_change()`: Calcula tiempo restante
   - `set_countdown_callback()`: Registra callback
   - `_monitor_loop()`: Actualiza cada segundo

2. **`system_tray.py`**
   - `update_countdown()`: Actualiza tooltip
   - `update_title()`: Cambia el título del icono

3. **`gui.py`**
   - `countdown_label`: Label para mostrar contador
   - `update_countdown()`: Actualiza UI y tray

## 🚀 Uso

### Activar el Contador
```
1. Abre la aplicación
2. Selecciona "Modo Tiempo"
3. Configura un intervalo
4. El contador aparece automáticamente
```

### Ver el Contador
```
Opción 1: En la app (pestaña General)
Opción 2: Tooltip del icono en bandeja
```

### Desactivar
```
Cambia a "Modo Días de la semana"
→ El contador desaparece automáticamente
```

## 🎉 Resultado

El contador regresivo proporciona:
- ✨ Mejor experiencia de usuario
- 📊 Información en tiempo real
- 🎯 Mayor control y transparencia
- 💚 Feedback visual constante

**¡Ahora siempre sabrás cuándo cambiará tu fondo de pantalla!** ⏰✨
