# 🖼️ Cambiador de Fondo de Pantalla

<div align="center">

![Icon](assets/icon_64.png)

**Aplicación Windows para cambiar fondos de pantalla automáticamente (imágenes y videos)**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)](docs/CHANGELOG.md)
[![GitHub](https://img.shields.io/badge/GitHub-Infor--Mayo-black.svg)](https://github.com/Infor-Mayo/gestor-de-fondo)

</div>

---

## 📋 Descripción

Aplicación de escritorio para Windows que cambia automáticamente el fondo de pantalla según:
- ⏰ **Intervalos de tiempo** configurables
- 📅 **Días de la semana** específicos

### ✨ Características Principales

- 🎨 **Interfaz Moderna** con CustomTkinter
- 🌓 **Modo Claro/Oscuro** con detección automática
- ⏱️ **Contador Regresivo** en tiempo real
- 📁 **Carpeta Persistente** para fondos
- 🖼️ **Soporte de Imágenes** (JPG, PNG, BMP)
- 🎬 **Soporte de Videos** (MP4, AVI, MOV, WMV, MKV, etc.)
- 🖱️ **Drag & Drop** - Arrastra archivos directamente
- 🔔 **Bandeja del Sistema** con notificaciones
- 🚀 **Inicio Automático** con Windows
- 🔧 **Arquitectura Modular** para fácil extensión

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar (versión modular)
python main.py

# O ejecutar sin consola
pythonw main.py
```

## 📸 Capturas

![Interfaz Principal](docs/screenshots/main.png)
*Interfaz moderna con tema oscuro*

## 📚 Documentación

### Para Usuarios
- 📖 [Guía Rápida](docs/GUIA_RAPIDA.md) - Cómo usar la aplicación
- 🔄 [Contador Regresivo](docs/CONTADOR_REGRESIVO.md) - Nueva funcionalidad

### Para Desarrolladores
- 👨‍💻 [Guía de Desarrolladores](docs/DEVELOPER_GUIDE.md) - Arquitectura y desarrollo
- 📡 [Referencia de API](docs/API_REFERENCE.md) - API interna
- 🏗️ [Estructura del Proyecto](docs/ESTRUCTURA.md) - Organización modular
- 📦 [Versión Modular](docs/README_MODULAR.md) - Detalles de modularización
- 📝 [Resumen Modular](docs/RESUMEN_MODULAR.md) - Comparación y ventajas

## 💻 Requisitos

- **Sistema Operativo**: Windows 10 o superior
- **Python**: 3.8 o superior
- **Dependencias**: Ver `requirements.txt`

## 📥 Instalación

```bash
# Clonar repositorio
git clone https://github.com/usuario/cambiador-de-fondo.git
cd cambiador-de-fondo

# Instalar dependencias
pip install -r requirements.txt

# O usar el instalador
install.bat
```

## 🎮 Uso Básico

### Modo Tiempo
1. Selecciona "⏰ Cambiar cada cierto tiempo"
2. Configura el intervalo en minutos
3. Agrega fondos de pantalla:
   - **Carpeta**: Selecciona una carpeta con imágenes y/o videos
   - **Lista Manual**: Usa el botón "➕ Agregar Imagen/Video"
   - **Drag & Drop**: Arrastra archivos directamente desde el explorador
4. ¡Listo! El contador mostrará el tiempo restante

### Modo Días
1. Selecciona "📅 Cambiar según día de la semana"
2. Asigna una imagen o video para cada día
3. El fondo cambiará automáticamente cada día

### 🖱️ Drag & Drop (Arrastrar y Soltar)
- **Fácil de usar**: Arrastra archivos desde el Explorador de Windows
- **Detección automática**: Reconoce imágenes y videos automáticamente
- **Validación inteligente**: Solo acepta formatos soportados
- **Feedback visual**: Indicadores claros durante el arrastre
- **Sin duplicados**: Evita agregar archivos que ya están en la lista

### 🎬 Formatos de Video Soportados
- **MP4** - Formato más común y recomendado
- **AVI** - Formato clásico de Windows
- **MOV** - Formato de QuickTime
- **WMV** - Formato nativo de Windows Media
- **MKV** - Formato contenedor de alta calidad
- **FLV, WEBM, M4V** - Formatos adicionales

## 📂 Estructura del Proyecto

```
cambiador-de-fondo/
├── modules/          # Módulos principales
├── docs/             # Documentación completa
├── assets/           # Iconos y recursos
├── main.py           # Punto de entrada
└── README.md         # Este archivo
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Ver [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) para más información.

## 📄 Licencia

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

✅ **Puedes:**
- Usar el software libremente
- Modificar el código
- Compartir con otros
- Contribuir mejoras

❌ **NO Puedes:**
- Vender el software
- Usar comercialmente sin permiso
- Distribuir con fines de lucro

Ver archivo [LICENSE](LICENSE) para detalles completos.

## 🙏 Agradecimientos

- CustomTkinter por la UI moderna
- pystray por la integración con system tray
- darkdetect por la detección de tema
- OpenCV por el procesamiento de videos
- Pillow por el manejo de imágenes

---

<div align="center">

**¿Preguntas o sugerencias?**

[Reportar un problema](https://github.com/Infor-Mayo/gestor-de-fondo/issues) · [Solicitar función](https://github.com/Infor-Mayo/gestor-de-fondo/issues)

**Desarrollado por Infor-Mayo** 🚀

</div>
