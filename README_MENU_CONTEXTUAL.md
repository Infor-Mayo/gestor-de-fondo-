# 🖼️ Menú Contextual para Fondos de Pantalla

## ¿Qué es esto?

Esta funcionalidad agrega una opción al menú contextual del Explorador de Windows que te permite agregar imágenes y videos directamente a tu lista de fondos de pantalla con solo hacer **clic derecho**.

## 🚀 Instalación

### Método 1: Script Automático (Recomendado)
```bash
# Ejecutar como administrador (opcional, pero recomendado)
install_menu.bat
```

### Método 2: Manual
```bash
python install_context_menu.py
```

## 🎯 Cómo Usar

1. **Instala el menú contextual** usando uno de los métodos arriba
2. **Navega a cualquier carpeta** con imágenes o videos
3. **Haz clic derecho** en una imagen o video
4. **Selecciona** "🖼️ Agregar a Lista de Fondos"
5. **¡Listo!** El archivo se agregará automáticamente

## 📁 Formatos Soportados

### 🖼️ Imágenes
- `.jpg`, `.jpeg`
- `.png`
- `.bmp`

### 🎬 Videos
- `.mp4`, `.avi`, `.mov`
- `.wmv`, `.mkv`
- `.flv`, `.webm`, `.m4v`

## ✨ Características

- ✅ **Detección automática** de duplicados
- ✅ **Validación de formatos** soportados
- ✅ **Mensajes informativos** de confirmación
- ✅ **Integración perfecta** con Windows Explorer
- ✅ **Fácil instalación y desinstalación**

## 🗑️ Desinstalación

### Método 1: Script Automático
```bash
uninstall_menu.bat
```

### Método 2: Manual
```bash
python install_context_menu.py --uninstall
```

## 🔧 Solución de Problemas

### El menú no aparece
1. **Reinicia el Explorador de Windows**:
   - Ctrl+Shift+Esc → Procesos → Windows Explorer → Reiniciar
2. **Verifica permisos**: Ejecuta como administrador
3. **Reinstala**: Desinstala y vuelve a instalar

### Error al agregar archivo
1. **Verifica que el archivo existe**
2. **Comprueba el formato** (debe ser soportado)
3. **Revisa permisos** de la carpeta de configuración

### Mensajes no aparecen
- Asegúrate de tener Python y tkinter instalados
- Los mensajes aparecerán como ventanas emergentes

## 📝 Notas Técnicas

- **Registro de Windows**: Se modifica `HKEY_CURRENT_USER\SystemFileAssociations`
- **Solo usuario actual**: No afecta otros usuarios del sistema
- **Reversible**: Se puede desinstalar completamente
- **Seguro**: No modifica archivos del sistema

## 🎉 ¡Disfruta!

Ahora puedes agregar fondos de pantalla de forma súper rápida y conveniente directamente desde el Explorador de Windows. ¡No más navegación por menús complicados!
