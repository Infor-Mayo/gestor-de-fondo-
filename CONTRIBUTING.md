# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Cambiador de Fondo de Pantalla!

## 📋 Código de Conducta

- Sé respetuoso con otros contribuidores
- Proporciona retroalimentación constructiva
- Acepta críticas constructivas con gracia

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio

```bash
# Haz fork en GitHub y clona tu fork
git clone https://github.com/TU-USUARIO/gestor-de-fondo.git
cd gestor-de-fondo
```

### 2. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 3. Hacer Cambios

- Sigue el estilo de código existente
- Agrega docstrings a funciones nuevas
- Usa type hints cuando sea posible
- Mantén los módulos pequeños y enfocados

### 4. Probar

```bash
# Ejecutar la aplicación
python main.py

# Verificar que todo funciona
```

### 5. Commit

```bash
git add .
git commit -m "feat: descripción clara del cambio"
```

**Formato de commits:**
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, sin cambios de código
- `refactor:` Refactorización de código
- `test:` Agregar tests
- `chore:` Mantenimiento

### 6. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego crea un Pull Request en GitHub.

## 📝 Guías de Estilo

### Python

- Sigue PEP 8
- Usa 4 espacios para indentación
- Máximo 100 caracteres por línea
- Docstrings en español
- Type hints en funciones públicas

```python
def ejemplo_funcion(parametro: str) -> bool:
    """
    Descripción breve de la función
    
    Args:
        parametro: Descripción del parámetro
        
    Returns:
        Descripción del valor de retorno
    """
    return True
```

### Commits

- Usa español para los mensajes
- Primera línea: resumen (máx 50 caracteres)
- Línea en blanco
- Descripción detallada si es necesario

## 🐛 Reportar Bugs

Usa las [GitHub Issues](https://github.com/Infor-Mayo/gestor-de-fondo/issues) e incluye:

- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Capturas de pantalla si aplica
- Versión de Python y Windows

## 💡 Sugerir Funcionalidades

Abre un Issue con:

- Descripción clara de la funcionalidad
- Casos de uso
- Mockups o ejemplos si es posible

## 📚 Mejorar Documentación

La documentación siempre puede mejorar:

- Corregir errores tipográficos
- Aclarar explicaciones confusas
- Agregar ejemplos
- Traducir a otros idiomas

## ⚖️ Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la misma licencia CC BY-NC 4.0 del proyecto.

## ❓ Preguntas

Si tienes preguntas, abre un Issue o contacta a los mantenedores.

---

**¡Gracias por contribuir!** 🎉
