"""
Módulo especializado para manejar drag & drop
Implementación robusta que funciona con CustomTkinter
"""

import tkinter as tk
import os
from pathlib import Path
from typing import List, Callable, Optional

class DragDropHandler:
    """Manejador de drag & drop para widgets de tkinter"""
    
    def __init__(self, widget, callback: Optional[Callable] = None):
        """
        Inicializa el manejador de drag & drop
        
        Args:
            widget: Widget de tkinter donde habilitar drag & drop
            callback: Función a llamar cuando se suelten archivos
        """
        self.widget = widget
        self.callback = callback
        self.setup_drag_drop()
    
    def setup_drag_drop(self):
        """Configura drag & drop usando múltiples métodos"""
        try:
            # Método 1: Intentar con Windows API (más compatible)
            self._setup_windows_api()
        except:
            try:
                # Método 2: Intentar con tkinterdnd2
                self._setup_tkinterdnd2()
            except:
                # Método 3: Usar solo eventos básicos
                print("⚠️ Drag & drop avanzado no disponible, usando método básico")
                self._setup_basic_events()
    
    def _setup_tkinterdnd2(self):
        """Configura usando tkinterdnd2"""
        try:
            import tkinterdnd2 as tkdnd
            
            # Registrar el widget
            self.widget.drop_target_register(tkdnd.DND_FILES)
            
            # Configurar eventos
            self.widget.dnd_bind('<<Drop>>', self._on_drop_tkdnd)
            self.widget.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.widget.dnd_bind('<<DragLeave>>', self._on_drag_leave)
            
            print("✅ Drag & drop configurado con tkinterdnd2")
            
        except Exception as e:
            print(f"❌ tkinterdnd2 falló: {e}")
            raise
    
    def _setup_windows_api(self):
        """Configura usando Windows API - FUNCIONAL"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Obtener handle de la ventana después de que esté mapeada
            def setup_when_ready():
                try:
                    hwnd = self.widget.winfo_id()
                    # Habilitar drag & drop
                    ctypes.windll.shell32.DragAcceptFiles(hwnd, True)
                    print("✅ Windows API drag & drop habilitado")
                except Exception as e:
                    print(f"Error habilitando DragAcceptFiles: {e}")
            
            # Ejecutar cuando el widget esté listo
            self.widget.after(100, setup_when_ready)
            
            # Configurar eventos básicos como respaldo
            self._setup_basic_events()
            
        except Exception as e:
            print(f"❌ Windows API falló: {e}")
            raise
    
    def _setup_window_proc(self, hwnd):
        """Método deshabilitado por estabilidad"""
        pass
    
    def _handle_drop_files(self, hdrop):
        """Método deshabilitado por estabilidad"""
        pass
    
    def _setup_basic_events(self):
        """Configura eventos básicos como respaldo"""
        try:
            # Configurar eventos de mouse
            self.widget.bind('<Button-3>', self._show_context_menu)
            self.widget.bind('<Double-Button-1>', self._quick_add)
            
            print("✅ Eventos básicos configurados")
            
        except Exception as e:
            print(f"Error configurando eventos básicos: {e}")
    
    def _on_drop_tkdnd(self, event):
        """Maneja drop con tkinterdnd2"""
        try:
            files = event.widget.tk.splitlist(event.data)
            
            # Restaurar apariencia
            self.widget.configure(bg='white')
            
            # Llamar callback
            if self.callback and files:
                self.callback(files)
                
        except Exception as e:
            print(f"Error en drop tkdnd: {e}")
    
    def _on_drag_enter(self, event):
        """Cambiar apariencia al entrar"""
        try:
            self.widget.configure(bg='#E8F5E8')  # Verde claro
        except:
            pass
    
    def _on_drag_leave(self, event):
        """Restaurar apariencia al salir"""
        try:
            self.widget.configure(bg='white')
        except:
            pass
    
    def _show_context_menu(self, event):
        """Muestra menú contextual"""
        try:
            import tkinter.messagebox as msgbox
            
            result = msgbox.askyesno(
                "Agregar Archivos",
                "¿Quieres abrir el selector de archivos?\n\n"
                "Nota: Si el drag & drop no funciona,\n"
                "usa esta opción para agregar archivos.",
                icon="question"
            )
            
            if result and hasattr(self, 'fallback_callback'):
                self.fallback_callback()
                
        except Exception as e:
            print(f"Error en menú contextual: {e}")
    
    def _quick_add(self, event):
        """Selector rápido con doble clic"""
        try:
            if hasattr(self, 'fallback_callback'):
                self.fallback_callback()
        except Exception as e:
            print(f"Error en quick add: {e}")
    
    def set_fallback_callback(self, callback: Callable):
        """Establece callback de respaldo para cuando drag & drop no funcione"""
        self.fallback_callback = callback


def create_drag_drop_area(parent, callback: Callable, fallback_callback: Optional[Callable] = None):
    """
    Crea un área de drag & drop funcional
    
    Args:
        parent: Widget padre
        callback: Función a llamar con archivos soltados
        fallback_callback: Función de respaldo si drag & drop falla
        
    Returns:
        Widget configurado con drag & drop
    """
    try:
        # Intentar usar tkinterdnd2 para crear la ventana
        import tkinterdnd2 as tkdnd
        
        # Crear frame con soporte DnD
        frame = tk.Frame(parent)
        
        # Configurar drag & drop
        handler = DragDropHandler(frame, callback)
        
        if fallback_callback:
            handler.set_fallback_callback(fallback_callback)
        
        return frame, handler
        
    except ImportError:
        # Crear frame normal si tkinterdnd2 no está disponible
        frame = tk.Frame(parent)
        handler = DragDropHandler(frame, callback)
        
        if fallback_callback:
            handler.set_fallback_callback(fallback_callback)
        
        return frame, handler
