# 🎬 Soporte de Videos como Fondos de Pantalla

## 📋 Descripción

La aplicación ahora soporta videos como fondos de pantalla animados, además de las imágenes tradicionales. Esta funcionalidad permite crear fondos dinámicos y atractivos para tu escritorio.

## 🎯 Formatos Soportados

### Videos
- **MP4** - Formato más común y recomendado
- **AVI** - Formato clásico de Windows
- **MOV** - Formato de QuickTime
- **WMV** - Formato nativo de Windows Media
- **MKV** - Formato contenedor de alta calidad
- **FLV** - Formato Flash Video
- **WEBM** - Formato web moderno
- **M4V** - Formato iTunes/Apple

### Imágenes (mantiene compatibilidad)
- **JPG/JPEG** - Formato comprimido
- **PNG** - Formato con transparencia
- **BMP** - Formato bitmap de Windows

## 🚀 Cómo Usar Videos

### Modo Carpeta
1. Selecciona "Usar carpeta en lugar de lista manual"
2. Elige una carpeta que contenga videos e imágenes
3. La aplicación detectará automáticamente ambos tipos de archivos
4. Los videos se reproducirán en bucle como fondo animado

### Modo Lista Manual
1. Haz clic en "➕ Agregar Imagen/Video"
2. Selecciona videos desde el diálogo de archivos
3. Los videos se agregarán a la lista junto con las imágenes
4. Se alternarán según el intervalo configurado

### Modo Días de la Semana
1. Para cada día, puedes asignar una imagen o un video
2. Haz clic en "Seleccionar" junto al día deseado
3. Elige un video desde el diálogo de archivos
4. El video se establecerá como fondo para ese día específico

## ⚙️ Funcionamiento Técnico

### Métodos de Reproducción
La aplicación utiliza múltiples métodos para establecer videos como fondo:

1. **Windows Media Player** - Método principal usando HTML5
2. **VLC Player** - Si está instalado, usa modo wallpaper nativo
3. **Ventana Transparente** - Método alternativo con OpenCV

### Características Técnicas
- **Reproducción en Bucle** - Los videos se repiten automáticamente
- **Sin Audio** - Los videos se reproducen silenciados
- **Optimización de Rendimiento** - Ajuste automático de resolución
- **Detección Automática** - Reconoce formatos de video automáticamente

## 📊 Rendimiento

### Recomendaciones
- **Resolución**: Usa videos de resolución similar a tu pantalla
- **Duración**: Videos de 30 segundos a 5 minutos funcionan mejor
- **Formato**: MP4 con codificación H.264 es el más eficiente
- **Tamaño**: Archivos menores a 100MB para mejor rendimiento

### Consideraciones de Sistema
- **RAM**: Videos consumen más memoria que imágenes
- **CPU**: La reproducción puede usar recursos adicionales
- **Batería**: En laptops, puede reducir la duración de la batería

## 🔧 Solución de Problemas

### Video No Se Reproduce
1. Verifica que el formato sea soportado
2. Asegúrate de que el archivo no esté corrupto
3. Intenta con un video MP4 simple
4. Revisa que tengas las dependencias instaladas

### Rendimiento Lento
1. Reduce la resolución del video
2. Usa formatos más eficientes (MP4)
3. Cierra otras aplicaciones que usen video
4. Considera usar imágenes para mejor rendimiento

### Video Se Detiene
1. Verifica que el archivo siga existiendo
2. Comprueba permisos de lectura del archivo
3. Reinicia la aplicación
4. Revisa los logs de error en la consola

## 🛠️ Dependencias Técnicas

### Nuevas Librerías
```
opencv-python>=4.8.0  # Procesamiento de video
numpy>=1.24.0         # Operaciones matemáticas
```

### Instalación
```bash
pip install opencv-python numpy
```

## 📝 Notas Importantes

### Compatibilidad
- **Windows 10+** requerido para funcionalidad completa
- **DirectX** debe estar actualizado
- **Codecs de video** pueden ser necesarios para algunos formatos

### Limitaciones
- No todos los formatos de video están garantizados
- El rendimiento varía según el hardware
- Algunos antivirus pueden interferir con la reproducción

### Consejos de Uso
- Prueba primero con videos cortos y simples
- Mantén una copia de respaldo de tus videos favoritos
- Usa la función de "Cambiar Fondo Ahora" para probar videos
- Combina videos e imágenes para variedad

## 🔄 Migración desde Versión Anterior

Si actualizas desde una versión que solo soportaba imágenes:

1. **Configuración Existente** - Se mantiene intacta
2. **Carpetas de Imágenes** - Ahora también buscarán videos
3. **Listas Manuales** - Puedes agregar videos a las existentes
4. **Días de la Semana** - Puedes reemplazar imágenes con videos

## 📞 Soporte

Si tienes problemas con videos específicos:
1. Reporta el formato y codec del video
2. Incluye información de tu sistema operativo
3. Describe el comportamiento observado
4. Proporciona logs de error si están disponibles

---

**Desarrollado por Infor-Mayo** 🚀
