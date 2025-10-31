"""
Cambiador de Fondo de Pantalla - Aplicación Principal
Versión 2.0 - Modular

Aplicación para cambiar automáticamente el fondo de pantalla de Windows
según intervalos de tiempo o días de la semana.

Autor: Cambiador de Fondo Team
Licencia: MIT
"""

import sys
import customtkinter as ctk

# Importar módulos
from modules.gui import WallpaperChangerGUI


def main():
    """Función principal de la aplicación"""
    try:
        # Crear ventana principal
        root = ctk.CTk()
        
        # Inicializar aplicación
        app = WallpaperChangerGUI(root)
        
        # Iniciar loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"Error fatal en la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
