# 🖼️ Guía Rápida - Cambiador de Fondo de Pantalla

## 🚀 Inicio Rápido

### 1️⃣ Instalación (Primera vez)
1. Haz doble clic en `install.bat`
2. Espera a que se instalen las dependencias
3. ¡Listo!

### 2️⃣ Ejecutar la Aplicación
- **Opción 1:** Doble clic en `run.bat`
- **Opción 2:** Abre una terminal y ejecuta `python wallpaper_changer.py`

## 📋 Configuración Básica

### Modo 1: Cambio por Tiempo ⏰

#### Opción A: Usar Carpeta (Más Fácil) 📁
1. Abre la aplicación
2. En "Configuración General" selecciona **"Cambiar cada cierto tiempo"**
3. Ve a la pestaña **"Modo Tiempo"**
4. Configura el intervalo (ej: 30 minutos)
5. Marca la casilla **"Usar carpeta en lugar de lista manual"**
6. Haz clic en **"Seleccionar Carpeta"** y elige tu carpeta de imágenes
7. ¡Listo! La aplicación usará automáticamente todas las imágenes de esa carpeta

#### Opción B: Lista Manual 📋
1. Abre la aplicación
2. En "Configuración General" selecciona **"Cambiar cada cierto tiempo"**
3. Ve a la pestaña **"Modo Tiempo"**
4. Configura el intervalo (ej: 30 minutos)
5. Haz clic en **"Agregar Imagen"** y selecciona tus fondos uno por uno
6. ¡Listo! Los fondos cambiarán automáticamente

### Modo 2: Cambio por Día de la Semana 📅
1. Abre la aplicación
2. En "Configuración General" selecciona **"Cambiar según día de la semana"**
3. Ve a la pestaña **"Modo Días de la Semana"**
4. Para cada día, haz clic en **"Seleccionar"** y elige una imagen
5. Haz clic en **"Guardar Configuración de Días"**
6. ¡Listo! Cada día tendrá su propio fondo

## 🔄 Inicio Automático con Windows

1. Ve a la pestaña **"Inicio Automático"**
2. Haz clic en **"Habilitar Inicio Automático"**
3. Ahora la aplicación se iniciará cuando enciendas tu PC

## 🎯 Funciones Útiles

- **Cambiar Fondo Ahora:** Botón en la pestaña "Configuración General" para cambiar inmediatamente
- **Usar Carpeta:** Marca la casilla para usar automáticamente todas las imágenes de una carpeta
- **Refrescar Lista:** Actualiza la lista de imágenes mostradas (útil si agregaste imágenes a la carpeta)
- **Eliminar Imagen:** Selecciona una imagen en la lista y haz clic en "Eliminar Seleccionada"
- **Ver Estado:** La pestaña "Configuración General" muestra el modo actual y último cambio

## 💻 Crear Ejecutable (Opcional)

Si quieres un archivo .exe que no necesite Python:
1. Haz doble clic en `build_exe.bat`
2. Espera a que termine la compilación
3. El archivo estará en la carpeta `dist/WallpaperChanger.exe`
4. Puedes copiar ese .exe a cualquier PC con Windows

## ❓ Preguntas Frecuentes

**P: ¿Dónde se guardan mis configuraciones?**
R: En `C:\Users\TU_USUARIO\wallpaper_changer_config.json`

**P: ¿Qué formatos de imagen acepta?**
R: JPG, JPEG, PNG y BMP

**P: ¿Puedo usar imágenes de diferentes carpetas?**
R: Sí, en modo lista manual puedes seleccionar imágenes de cualquier ubicación. O usa el modo carpeta para usar todas las imágenes de una carpeta específica

**P: ¿Se actualizan automáticamente las imágenes si agrego más a la carpeta?**
R: Sí, si usas el modo carpeta, la aplicación detectará automáticamente las nuevas imágenes. Puedes hacer clic en "Refrescar Lista" para verlas en la interfaz

**P: ¿Cómo detengo el cambio automático?**
R: Cierra la aplicación o cambia a otro modo

**P: ¿Funciona en Windows 11?**
R: Sí, funciona en Windows 10 y 11

## 🛠️ Solución de Problemas

### El fondo no cambia
- Verifica que las rutas de las imágenes sean correctas
- Asegúrate de haber guardado la configuración
- Comprueba que el modo seleccionado tenga imágenes asignadas

### Error al instalar
- Asegúrate de tener Python 3.8 o superior instalado
- Ejecuta `install.bat` como administrador

### La aplicación no se inicia con Windows
- Ejecuta la aplicación como administrador
- Vuelve a habilitar el inicio automático

## 📞 Soporte

Si tienes problemas, revisa el archivo `README.md` para más detalles técnicos.

---

**¡Disfruta de tus fondos de pantalla dinámicos! 🎨**
