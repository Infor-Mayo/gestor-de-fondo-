"""
Módulo de interfaz gráfica
Maneja toda la interfaz de usuario con CustomTkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Optional

try:
    import darkdetect
    DARKDETECT_AVAILABLE = True
except ImportError:
    DARKDETECT_AVAILABLE = False

from .config_manager import ConfigManager
from .wallpaper_engine import WallpaperEngine
from .system_tray import SystemTrayManager
from .startup_manager import StartupManager


class WallpaperChangerGUI:
    """Interfaz gráfica principal de la aplicación"""
    
    def __init__(self, root: ctk.CTk):
        """
        Inicializa la interfaz gráfica
        
        Args:
            root: Ventana raíz de CustomTkinter
        """
        self.root = root
        self.root.title("Cambiador de Fondo de Pantalla")
        self.root.geometry("850x700")
        
        # Configurar icono de la ventana
        self.setup_window_icon()
        
        # Detectar y configurar tema
        self.setup_theme()
        
        # Inicializar componentes
        self.config_manager = ConfigManager()
        self.wallpaper_engine = WallpaperEngine(self.config_manager)
        self.tray_manager = None
        
        # Configurar UI
        self.setup_ui()
        self.load_current_config()
        
        # Configurar callback del contador
        self.wallpaper_engine.set_countdown_callback(self.update_countdown)
        
        # Iniciar servicios
        self.wallpaper_engine.start_monitoring()
        self.setup_system_tray()
        
        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_window_icon(self) -> None:
        """Configura el icono de la ventana"""
        try:
            import os
            import sys
            
            # Determinar la ruta base (diferente en .exe vs script)
            if getattr(sys, 'frozen', False):
                # Ejecutando como .exe
                base_path = sys._MEIPASS
            else:
                # Ejecutando como script
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Intentar cargar el icono
            icon_path = os.path.join(base_path, 'assets', 'icon.ico')
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                # Intentar con PNG si ICO no existe
                icon_png = os.path.join(base_path, 'assets', 'icon.png')
                if os.path.exists(icon_png):
                    from PIL import Image, ImageTk
                    icon_image = Image.open(icon_png)
                    photo = ImageTk.PhotoImage(icon_image)
                    self.root.iconphoto(True, photo)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
    
    def setup_theme(self) -> None:
        """Detecta y configura el tema inicial"""
        if DARKDETECT_AVAILABLE:
            try:
                system_theme = darkdetect.theme()
                if system_theme == "Dark":
                    ctk.set_appearance_mode("dark")
                    self.current_theme = "Dark"
                else:
                    ctk.set_appearance_mode("light")
                    self.current_theme = "Light"
            except:
                ctk.set_appearance_mode("system")
                self.current_theme = "System"
        else:
            ctk.set_appearance_mode("system")
            self.current_theme = "System"
        
        ctk.set_default_color_theme("blue")
    
    def change_theme(self, choice: str) -> None:
        """
        Cambia el tema de la aplicación
        
        Args:
            choice: Tema seleccionado (System/Light/Dark)
        """
        if choice == "System":
            ctk.set_appearance_mode("system")
        elif choice == "Light":
            ctk.set_appearance_mode("light")
        elif choice == "Dark":
            ctk.set_appearance_mode("dark")
        self.current_theme = choice
    
    def setup_ui(self) -> None:
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header
        self.setup_header(main_frame)
        
        # Tabview
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill='both', expand=True)
        
        # Crear pestañas
        self.tabview.add("⚙️ General")
        self.tabview.add("⏰ Modo Tiempo")
        self.tabview.add("📅 Modo Días")
        self.tabview.add("🚀 Inicio Automático")
        
        # Configurar cada pestaña
        self.setup_general_tab(self.tabview.tab("⚙️ General"))
        self.setup_time_tab(self.tabview.tab("⏰ Modo Tiempo"))
        self.setup_weekday_tab(self.tabview.tab("📅 Modo Días"))
        self.setup_startup_tab(self.tabview.tab("🚀 Inicio Automático"))
    
    def setup_header(self, parent) -> None:
        """Configura el header con título y selector de tema"""
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill='x', pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🖼️ Cambiador de Fondo de Pantalla",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side='left', padx=15, pady=10)
        
        # Selector de tema
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.pack(side='right', padx=15)
        
        ctk.CTkLabel(
            theme_frame,
            text="Tema:",
            font=ctk.CTkFont(size=12)
        ).pack(side='left', padx=5)
        
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["System", "Light", "Dark"],
            command=self.change_theme,
            width=120
        )
        theme_menu.set(self.current_theme)
        theme_menu.pack(side='left', padx=5)
    
    def setup_general_tab(self, parent) -> None:
        """Configura la pestaña general"""
        # Modo de operación
        mode_frame = ctk.CTkFrame(parent)
        mode_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            mode_frame,
            text="Modo de Operación",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15,10))
        
        self.mode_var = tk.StringVar(value=self.config_manager.get("mode"))
        
        ctk.CTkRadioButton(
            mode_frame,
            text="⏰ Cambiar cada cierto tiempo",
            variable=self.mode_var,
            value="time",
            command=self.on_mode_change
        ).pack(anchor='w', padx=15, pady=5)
        
        ctk.CTkRadioButton(
            mode_frame,
            text="📅 Cambiar según día de la semana",
            variable=self.mode_var,
            value="weekday",
            command=self.on_mode_change
        ).pack(anchor='w', padx=15, pady=(5,15))
        
        # Botón de cambio manual
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            btn_frame,
            text="Acción Manual",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15,10))
        
        self.change_now_button = ctk.CTkButton(
            btn_frame,
            text="🔄 Cambiar Fondo Ahora",
            command=self.change_now,
            height=40
        )
        self.change_now_button.pack(padx=15, pady=(0,15))
        
        # Estado
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="Estado Actual",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15,10))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="",
            justify='left'
        )
        self.status_label.pack(anchor='w', padx=15, pady=(0,5))
        
        # Contador regresivo
        self.countdown_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4CAF50"
        )
        self.countdown_label.pack(anchor='w', padx=15, pady=(0,15))
        
        self.update_status()
    
    def setup_time_tab(self, parent) -> None:
        """Configura la pestaña de modo tiempo"""
        # Intervalo
        interval_frame = ctk.CTkFrame(parent)
        interval_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            interval_frame,
            text="Intervalo de Cambio",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15,10))
        
        interval_inner = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_inner.pack(fill='x', padx=15, pady=(0,10))
        
        ctk.CTkLabel(
            interval_inner,
            text="Cambiar cada:"
        ).pack(side='left', padx=(0,10))
        
        self.interval_var = tk.IntVar(value=self.config_manager.get("interval_minutes"))
        interval_entry = ctk.CTkEntry(
            interval_inner,
            textvariable=self.interval_var,
            width=100
        )
        interval_entry.pack(side='left', padx=(0,10))
        
        ctk.CTkLabel(interval_inner, text="minutos").pack(side='left')
        
        ctk.CTkButton(
            interval_frame,
            text="💾 Guardar Intervalo",
            command=self.save_interval,
            height=35
        ).pack(padx=15, pady=(0,15))
        
        # Carpeta de fondos
        folder_frame = ctk.CTkFrame(parent)
        folder_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            folder_frame,
            text="📁 Carpeta de Fondos (Persistente)",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15,10))
        
        self.use_folder_var = tk.BooleanVar(value=self.config_manager.get("use_folder", False))
        
        ctk.CTkCheckBox(
            folder_frame,
            text="Usar carpeta en lugar de lista manual",
            variable=self.use_folder_var,
            command=self.toggle_folder_mode
        ).pack(anchor='w', padx=15, pady=(0,10))
        
        folder_select_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_select_frame.pack(fill='x', padx=15, pady=(0,10))
        
        self.folder_entry = ctk.CTkEntry(
            folder_select_frame,
            placeholder_text="Selecciona una carpeta..."
        )
        self.folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        if self.config_manager.get("wallpaper_folder"):
            self.folder_entry.insert(0, self.config_manager.get("wallpaper_folder"))
        
        ctk.CTkButton(
            folder_select_frame,
            text="📂 Seleccionar Carpeta",
            command=self.select_wallpaper_folder,
            width=150
        ).pack(side='left')
        
        self.folder_info_label = ctk.CTkLabel(
            folder_frame,
            text=""
        )
        self.folder_info_label.pack(anchor='w', padx=15, pady=(0,15))
        self.update_folder_info()
        
        # Lista de fondos
        wallpapers_frame = ctk.CTkFrame(parent)
        wallpapers_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            wallpapers_frame,
            text="🖼️ Fondos de Pantalla (Lista Manual)",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15,10))
        
        # Textbox como lista
        self.wallpapers_textbox = ctk.CTkTextbox(
            wallpapers_frame,
            height=200
        )
        self.wallpapers_textbox.pack(fill='both', expand=True, padx=15, pady=(0,10))
        
        # Botones
        btn_frame = ctk.CTkFrame(wallpapers_frame, fg_color="transparent")
        btn_frame.pack(fill='x', padx=15, pady=(0,15))
        
        ctk.CTkButton(
            btn_frame,
            text="➕ Agregar Imagen",
            command=self.add_wallpaper,
            width=120
        ).pack(side='left', padx=(0,5))
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Refrescar Lista",
            command=self.refresh_wallpaper_list,
            width=120
        ).pack(side='left', padx=5)
    
    def setup_weekday_tab(self, parent) -> None:
        """Configura la pestaña de días de la semana"""
        ctk.CTkLabel(
            parent,
            text="Asigna un fondo de pantalla para cada día de la semana:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10,20))
        
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        day_icons = ["📌", "📌", "📌", "📌", "📌", "🎉", "🎉"]
        self.weekday_entries = {}
        
        for i, (day, icon) in enumerate(zip(days, day_icons)):
            frame = ctk.CTkFrame(parent)
            frame.pack(fill='x', padx=20, pady=5)
            
            ctk.CTkLabel(
                frame,
                text=f"{icon} {day}:",
                width=120,
                font=ctk.CTkFont(size=13)
            ).pack(side='left', padx=15, pady=10)
            
            entry = ctk.CTkEntry(
                frame,
                placeholder_text="Selecciona una imagen..."
            )
            entry.pack(side='left', padx=(0,10), fill='x', expand=True)
            self.weekday_entries[str(i)] = entry
            
            ctk.CTkButton(
                frame,
                text="📂 Seleccionar",
                command=lambda d=str(i): self.select_weekday_wallpaper(d),
                width=120
            ).pack(side='left', padx=(0,15))
        
        ctk.CTkButton(
            parent,
            text="💾 Guardar Configuración de Días",
            command=self.save_weekday_config,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20)
    
    def setup_startup_tab(self, parent) -> None:
        """Configura la pestaña de inicio automático"""
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="🚀 Inicio Automático con Windows",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20,10))
        
        ctk.CTkLabel(
            info_frame,
            text="Configura la aplicación para que se inicie automáticamente\ncuando Windows arranque.",
            font=ctk.CTkFont(size=13),
            justify='center'
        ).pack(pady=(0,20))
        
        self.startup_status_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.startup_status_label.pack(pady=10)
        
        btn_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        btn_frame.pack(pady=(10,20))
        
        ctk.CTkButton(
            btn_frame,
            text="✅ Habilitar Inicio Automático",
            command=self.enable_startup,
            width=220,
            height=40
        ).pack(side='left', padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Deshabilitar Inicio Automático",
            command=self.disable_startup,
            width=220,
            height=40,
            fg_color="gray40",
            hover_color="gray30"
        ).pack(side='left', padx=10)
        
        self.update_startup_status()
    
    # Métodos de eventos y acciones
    
    def load_current_config(self) -> None:
        """Carga la configuración actual en la interfaz"""
        # Cargar fondos por día
        weekday_wallpapers = self.config_manager.get("weekday_wallpapers", {})
        for day, wallpaper in weekday_wallpapers.items():
            if wallpaper:
                self.weekday_entries[day].insert(0, wallpaper)
        
        # Configurar estado inicial del botón
        if self.config_manager.get("mode") == "weekday":
            self.change_now_button.configure(state="disabled")
        else:
            self.change_now_button.configure(state="normal")
        
        # Cargar lista de fondos
        self.refresh_wallpaper_list()
    
    def on_mode_change(self) -> None:
        """Maneja el cambio de modo"""
        self.config_manager.set("mode", self.mode_var.get())
        self.config_manager.save_config()
        self.update_status()
        
        # Deshabilitar botón en modo días
        if self.mode_var.get() == "weekday":
            self.change_now_button.configure(state="disabled")
        else:
            self.change_now_button.configure(state="normal")
        
        messagebox.showinfo("Modo Cambiado", f"Modo cambiado a: {self.mode_var.get()}")
    
    def save_interval(self) -> None:
        """Guarda el intervalo de cambio"""
        self.config_manager.set("interval_minutes", self.interval_var.get())
        self.config_manager.save_config()
        self.update_status()
        messagebox.showinfo("Guardado", "Intervalo guardado correctamente")
    
    def add_wallpaper(self) -> None:
        """Agrega fondos de pantalla a la lista"""
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        wallpapers = self.config_manager.get("wallpapers", [])
        for file in files:
            if file not in wallpapers:
                wallpapers.append(file)
        
        self.config_manager.set("wallpapers", wallpapers)
        self.config_manager.save_config()
        self.refresh_wallpaper_list()
    
    def remove_wallpaper(self) -> None:
        """Elimina el fondo seleccionado - No disponible en textbox"""
        messagebox.showinfo(
            "Información",
            "Para eliminar fondos, edita el archivo de configuración o usa la lista manual."
        )
    
    def select_wallpaper_folder(self) -> None:
        """Selecciona una carpeta de fondos"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta con imágenes")
        
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.config_manager.set("wallpaper_folder", folder)
            self.config_manager.save_config()
            self.update_folder_info()
            messagebox.showinfo("Carpeta Seleccionada",
                              f"Carpeta configurada correctamente.\n\n{self.folder_info_label.cget('text')}")
    
    def toggle_folder_mode(self) -> None:
        """Activa/desactiva el modo de carpeta"""
        self.config_manager.set("use_folder", self.use_folder_var.get())
        self.config_manager.set("current_index", 0)
        self.config_manager.save_config()
        self.update_folder_info()
        self.refresh_wallpaper_list()
        
        mode_text = "carpeta" if self.use_folder_var.get() else "lista manual"
        messagebox.showinfo("Modo Cambiado", f"Ahora se usará: {mode_text}")
    
    def update_folder_info(self) -> None:
        """Actualiza la información de la carpeta"""
        if self.config_manager.get("use_folder", False):
            images = self.wallpaper_engine.get_images_from_folder()
            count = len(images)
            self.folder_info_label.configure(
                text=f"✓ Modo carpeta activo - {count} imagen(es) encontrada(s)",
                text_color="green"
            )
        else:
            if self.config_manager.get("wallpaper_folder"):
                images = self.wallpaper_engine.get_images_from_folder()
                count = len(images)
                self.folder_info_label.configure(
                    text=f"Carpeta configurada - {count} imagen(es) disponible(s) (modo desactivado)",
                    text_color="orange"
                )
            else:
                self.folder_info_label.configure(
                    text="No hay carpeta configurada",
                    text_color="gray"
                )
    
    def refresh_wallpaper_list(self) -> None:
        """Refresca la lista de fondos mostrada"""
        self.wallpapers_textbox.delete("1.0", tk.END)
        
        wallpapers = self.wallpaper_engine.get_wallpaper_list()
        if wallpapers:
            for i, wallpaper in enumerate(wallpapers, 1):
                self.wallpapers_textbox.insert(tk.END, f"{i}. {wallpaper}\n")
        else:
            self.wallpapers_textbox.insert(tk.END, "No hay imágenes configuradas")
        
        self.update_folder_info()
    
    def select_weekday_wallpaper(self, day: str) -> None:
        """Selecciona un fondo para un día específico"""
        file = filedialog.askopenfilename(
            title=f"Seleccionar fondo para el día",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file:
            self.weekday_entries[day].delete(0, tk.END)
            self.weekday_entries[day].insert(0, file)
    
    def save_weekday_config(self) -> None:
        """Guarda la configuración de días"""
        weekday_wallpapers = {}
        for day, entry in self.weekday_entries.items():
            value = entry.get()
            weekday_wallpapers[day] = value if value else None
        
        self.config_manager.set("weekday_wallpapers", weekday_wallpapers)
        self.config_manager.save_config()
        messagebox.showinfo("Guardado", "Configuración de días guardada correctamente")
    
    def change_now(self) -> None:
        """Cambia el fondo inmediatamente"""
        if self.wallpaper_engine.change_wallpaper():
            messagebox.showinfo("Éxito", "Fondo de pantalla cambiado correctamente")
            self.update_status()
        else:
            messagebox.showerror("Error", "No se pudo cambiar el fondo de pantalla")
    
    def update_status(self) -> None:
        """Actualiza el estado mostrado"""
        mode = "Tiempo" if self.config_manager.get("mode") == "time" else "Días de la semana"
        last_change = self.config_manager.get("last_change", "Nunca")
        
        if last_change != "Nunca":
            try:
                last_change = datetime.fromisoformat(last_change).strftime("%d/%m/%Y %H:%M:%S")
            except:
                pass
        
        # Información adicional
        if self.config_manager.get("mode") == "time":
            if self.config_manager.get("use_folder", False):
                images_count = len(self.wallpaper_engine.get_images_from_folder())
                source = f"Carpeta ({images_count} imágenes)"
            else:
                images_count = len(self.config_manager.get("wallpapers", []))
                source = f"Lista manual ({images_count} imágenes)"
            status_text = f"Modo actual: {mode}\nFuente: {source}\nÚltimo cambio: {last_change}"
        else:
            status_text = f"Modo actual: {mode}\nÚltimo cambio: {last_change}"
        
        self.status_label.configure(text=status_text)
    
    def update_countdown(self, minutes: int, seconds: int) -> None:
        """
        Actualiza el contador regresivo
        
        Args:
            minutes: Minutos restantes
            seconds: Segundos restantes
        """
        # Actualizar en la interfaz
        if self.config_manager.get("mode") == "time":
            if minutes > 0:
                countdown_text = f"⏰ Próximo cambio en: {minutes}m {seconds}s"
            else:
                countdown_text = f"⏰ Próximo cambio en: {seconds}s"
            
            # Usar after para actualizar desde el thread principal
            self.root.after(0, lambda: self.countdown_label.configure(text=countdown_text))
        else:
            self.root.after(0, lambda: self.countdown_label.configure(text=""))
        
        # Actualizar en el system tray
        if self.tray_manager:
            self.tray_manager.update_countdown(minutes, seconds)
    
    def enable_startup(self) -> None:
        """Habilita el inicio automático"""
        success, message = StartupManager.enable()
        if success:
            messagebox.showinfo("Éxito", message)
        else:
            messagebox.showerror("Error", message)
        self.update_startup_status()
    
    def disable_startup(self) -> None:
        """Deshabilita el inicio automático"""
        success, message = StartupManager.disable()
        if success:
            messagebox.showinfo("Éxito", message)
        else:
            messagebox.showerror("Error", message)
        self.update_startup_status()
    
    def update_startup_status(self) -> None:
        """Actualiza el estado del inicio automático"""
        enabled, status, color = StartupManager.get_status()
        self.startup_status_label.configure(text=status, text_color=color)
    
    # Métodos de bandeja del sistema
    
    def setup_system_tray(self) -> None:
        """Configura la bandeja del sistema"""
        self.tray_manager = SystemTrayManager(
            on_show=self.show_window,
            on_change_now=self.change_now_from_tray,
            on_quit=self.quit_app
        )
        self.tray_manager.setup()
    
    def show_window(self, icon=None, item=None) -> None:
        """Muestra la ventana principal"""
        self.root.after(0, self._show_window)
    
    def _show_window(self) -> None:
        """Método auxiliar para mostrar ventana"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide_window(self) -> None:
        """Oculta la ventana principal"""
        self.root.withdraw()
    
    def change_now_from_tray(self, icon=None, item=None) -> None:
        """Cambia el fondo desde la bandeja"""
        if self.config_manager.get("mode") == "weekday":
            return
        
        if self.wallpaper_engine.change_wallpaper():
            if self.tray_manager:
                self.tray_manager.notify(
                    "Fondo Cambiado",
                    "El fondo de pantalla se cambió correctamente"
                )
    
    def quit_app(self, icon=None, item=None) -> None:
        """Cierra completamente la aplicación"""
        self.wallpaper_engine.stop_monitoring()
        if self.tray_manager:
            self.tray_manager.stop()
        self.root.after(0, self.root.destroy)
    
    def on_closing(self) -> None:
        """Maneja el cierre de la aplicación"""
        # Minimizar a la bandeja en lugar de cerrar
        self.hide_window()
