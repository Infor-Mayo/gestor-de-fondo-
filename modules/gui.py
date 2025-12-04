"""
Módulo de interfaz gráfica
Maneja toda la interfaz de usuario con CustomTkinter
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Optional
from pathlib import Path

try:
    import darkdetect
    DARKDETECT_AVAILABLE = True
except ImportError:
    DARKDETECT_AVAILABLE = False

from .config_manager import ConfigManager
from .wallpaper_engine import WallpaperEngine
# Importar system tray de forma opcional
try:
    from .system_tray import SystemTrayManager
    SYSTEM_TRAY_AVAILABLE = True
except ImportError:
    SYSTEM_TRAY_AVAILABLE = False
    print("[ADVERTENCIA] Sistema de bandeja del sistema no disponible")
# Fallback tray simplificado
try:
    from .simple_tray import SimpleTrayManager
    SIMPLE_TRAY_AVAILABLE = True
except ImportError:
    SIMPLE_TRAY_AVAILABLE = False
from .startup_manager import StartupManager
from .drag_drop_handler import DragDropHandler


class WallpaperChangerGUI:
    """Interfaz gráfica principal de la aplicación"""

    def __init__(self, root: ctk.CTk):
        """
        Inicializa la interfaz gráfica

        Args:
            root: Ventana raíz de CustomTkinter
        """
        self.root = root
        # Configurar ventana
        self.root.title("Cambiador de Fondo de Pantalla v2.1")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # Configurar icono de la ventana
        try:
            import sys
            if getattr(sys, 'frozen', False):
                # Ejecutándose como EXE
                icon_path = os.path.join(sys._MEIPASS, 'assets', 'icon.ico')
            else:
                # Ejecutándose como script
                icon_path = os.path.join(os.path.dirname(
                    os.path.dirname(__file__)), 'assets', 'icon.ico')

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print(f"✅ Icono cargado: {icon_path}")
            else:
                print(f"⚠️ Icono no encontrado: {icon_path}")
        except Exception as e:
            print(f"⚠️ Error cargando icono: {e}")

        # Asegurar que aparezca en la barra de tareas
        self.root.attributes('-topmost', False)
        self.root.lift()
        self.root.focus_force()

        # NO configurar protocolo aquí - se configurará después de setup_system_tray

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

        # Configurar bandeja del sistema PRIMERO (antes de cualquier otra cosa)
        self.setup_system_tray()

        # IMPORTANTE: Configurar protocolo de cierre DESPUÉS de setup_system_tray
        # Esto asegura que cuando se cierre la ventana, se minimice a la bandeja
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Iniciar minimizado si se especifica
        if len(sys.argv) > 1 and '--minimized' in sys.argv:
            self.root.withdraw()  # Ocultar ventana al inicio

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
                base_path = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))

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
        ).pack(anchor='w', padx=15, pady=(15, 10))

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
        ).pack(anchor='w', padx=15, pady=(5, 15))

        # Botón de cambio manual
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.pack(fill='x', padx=10, pady=10)

        ctk.CTkLabel(
            btn_frame,
            text="Acción Manual",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15, 10))

        self.change_now_button = ctk.CTkButton(
            btn_frame,
            text="🔄 Cambiar Fondo Ahora",
            command=self.change_now,
            height=40
        )
        self.change_now_button.pack(padx=15, pady=(0, 15))

        # Estado
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill='x', padx=10, pady=10)

        ctk.CTkLabel(
            status_frame,
            text="Estado Actual",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15, 10))

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="",
            justify='left'
        )
        self.status_label.pack(anchor='w', padx=15, pady=(0, 5))

        # Contador regresivo
        self.countdown_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4CAF50"
        )
        self.countdown_label.pack(anchor='w', padx=15, pady=(0, 15))

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
        ).pack(anchor='w', padx=15, pady=(15, 10))

        interval_inner = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_inner.pack(fill='x', padx=15, pady=(0, 10))

        ctk.CTkLabel(
            interval_inner,
            text="Cambiar cada:"
        ).pack(side='left', padx=(0, 10))

        self.interval_var = tk.IntVar(
            value=self.config_manager.get("interval_minutes"))
        interval_entry = ctk.CTkEntry(
            interval_inner,
            textvariable=self.interval_var,
            width=100
        )
        interval_entry.pack(side='left', padx=(0, 10))

        ctk.CTkLabel(interval_inner, text="minutos").pack(side='left')

        ctk.CTkButton(
            interval_frame,
            text="💾 Guardar Intervalo",
            command=self.save_interval,
            height=35
        ).pack(padx=15, pady=(0, 15))

        # Carpeta de fondos
        folder_frame = ctk.CTkFrame(parent)
        folder_frame.pack(fill='x', padx=10, pady=10)

        ctk.CTkLabel(
            folder_frame,
            text="📁 Carpeta de Fondos - Imágenes y Videos (Persistente)",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15, 10))

        self.use_folder_var = tk.BooleanVar(
            value=self.config_manager.get("use_folder", False))

        ctk.CTkCheckBox(
            folder_frame,
            text="Usar carpeta en lugar de lista manual",
            variable=self.use_folder_var,
            command=self.toggle_folder_mode
        ).pack(anchor='w', padx=15, pady=(0, 10))

        folder_select_frame = ctk.CTkFrame(
            folder_frame, fg_color="transparent")
        folder_select_frame.pack(fill='x', padx=15, pady=(0, 10))

        self.folder_entry = ctk.CTkEntry(
            folder_select_frame,
            placeholder_text="Selecciona una carpeta..."
        )
        self.folder_entry.pack(side='left', fill='x',
                               expand=True, padx=(0, 10))
        if self.config_manager.get("wallpaper_folder"):
            self.folder_entry.insert(
                0, self.config_manager.get("wallpaper_folder"))

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
        self.folder_info_label.pack(anchor='w', padx=15, pady=(0, 15))
        self.update_folder_info()

        # Contenedor principal con scroll
        main_scroll_frame = ctk.CTkScrollableFrame(parent)
        main_scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Lista de fondos
        wallpapers_frame = ctk.CTkFrame(
            main_scroll_frame, fg_color="transparent")
        wallpapers_frame.pack(fill='both', expand=True, padx=0, pady=0)

        ctk.CTkLabel(
            wallpapers_frame,
            text="🖼️ Fondos de Pantalla - Imágenes y Videos (Lista Manual)",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor='w', padx=15, pady=(15, 10))

        # Zona de archivos (botones de acción)
        self.drop_zone_frame = ctk.CTkFrame(
            wallpapers_frame, fg_color="transparent")
        self.drop_zone_frame.pack(fill='x', padx=15, pady=(0, 10))

        # Frame para lista de wallpapers (sin scroll propio, usa el principal)
        self.wallpapers_list_frame = ctk.CTkFrame(wallpapers_frame)
        self.wallpapers_list_frame.pack(
            fill='both', expand=True, padx=15, pady=(0, 10))

        # Configurar drag & drop después de que la ventana esté lista
        self.root.after(500, self.setup_working_drag_drop)

        # Botones
        btn_frame = ctk.CTkFrame(wallpapers_frame, fg_color="transparent")
        btn_frame.pack(fill='x', padx=15, pady=(0, 15))

        ctk.CTkButton(
            btn_frame,
            text="➕ Agregar Imagen/Video",
            command=self.add_wallpaper,
            width=140
        ).pack(side='left', padx=(0, 5))

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
            text="Configura múltiples imágenes o una carpeta por día y el intervalo de rotación:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 10))

        # Intervalo de rotación para modo día
        interval_frame = ctk.CTkFrame(parent)
        interval_frame.pack(fill='x', padx=20, pady=(0, 10))
        ctk.CTkLabel(interval_frame, text="Intervalo (min) para rotación intra-día:").pack(side='left', padx=(10, 10))
        self.weekday_rotation_var = tk.IntVar(value=self.config_manager.get("weekday_rotation_minutes", 30))
        self.weekday_rotation_entry = ctk.CTkEntry(interval_frame, textvariable=self.weekday_rotation_var, width=80)
        self.weekday_rotation_entry.pack(side='left')

        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.weekday_use_folder_vars = {}
        self.weekday_folder_entries = {}
        self.weekday_summary_labels = {}
        self.weekday_selected_images = {}

        for i, day in enumerate(days):
            dkey = str(i)
            self.weekday_selected_images[dkey] = []

            outer = ctk.CTkFrame(parent)
            outer.pack(fill='x', padx=20, pady=8)

            # Encabezado y toggle
            header = ctk.CTkFrame(outer, fg_color="transparent")
            header.pack(fill='x')
            ctk.CTkLabel(header, text=f"📅 {day}", font=ctk.CTkFont(size=13, weight="bold"), width=120).pack(side='left', padx=(10, 10))
            self.weekday_use_folder_vars[dkey] = tk.BooleanVar(value=False)
            ctk.CTkCheckBox(
                header,
                text="Usar carpeta",
                variable=self.weekday_use_folder_vars[dkey],
                command=lambda d=dkey: self.on_day_use_folder_toggle(d)
            ).pack(side='left')

            # Selector de carpeta
            folder_row = ctk.CTkFrame(outer, fg_color="transparent")
            folder_row.pack(fill='x', pady=(6, 4))
            self.weekday_folder_entries[dkey] = ctk.CTkEntry(folder_row, placeholder_text="Selecciona una carpeta de imágenes…")
            self.weekday_folder_entries[dkey].pack(side='left', fill='x', expand=True, padx=(10, 10))
            ctk.CTkButton(folder_row, text="📁 Carpeta", width=120, command=lambda d=dkey: self.select_weekday_folder(d)).pack(side='left', padx=(0, 10))

            # Selector de múltiples imágenes
            actions = ctk.CTkFrame(outer, fg_color="transparent")
            actions.pack(fill='x')
            ctk.CTkButton(actions, text="➕ Agregar imágenes", command=lambda d=dkey: self.select_weekday_images(d), width=160).pack(side='left', padx=(10, 10))
            self.weekday_summary_labels[dkey] = ctk.CTkLabel(actions, text="0 imágenes")
            self.weekday_summary_labels[dkey].pack(side='left')

        # Botón guardar
        ctk.CTkButton(
            parent,
            text="💾 Guardar Configuración de Días",
            command=self.save_weekday_config,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=15)

    def setup_startup_tab(self, parent) -> None:
        """Configura la pestaña de inicio automático"""
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill='x', padx=10, pady=10)

        ctk.CTkLabel(
            info_frame,
            text="🚀 Inicio Automático con Windows",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            info_frame,
            text="Configura la aplicación para que se inicie automáticamente\ncuando Windows arranque.",
            font=ctk.CTkFont(size=13),
            justify='center'
        ).pack(pady=(0, 20))

        self.startup_status_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.startup_status_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

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
        # Rotación intra-día
        rotation = self.config_manager.get("weekday_rotation_minutes", 30)
        if hasattr(self, "weekday_rotation_var"):
            try:
                self.weekday_rotation_var.set(int(rotation))
            except:
                self.weekday_rotation_var.set(30)

        # Cargar playlists por día con compatibilidad legacy
        playlists = self.config_manager.get("weekday_playlists", {})
        legacy = self.config_manager.get("weekday_wallpapers", {})

        for i in range(7):
            key = str(i)
            use_folder = False
            folder = ""
            images = []

            if key in playlists:
                data = playlists.get(key) or {}
                use_folder = bool(data.get("use_folder", False))
                folder = data.get("folder") or ""
                images = data.get("images") or []
            else:
                # Fallback legacy: una sola imagen por día
                path = legacy.get(key)
                if path:
                    images = [path]

            # Poblar UI
            if hasattr(self, "weekday_use_folder_vars") and key in self.weekday_use_folder_vars:
                self.weekday_use_folder_vars[key].set(use_folder)
            if hasattr(self, "weekday_folder_entries") and key in self.weekday_folder_entries:
                entry = self.weekday_folder_entries[key]
                entry.delete(0, tk.END)
                if folder:
                    entry.insert(0, folder)
            if hasattr(self, "weekday_selected_images"):
                self.weekday_selected_images[key] = images
            if hasattr(self, "weekday_summary_labels") and key in self.weekday_summary_labels:
                self.weekday_summary_labels[key].configure(text=f"{len(images)} imágenes")

        # Configurar estado inicial del botón
        if self.config_manager.get("mode") == "weekday":
            self.change_now_button.configure(state="disabled")
        else:
            self.change_now_button.configure(state="normal")

        # Cargar lista de fondos (modo tiempo)
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

        messagebox.showinfo(
            "Modo Cambiado", f"Modo cambiado a: {self.mode_var.get()}")

    def save_interval(self) -> None:
        """Guarda el intervalo de cambio"""
        self.config_manager.set("interval_minutes", self.interval_var.get())
        self.config_manager.save_config()
        self.update_status()
        messagebox.showinfo("Guardado", "Intervalo guardado correctamente")

    def add_wallpaper(self) -> None:
        """Agrega fondos de pantalla (imágenes y videos) a la lista"""
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes y videos",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp"),
                ("Videos", "*.mp4 *.avi *.mov *.wmv *.mkv *.flv *.webm *.m4v"),
                ("Imágenes y Videos",
                 "*.jpg *.jpeg *.png *.bmp *.mp4 *.avi *.mov *.wmv *.mkv *.flv *.webm *.m4v"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not files:
            print("No se seleccionaron archivos")
            return

        print(f"📁 Archivos seleccionados: {len(files)}")

        wallpapers = self.config_manager.get("wallpapers", [])
        added_files = []

        for file in files:
            print(f"🔍 Procesando archivo: {file}")

            # Verificar extensión
            file_ext = Path(file).suffix.lower()
            print(f"   Extensión: {file_ext}")

            # Verificar si es video
            is_video = self.wallpaper_engine.video_engine.is_video_file(file)
            print(f"   ¿Es video?: {is_video}")

            if file not in wallpapers:
                wallpapers.append(file)
                added_files.append(file)
                # Determinar tipo de archivo
                file_type = "🎬 Video" if is_video else "🖼️ Imagen"
                print(f"  ✅ Agregado: {file_type} - {os.path.basename(file)}")
            else:
                print(f"  ⚠️ Ya existe: {os.path.basename(file)}")

        if added_files:
            self.config_manager.set("wallpapers", wallpapers)
            self.config_manager.save_config()

            # Forzar actualización inmediata
            print("💾 Configuración guardada, refrescando lista...")

            def force_refresh():
                # Recargar configuración para asegurar que esté actualizada
                self.config_manager.load_config()
                self.refresh_wallpaper_list()
                print("🔄 Lista actualizada forzosamente")

            self.root.after(100, force_refresh)

            # Mostrar mensaje de confirmación
            image_count = sum(
                1 for f in added_files if not self.wallpaper_engine.video_engine.is_video_file(f))
            video_count = len(added_files) - image_count

            message = f"✅ Se agregaron {len(added_files)} archivo(s):\n"
            if image_count > 0:
                message += f"   • {image_count} imagen(es)\n"
            if video_count > 0:
                message += f"   • {video_count} video(s)\n"

            messagebox.showinfo("Archivos Agregados", message)
        else:
            messagebox.showinfo(
                "Sin Cambios", "Todos los archivos seleccionados ya están en la lista.")

    def remove_wallpaper(self) -> None:
        """Elimina el fondo seleccionado - No disponible en textbox"""
        messagebox.showinfo(
            "Información",
            "Para eliminar fondos, edita el archivo de configuración o usa la lista manual."
        )

    def select_wallpaper_folder(self) -> None:
        """Selecciona una carpeta de fondos"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta con imágenes y videos")

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
            media_files = self.wallpaper_engine.get_media_from_folder()
            videos = [
                f for f in media_files if self.wallpaper_engine.video_engine.is_video_file(f)]
            images = [
                f for f in media_files if not self.wallpaper_engine.video_engine.is_video_file(f)]

            total_count = len(media_files)
            image_count = len(images)
            video_count = len(videos)

            self.folder_info_label.configure(
                text=f"✓ Modo carpeta activo - {total_count} archivo(s): {image_count} imagen(es), {video_count} video(s)",
                text_color="green"
            )
        else:
            if self.config_manager.get("wallpaper_folder"):
                media_files = self.wallpaper_engine.get_media_from_folder()
                videos = [
                    f for f in media_files if self.wallpaper_engine.video_engine.is_video_file(f)]
                images = [
                    f for f in media_files if not self.wallpaper_engine.video_engine.is_video_file(f)]

                total_count = len(media_files)
                image_count = len(images)
                video_count = len(videos)

                self.folder_info_label.configure(
                    text=f"Carpeta configurada - {total_count} archivo(s): {image_count} imagen(es), {video_count} video(s) (modo desactivado)",
                    text_color="orange"
                )
            else:
                self.folder_info_label.configure(
                    text="No hay carpeta configurada",
                    text_color="gray"
                )

    def refresh_wallpaper_list(self) -> None:
        """Refresca la lista de fondos mostrada con botones reales"""
        # Limpiar frame anterior
        for widget in self.wallpapers_list_frame.winfo_children():
            widget.destroy()

        # Crear frame interno con scroll para la lista de archivos
        inner_scroll_frame = ctk.CTkScrollableFrame(
            self.wallpapers_list_frame,
            height=300,
            label_text="Archivos en la Lista"
        )
        inner_scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)

        wallpapers = self.wallpaper_engine.get_wallpaper_list()
        print(f"🔄 Refrescando lista: {len(wallpapers)} archivo(s)")

        if wallpapers:
            # Separar imágenes y videos
            images = []
            videos = []

            print(f"🔍 Analizando {len(wallpapers)} archivos:")
            for wallpaper in wallpapers:
                # Verificar si el archivo existe
                if not os.path.exists(wallpaper):
                    print(
                        f"⚠️ Archivo no encontrado: {os.path.basename(wallpaper)}")
                    # Aún así agregarlo para que el usuario pueda eliminarlo

                filename = os.path.basename(wallpaper)
                ext = Path(wallpaper).suffix.lower()
                is_video = self.wallpaper_engine.video_engine.is_video_file(
                    wallpaper)

                print(f"  {filename} ({ext}) -> Video: {is_video}")

                if is_video:
                    videos.append(wallpaper)
                else:
                    images.append(wallpaper)

            # Mostrar resumen
            total_count = len(wallpapers)
            image_count = len(images)
            video_count = len(videos)

            print(
                f"📊 Resultado: {total_count} total = {image_count} imágenes + {video_count} videos")

            # Verificar que no se pierdan archivos
            if (image_count + video_count) != total_count:
                print(
                    f"⚠️ ERROR: Se perdieron archivos! {total_count} != {image_count + video_count}")
                # Mostrar todos los archivos sin separar
                print("📋 Lista completa de archivos:")
                for i, wallpaper in enumerate(wallpapers):
                    print(f"  {i+1}. {os.path.basename(wallpaper)}")

                # Usar todos como imágenes si hay problema de detección
                images = wallpapers
                videos = []
                image_count = len(images)
                video_count = 0
                print("🔧 Usando todos los archivos como imágenes para evitar pérdida")

            # Etiqueta de resumen
            summary_label = ctk.CTkLabel(
                inner_scroll_frame,
                text=f"📊 Total: {total_count} archivo(s) - 🖼️ {image_count} imágenes, 🎬 {video_count} videos",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            summary_label.pack(pady=(0, 10))

            # Mostrar videos primero
            if videos:
                video_label = ctk.CTkLabel(
                    inner_scroll_frame,
                    text="🎬 VIDEOS:",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#4CAF50"
                )
                video_label.pack(anchor='w', pady=(10, 5))

                for video_path in videos:
                    self.create_file_item(video_path, "🎬", inner_scroll_frame)

            # Mostrar imágenes después
            if images:
                image_label = ctk.CTkLabel(
                    inner_scroll_frame,
                    text="🖼️ IMÁGENES:",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#2196F3"
                )
                image_label.pack(anchor='w', pady=(10, 5))

                for image_path in images:
                    self.create_file_item(image_path, "🖼️", inner_scroll_frame)

            print(
                f"📊 Lista mostrada: {image_count} imágenes, {video_count} videos")
        else:
            print("  Lista vacía, mostrando mensaje de ayuda")
            # Mostrar mensaje cuando esté vacío
            empty_label = ctk.CTkLabel(
                inner_scroll_frame,
                text="📋 Lista vacía\n\n💡 Usa los botones de arriba para agregar archivos:\n• 📁 Zona de Archivos\n• 📂 Seleccionar Carpeta\n• ➕ Agregar Imagen/Video",
                font=ctk.CTkFont(size=12),
                justify="center"
            )
            empty_label.pack(expand=True, pady=20)

        self.update_folder_info()

    def create_file_item(self, file_path: str, icon: str, parent_frame=None):
        """Crea un elemento de archivo con botón de eliminar"""
        if parent_frame is None:
            parent_frame = self.wallpapers_list_frame

        filename = os.path.basename(file_path)

        # Verificar si el archivo existe
        exists = os.path.exists(file_path)
        status_icon = "✅" if exists else "❌"

        # Frame para cada archivo
        item_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        item_frame.pack(fill='x', pady=2)

        # Etiqueta con el archivo
        display_text = f"{status_icon} {icon} {filename}"
        text_color = "white" if exists else "gray"

        file_label = ctk.CTkLabel(
            item_frame,
            text=display_text,
            font=ctk.CTkFont(size=11),
            anchor="w",
            text_color=text_color
        )
        file_label.pack(side='left', fill='x', expand=True, padx=(5, 0))

        # Botón de eliminar
        delete_btn = ctk.CTkButton(
            item_frame,
            text="🗑️",
            width=30,
            height=25,
            font=ctk.CTkFont(size=12),
            fg_color="#d32f2f",
            hover_color="#f44336",
            command=lambda: self.remove_wallpaper_by_path(file_path)
        )
        delete_btn.pack(side='right', padx=(5, 0))

    def remove_wallpaper_by_path(self, file_path: str):
        """Elimina un wallpaper por su ruta completa"""
        try:
            import tkinter.messagebox as msgbox

            filename = os.path.basename(file_path)

            # Confirmar eliminación
            result = msgbox.askyesno(
                "🗑️ Eliminar Archivo",
                f"¿Eliminar este archivo de la lista?\n\n{filename}",
                icon="warning"
            )

            if result:
                wallpapers = self.config_manager.get("wallpapers", [])

                if file_path in wallpapers:
                    wallpapers.remove(file_path)

                    # Guardar configuración
                    self.config_manager.set("wallpapers", wallpapers)
                    self.config_manager.save_config()

                    # Actualizar lista
                    def force_refresh():
                        self.config_manager.load_config()
                        self.refresh_wallpaper_list()
                        print(f"🗑️ Eliminado: {filename}")

                    self.root.after(100, force_refresh)

                    msgbox.showinfo("Eliminado", f"✅ Se eliminó: {filename}")
                else:
                    msgbox.showwarning(
                        "No Encontrado", f"El archivo ya no está en la lista.")

        except Exception as e:
            print(f"Error eliminando archivo: {e}")
            messagebox.showerror("Error", f"Error eliminando archivo: {e}")

    def on_day_use_folder_toggle(self, day: str) -> None:
        """Actualiza el resumen al alternar 'Usar carpeta'"""
        self.update_day_summary(day)

    def update_day_summary(self, day: str) -> None:
        count = len(self.weekday_selected_images.get(day, []))
        self.weekday_summary_labels[day].configure(text=f"{count} imágenes")

    def select_weekday_folder(self, day: str) -> None:
        """Selecciona una carpeta de imágenes para un día"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de imágenes para el día")
        if folder:
            self.weekday_folder_entries[day].delete(0, tk.END)
            self.weekday_folder_entries[day].insert(0, folder)
            self.weekday_use_folder_vars[day].set(True)
            self.update_day_summary(day)

    def select_weekday_images(self, day: str) -> None:
        """Agrega múltiples imágenes para un día"""
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes para el día",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if not files:
            return
        current = self.weekday_selected_images.get(day, [])
        added = [f for f in files if f not in current]
        self.weekday_selected_images[day] = current + added
        # Al agregar imágenes, priorizamos lista manual
        self.weekday_use_folder_vars[day].set(False)
        self.update_day_summary(day)
        messagebox.showinfo("Imágenes agregadas", f"Se agregaron {len(added)} imagen(es) al día.")

    def save_weekday_config(self) -> None:
        """Guarda la configuración de playlists por día y el intervalo"""
        playlists = {}
        legacy = {}
        for i in range(7):
            key = str(i)
            use_folder = bool(self.weekday_use_folder_vars[key].get())
            folder = self.weekday_folder_entries[key].get().strip()
            images = self.weekday_selected_images.get(key, [])
            playlists[key] = {
                "use_folder": use_folder,
                "folder": folder if folder else None,
                "images": images
            }
            # Compatibilidad legacy: una imagen por día cuando no se usa carpeta
            legacy[key] = images[0] if (images and not use_folder) else None

        self.config_manager.set("weekday_playlists", playlists)
        self.config_manager.set("weekday_rotation_minutes", int(self.weekday_rotation_var.get()))
        self.config_manager.set("weekday_wallpapers", legacy)
        self.config_manager.save_config()
        messagebox.showinfo("Guardado", "Configuración de días guardada correctamente")

    def change_now(self) -> None:
        """Cambia el fondo inmediatamente"""
        if self.wallpaper_engine.change_wallpaper():
            messagebox.showinfo(
                "Éxito", "Fondo de pantalla cambiado correctamente")
            self.update_status()
        else:
            messagebox.showerror(
                "Error", "No se pudo cambiar el fondo de pantalla")

    def update_status(self) -> None:
        """Actualiza el estado mostrado"""
        mode = "Tiempo" if self.config_manager.get(
            "mode") == "time" else "Días de la semana"
        last_change = self.config_manager.get("last_change", "Nunca")

        if last_change != "Nunca":
            try:
                last_change = datetime.fromisoformat(
                    last_change).strftime("%d/%m/%Y %H:%M:%S")
            except:
                pass

        # Información adicional
        if self.config_manager.get("mode") == "time":
            if self.config_manager.get("use_folder", False):
                media_files = self.wallpaper_engine.get_media_from_folder()
                media_count = len(media_files)
                source = f"Carpeta ({media_count} archivo(s))"
            else:
                media_files = self.config_manager.get("wallpapers", [])
                media_count = len(media_files)
                source = f"Lista manual ({media_count} archivo(s))"
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
        try:
            # Verificar que la ventana aún existe
            if not hasattr(self, 'root') or not self.root.winfo_exists():
                return

            # Actualizar en la interfaz
            if self.config_manager.get("mode") == "time":
                if minutes > 0:
                    countdown_text = f"⏰ Próximo cambio en: {minutes}m {seconds}s"
                else:
                    countdown_text = f"⏰ Próximo cambio en: {seconds}s"

                # Usar after para actualizar desde el thread principal de forma segura
                try:
                    self.root.after_idle(
                        lambda text=countdown_text: self.countdown_label.configure(text=text))
                except tk.TclError:
                    # La ventana fue cerrada, ignorar
                    pass
            else:
                try:
                    self.root.after_idle(
                        lambda: self.countdown_label.configure(text=""))
                except tk.TclError:
                    # La ventana fue cerrada, ignorar
                    pass
        except Exception as e:
            # Silenciar errores de threading al cerrar la aplicación
            pass

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
        """Configura la bandeja del sistema y lo inicia UNA SOLA VEZ"""
        if SYSTEM_TRAY_AVAILABLE:
            self.tray_manager = SystemTrayManager(
                root=self.root,  # Pasar root para usar root.after()
                on_show=self.show_window,
                on_change_now=self.change_now_from_tray,
                on_quit=self.quit_app
            )
            # Iniciar el icono UNA SOLA VEZ al inicio
            self.tray_manager.setup()
            print("✅ System tray iniciado al arranque")
        elif 'SIMPLE_TRAY_AVAILABLE' in globals() and SIMPLE_TRAY_AVAILABLE:
            # Fallback cuando pystray no está disponible o falla la importación
            self.tray_manager = SimpleTrayManager(
                on_show=self.show_window,
                on_quit=self.quit_app
            )
            self.tray_manager.setup()
            # Enlazar acción de cambio ahora si es posible
            try:
                self.tray_manager.change_wallpaper = self.change_now_from_tray
            except Exception:
                pass
            # Forzar visibilidad si el gestor lo soporta
            if hasattr(self.tray_manager, 'set_visible'):
                try:
                    self.tray_manager.set_visible(True)
                except Exception:
                    pass
            print("✅ System tray simple iniciado")
        else:
            self.tray_manager = None

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
        # Asegurar visibilidad del icono en la bandeja si el gestor lo soporta
        if self.tray_manager and hasattr(self.tray_manager, 'set_visible'):
            try:
                self.tray_manager.set_visible(True)
            except Exception:
                pass

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
        """Maneja el cierre de la aplicación - minimiza a bandeja si disponible"""
        if self.tray_manager:
            # Ocultar ventana CTk (el icono ya está corriendo desde el inicio)
            self.hide_window()

            # Notificar que la app sigue corriendo
            try:
                self.tray_manager.notify(
                    "Aplicación minimizada",
                    "La aplicación sigue ejecutándose en segundo plano."
                )
            except Exception:
                pass
        else:
            # Si no hay bandeja disponible, cerrar completamente para evitar quedar "perdida"
            self.quit_app()

    def setup_drag_drop(self) -> None:
        """Configura la funcionalidad de arrastrar y soltar"""
        try:
            # Usar implementación simple y robusta
            self.setup_simple_drag_drop()
        except Exception as e:
            print(f"Error configurando drag & drop: {e}")
            # Usar método básico como respaldo
            self.setup_drag_drop_basic()

        print("Drag & drop configurado exitosamente")

    def setup_working_drag_drop(self) -> None:
        """Configura método alternativo de agregar archivos"""
        try:
            # Configurar eventos en el frame de lista
            list_widget = self.wallpapers_list_frame

            # Crear área de drop visual
            self.create_drop_zone()

            # Configurar eventos alternativos en el frame de lista
            list_widget.bind('<Button-3>', self.show_enhanced_menu)
            list_widget.bind('<Double-Button-1>', self.quick_add_files)

            # La ayuda ahora se muestra automáticamente en refresh_wallpaper_list cuando está vacío

            print("✅ Método alternativo de archivos configurado")

        except Exception as e:
            print(f"❌ Error configurando método alternativo: {e}")
            self.setup_fallback_drag_drop()

    def create_drop_zone(self):
        """Crea una zona visual para 'simular' drag & drop"""
        try:
            # Usar el frame dedicado para la zona de archivos
            drop_frame = self.drop_zone_frame

            drop_button = ctk.CTkButton(
                drop_frame,
                text="📁 ZONA DE ARCHIVOS - Clic aquí para agregar",
                command=self.add_wallpaper,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#2B2B2B",
                hover_color="#404040"
            )
            drop_button.pack(fill='x', padx=5, pady=5)

            # Botón adicional para carpeta
            folder_button = ctk.CTkButton(
                drop_frame,
                text="📂 Seleccionar Carpeta Completa",
                command=self.select_folder_quick,
                height=35,
                fg_color="#1f538d",
                hover_color="#2d5aa0"
            )
            folder_button.pack(fill='x', padx=5, pady=(0, 5))

            # Botón para limpiar lista
            clear_button = ctk.CTkButton(
                drop_frame,
                text="🗑️ Limpiar Lista Completa",
                command=self.clear_wallpaper_list,
                height=35,
                fg_color="#d32f2f",
                hover_color="#f44336"
            )
            clear_button.pack(fill='x', padx=5, pady=(0, 5))

            # Botón para instalar menú contextual
            context_menu_button = ctk.CTkButton(
                drop_frame,
                text="⚙️ Instalar Menú Contextual",
                command=self.install_context_menu,
                height=35,
                fg_color="#9C27B0",
                hover_color="#BA68C8"
            )
            context_menu_button.pack(fill='x', padx=5, pady=(0, 5))

            print("✅ Zona de archivos creada")

        except Exception as e:
            print(f"Error creando zona de drop: {e}")

    def select_folder_quick(self):
        """Selector rápido de carpeta"""
        try:
            from tkinter import filedialog

            folder = filedialog.askdirectory(
                title="Seleccionar carpeta con imágenes y videos"
            )

            if folder:
                # Obtener todos los archivos de la carpeta
                media_files = self.wallpaper_engine.get_media_from_folder(
                    folder)

                if media_files:
                    # Agregar todos los archivos
                    wallpapers = self.config_manager.get("wallpapers", [])
                    added_count = 0

                    for file_path in media_files:
                        if file_path not in wallpapers:
                            wallpapers.append(file_path)
                            added_count += 1

                    if added_count > 0:
                        self.config_manager.set("wallpapers", wallpapers)
                        self.config_manager.save_config()
                        self.refresh_wallpaper_list()

                        messagebox.showinfo(
                            "Carpeta Agregada",
                            f"✅ Se agregaron {added_count} archivo(s) de la carpeta:\n{folder}"
                        )
                    else:
                        messagebox.showinfo(
                            "Sin Cambios",
                            "Todos los archivos de la carpeta ya están en la lista."
                        )
                else:
                    messagebox.showwarning(
                        "Carpeta Vacía",
                        "No se encontraron imágenes o videos en la carpeta seleccionada."
                    )

        except Exception as e:
            print(f"Error seleccionando carpeta: {e}")
            messagebox.showerror("Error", f"Error seleccionando carpeta: {e}")

    def show_enhanced_menu(self, event):
        """Menú contextual mejorado con opciones de eliminación"""
        try:
            import tkinter as tk

            # Crear menú contextual
            context_menu = tk.Menu(self.root, tearoff=0)

            # Opciones de agregar
            context_menu.add_command(
                label="📁 Agregar Archivos Individuales",
                command=self.add_wallpaper
            )
            context_menu.add_command(
                label="📂 Agregar Carpeta Completa",
                command=self.select_folder_quick
            )

            context_menu.add_separator()

            # Opciones de eliminar
            context_menu.add_command(
                label="🗑️ Eliminar Archivo Específico",
                command=self.show_delete_menu
            )
            context_menu.add_command(
                label="🗑️ Limpiar Lista Completa",
                command=self.clear_wallpaper_list
            )

            context_menu.add_separator()

            # Opción de ayuda
            context_menu.add_command(
                label="❓ Ayuda",
                command=self.show_help_dialog
            )

            # Mostrar menú en la posición del cursor
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

        except Exception as e:
            print(f"Error en menú contextual: {e}")

    def show_delete_menu(self):
        """Muestra menú para eliminar archivos específicos"""
        try:
            wallpapers = self.config_manager.get("wallpapers", [])

            if not wallpapers:
                messagebox.showinfo(
                    "Lista Vacía", "No hay archivos para eliminar.")
                return

            # Crear lista de nombres de archivo
            filenames = [os.path.basename(w) for w in wallpapers]

            # Crear ventana de selección
            delete_window = ctk.CTkToplevel(self.root)
            delete_window.title("🗑️ Eliminar Archivo")
            delete_window.geometry("500x400")
            delete_window.transient(self.root)
            delete_window.grab_set()

            # Etiqueta
            ctk.CTkLabel(
                delete_window,
                text="Selecciona el archivo a eliminar:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(pady=10)

            # Lista de archivos
            listbox_frame = ctk.CTkFrame(delete_window)
            listbox_frame.pack(fill='both', expand=True, padx=20, pady=10)

            # Usar Listbox nativo para selección
            import tkinter as tk
            listbox = tk.Listbox(listbox_frame, font=('Arial', 10))
            listbox.pack(fill='both', expand=True, padx=10, pady=10)

            # Agregar archivos a la lista
            for filename in filenames:
                listbox.insert(tk.END, filename)

            # Botones
            button_frame = ctk.CTkFrame(delete_window, fg_color="transparent")
            button_frame.pack(fill='x', padx=20, pady=10)

            def delete_selected():
                selection = listbox.curselection()
                if selection:
                    filename = filenames[selection[0]]
                    delete_window.destroy()
                    self.remove_wallpaper_by_name(filename)
                else:
                    messagebox.showwarning(
                        "Sin Selección", "Selecciona un archivo para eliminar.")

            ctk.CTkButton(
                button_frame,
                text="🗑️ Eliminar Seleccionado",
                command=delete_selected,
                fg_color="#d32f2f",
                hover_color="#f44336"
            ).pack(side='left', padx=5)

            ctk.CTkButton(
                button_frame,
                text="❌ Cancelar",
                command=delete_window.destroy
            ).pack(side='right', padx=5)

        except Exception as e:
            print(f"Error en menú de eliminación: {e}")
            messagebox.showerror(
                "Error", f"Error mostrando menú de eliminación: {e}")

    def show_help_dialog(self):
        """Muestra diálogo de ayuda"""
        try:
            help_text = (
                "🖱️ AYUDA - GESTIÓN DE ARCHIVOS\n\n"
                "📁 AGREGAR ARCHIVOS:\n"
                "• Botón '📁 ZONA DE ARCHIVOS'\n"
                "• Botón '📂 Seleccionar Carpeta'\n"
                "• Clic derecho → Agregar\n"
                "• Doble clic en área de texto\n"
                "• Ctrl+O (atajo de teclado)\n\n"
                "🗑️ ELIMINAR ARCHIVOS:\n"
                "• Botón '🗑️ Limpiar Lista' (todo)\n"
                "• Clic derecho → Eliminar específico\n"
                "• Ctrl+D (atajo de teclado)\n\n"
                "🎬 FORMATOS SOPORTADOS:\n"
                "• Imágenes: JPG, PNG, BMP\n"
                "• Videos: MP4, AVI, MOV, WMV, MKV\n\n"
                "💡 CONSEJOS:\n"
                "• Usa lista manual para mejor control\n"
                "• Los videos pueden tardar en cargar\n"
                "• Revisa que los archivos existan"
            )

            messagebox.showinfo("Ayuda", help_text)

        except Exception as e:
            print(f"Error mostrando ayuda: {e}")

    def install_context_menu(self):
        """Instala el menú contextual del explorador"""
        try:
            import tkinter.messagebox as msgbox

            # Confirmar instalación
            result = msgbox.askyesno(
                "⚙️ Instalar Menú Contextual",
                "¿Instalar menú contextual en el Explorador de Windows?\n\n"
                "Esto agregará la opción '🖼️ Agregar a Lista de Fondos'\n"
                "al hacer clic derecho en imágenes y videos.\n\n"
                "La instalación es segura y reversible.",
                icon="question"
            )

            if result:
                # Importar e instalar
                try:
                    import sys
                    import os

                    # Agregar directorio actual al path
                    current_dir = os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__)))
                    if current_dir not in sys.path:
                        sys.path.append(current_dir)

                    # Importar función de instalación
                    from install_context_menu import install_context_menu

                    # Instalar
                    success = install_context_menu()

                    if success:
                        msgbox.showinfo(
                            "✅ Instalado",
                            "¡Menú contextual instalado exitosamente!\n\n"
                            "Ahora puedes hacer clic derecho en imágenes y videos\n"
                            "desde el Explorador de Windows y seleccionar\n"
                            "'🖼️ Agregar a Lista de Fondos'.\n\n"
                            "💡 Si no aparece inmediatamente, reinicia el Explorador:\n"
                            "Ctrl+Shift+Esc → Procesos → Windows Explorer → Reiniciar"
                        )
                    else:
                        msgbox.showerror(
                            "❌ Error",
                            "No se pudo instalar el menú contextual.\n\n"
                            "Verifica que tengas permisos suficientes\n"
                            "o ejecuta la aplicación como administrador."
                        )

                except ImportError:
                    msgbox.showerror(
                        "❌ Error",
                        "No se encontró el módulo de instalación.\n\n"
                        "Asegúrate de que 'install_context_menu.py'\n"
                        "esté en el mismo directorio que la aplicación."
                    )
                except Exception as e:
                    msgbox.showerror(
                        "❌ Error",
                        f"Error instalando menú contextual:\n\n{str(e)}"
                    )

        except Exception as e:
            print(f"Error en install_context_menu: {e}")
            messagebox.showerror("Error", f"Error: {e}")

    def add_enhanced_help_text(self):
        """Agrega texto de ayuda mejorado"""
        try:
            current_text = self.wallpapers_textbox.get("1.0", tk.END)
            if not current_text.strip() or "No hay imágenes o videos configurados" in current_text:
                self.wallpapers_textbox.delete("1.0", tk.END)
                self.wallpapers_textbox.insert("1.0",
                                               "📋 Lista de fondos de pantalla\n\n"
                                               "🎯 MÉTODOS PARA AGREGAR ARCHIVOS:\n\n"
                                               "1️⃣ BOTONES SUPERIORES:\n"
                                               "   • 📁 'ZONA DE ARCHIVOS' - Seleccionar archivos\n"
                                               "   • 📂 'Seleccionar Carpeta' - Carpeta completa\n\n"
                                               "2️⃣ CLIC DERECHO aquí:\n"
                                               "   • Menú con opciones de archivos/carpeta\n\n"
                                               "3️⃣ DOBLE CLIC aquí:\n"
                                               "   • Selector rápido de archivos\n\n"
                                               "4️⃣ TECLADO:\n"
                                               "   • Ctrl+O - Abrir selector de archivos\n\n"
                                               "5️⃣ BOTÓN TRADICIONAL:\n"
                                               "   • '➕ Agregar Imagen/Video' (abajo)\n\n"
                                               "🎬 Formatos soportados:\n"
                                               "   • Imágenes: JPG, PNG, BMP\n"
                                               "   • Videos: MP4, AVI, MOV, WMV, MKV, etc."
                                               )
        except Exception as e:
            print(f"Error agregando texto de ayuda: {e}")

    def clear_wallpaper_list(self):
        """Limpia completamente la lista de wallpapers"""
        try:
            import tkinter.messagebox as msgbox

            # Confirmar acción
            result = msgbox.askyesno(
                "🗑️ Limpiar Lista",
                "¿Estás seguro de que quieres eliminar TODOS los archivos de la lista?\n\n"
                "Esta acción no se puede deshacer.",
                icon="warning"
            )

            if result:
                # Limpiar configuración
                self.config_manager.set("wallpapers", [])
                self.config_manager.save_config()

                # Forzar actualización
                def force_refresh():
                    self.config_manager.load_config()
                    self.refresh_wallpaper_list()
                    print("🗑️ Lista limpiada completamente")

                self.root.after(100, force_refresh)

                msgbox.showinfo(
                    "Lista Limpiada", "✅ Se eliminaron todos los archivos de la lista.")

        except Exception as e:
            print(f"Error limpiando lista: {e}")
            messagebox.showerror("Error", f"Error limpiando lista: {e}")

    def remove_wallpaper_by_name(self, filename):
        """Elimina un wallpaper específico por nombre de archivo"""
        try:
            wallpapers = self.config_manager.get("wallpapers", [])

            # Buscar y eliminar archivo
            removed = False
            for i, wallpaper in enumerate(wallpapers):
                if os.path.basename(wallpaper) == filename:
                    wallpapers.pop(i)
                    removed = True
                    break

            if removed:
                # Guardar configuración
                self.config_manager.set("wallpapers", wallpapers)
                self.config_manager.save_config()

                # Actualizar lista
                def force_refresh():
                    self.config_manager.load_config()
                    self.refresh_wallpaper_list()
                    print(f"🗑️ Eliminado: {filename}")

                self.root.after(100, force_refresh)

                messagebox.showinfo("Archivo Eliminado",
                                    f"✅ Se eliminó: {filename}")
                return True
            else:
                messagebox.showwarning(
                    "No Encontrado", f"No se encontró el archivo: {filename}")
                return False

        except Exception as e:
            print(f"Error eliminando archivo: {e}")
            messagebox.showerror("Error", f"Error eliminando archivo: {e}")
            return False

    def handle_drop(self, event):
        """Maneja archivos soltados - FUNCIONAL"""
        try:
            # Obtener archivos
            files = event.widget.tk.splitlist(event.data)

            # Restaurar color
            event.widget.configure(bg='white')

            print(f"📁 Archivos arrastrados: {len(files)}")

            # Procesar archivos
            self.process_dropped_files(files)

        except Exception as e:
            print(f"Error procesando drop: {e}")

    def handle_drag_enter(self, event):
        """Maneja entrada de drag"""
        try:
            event.widget.configure(bg='#E8F5E8')  # Verde claro
            print("🖱️ Archivos detectados")
        except:
            pass

    def handle_drag_leave(self, event):
        """Maneja salida de drag"""
        try:
            event.widget.configure(bg='white')
        except:
            pass

    def setup_fallback_drag_drop(self):
        """Método de respaldo cuando tkinterdnd2 no funciona"""
        try:
            textbox_widget = self.wallpapers_textbox._textbox

            # Configurar eventos alternativos
            textbox_widget.bind('<Button-3>', self.show_context_menu_simple)
            textbox_widget.bind('<Double-Button-1>', self.quick_add_files)

            # Agregar texto de ayuda
            self.add_drag_drop_help_text()

            print("✅ Método de respaldo configurado")

        except Exception as e:
            print(f"Error configurando respaldo: {e}")

    def show_context_menu_simple(self, event):
        """Menú contextual simple"""
        try:
            import tkinter.messagebox as msgbox

            result = msgbox.askyesno(
                "Agregar Archivos",
                "¿Quieres abrir el selector de archivos?\n\n"
                "Nota: El drag & drop no está disponible.\n"
                "Usa este método para agregar archivos.",
                icon="question"
            )

            if result:
                self.add_wallpaper()

        except Exception as e:
            print(f"Error en menú: {e}")

    def setup_new_drag_drop(self) -> None:
        """Configura drag & drop usando el manejador corregido"""
        try:
            # Obtener el widget interno del textbox
            textbox_widget = self.wallpapers_textbox._textbox

            # Usar el manejador corregido
            self.drag_drop_handler = DragDropHandler(
                widget=textbox_widget,
                callback=self.on_files_dropped
            )

            # Configurar callback de respaldo
            if hasattr(self.drag_drop_handler, 'set_fallback_callback'):
                self.drag_drop_handler.set_fallback_callback(
                    self.add_wallpaper)

            # Agregar texto de ayuda
            self.add_drag_drop_help_text()

            print("✅ Drag & drop robusto configurado")

        except Exception as e:
            print(f"❌ Error configurando drag & drop robusto: {e}")
            # Usar método básico como respaldo
            self.setup_drag_drop_basic()

    def on_robust_drop(self, event) -> None:
        """Maneja archivos soltados (versión robusta)"""
        try:
            # Obtener archivos del evento
            files = event.widget.tk.splitlist(event.data)

            print(f"📁 Archivos recibidos via drag & drop: {len(files)}")

            # Restaurar apariencia
            try:
                event.widget.configure(bg='white')
            except:
                pass

            # Procesar archivos
            self.process_dropped_files(files)

        except Exception as e:
            print(f"❌ Error en drop robusto: {e}")

    def on_robust_drag_enter(self, event) -> None:
        """Maneja entrada de drag (versión robusta)"""
        try:
            event.widget.configure(bg='#E8F5E8')  # Verde claro
            print("🖱️ Archivos detectados sobre el área")
        except:
            pass

    def on_robust_drag_leave(self, event) -> None:
        """Maneja salida de drag (versión robusta)"""
        try:
            event.widget.configure(bg='white')
        except:
            pass

    def setup_alternative_drag_drop(self) -> None:
        """Configura método alternativo cuando tkinterdnd2 falla"""
        try:
            textbox_widget = self.wallpapers_textbox._textbox

            # Configurar eventos de mouse como alternativa
            textbox_widget.bind('<Button-3>', self.show_enhanced_context_menu)
            textbox_widget.bind('<Double-Button-1>', self.quick_add_files)
            textbox_widget.bind('<Control-Button-1>', self.show_drag_drop_help)

            print("✅ Método alternativo configurado (clic derecho, doble clic)")

        except Exception as e:
            print(f"Error configurando método alternativo: {e}")

    def show_enhanced_context_menu(self, event) -> None:
        """Muestra menú contextual mejorado"""
        try:
            import tkinter.messagebox as msgbox

            result = msgbox.askyesnocancel(
                "🖱️ Agregar Archivos",
                "Selecciona una opción:\n\n"
                "✅ SÍ: Abrir selector de archivos\n"
                "📖 NO: Ver ayuda de drag & drop\n"
                "❌ CANCELAR: Cerrar menú\n\n"
                "💡 Tip: También puedes hacer doble clic para selector rápido",
                icon="question"
            )

            if result is True:
                self.add_wallpaper()
            elif result is False:
                self.show_drag_drop_help(event)

        except Exception as e:
            print(f"Error en menú contextual: {e}")

    def show_drag_drop_help(self, event) -> None:
        """Muestra ayuda detallada de drag & drop"""
        try:
            import tkinter.messagebox as msgbox

            help_text = (
                "🖱️ GUÍA DE DRAG & DROP\n\n"
                "📋 Métodos para agregar archivos:\n\n"
                "1️⃣ DRAG & DROP (si funciona):\n"
                "   • Abre el Explorador de Windows\n"
                "   • Selecciona imágenes/videos\n"
                "   • Arrástralos a esta área\n"
                "   • Suéltalos para agregarlos\n\n"
                "2️⃣ CLIC DERECHO:\n"
                "   • Clic derecho → Selector de archivos\n\n"
                "3️⃣ DOBLE CLIC:\n"
                "   • Doble clic → Selector rápido\n\n"
                "4️⃣ BOTÓN TRADICIONAL:\n"
                "   • Usa '➕ Agregar Imagen/Video'\n\n"
                "🎬 Formatos soportados:\n"
                "• Imágenes: JPG, PNG, BMP\n"
                "• Videos: MP4, AVI, MOV, WMV, MKV"
            )

            msgbox.showinfo("Ayuda Drag & Drop", help_text)

        except Exception as e:
            print(f"Error mostrando ayuda: {e}")

    def on_files_dropped(self, files: list) -> None:
        """Maneja archivos soltados desde el nuevo manejador"""
        try:
            print(f"📁 Archivos recibidos: {len(files)}")

            # Procesar archivos usando el método existente
            self.process_dropped_files(files)

        except Exception as e:
            print(f"Error procesando archivos soltados: {e}")

    def setup_simple_drag_drop(self) -> None:
        """Configura drag & drop simple y funcional"""
        try:
            import tkinterdnd2 as tkdnd

            # Obtener el widget interno del textbox
            textbox_widget = self.wallpapers_textbox._textbox

            # Intentar configurar drag & drop de forma simple
            try:
                # Registrar para recibir archivos
                textbox_widget.drop_target_register(tkdnd.DND_FILES)

                # Configurar eventos
                textbox_widget.dnd_bind('<<Drop>>', self.on_simple_drop)
                textbox_widget.dnd_bind(
                    '<<DragEnter>>', self.on_simple_drag_enter)
                textbox_widget.dnd_bind(
                    '<<DragLeave>>', self.on_simple_drag_leave)

                print("✅ Drag & drop simple configurado")

            except Exception as e:
                print(f"⚠️ Error configurando eventos DnD: {e}")
                # Configurar solo indicadores visuales
                self.setup_visual_drag_drop()

        except ImportError:
            print("⚠️ tkinterdnd2 no disponible, usando método alternativo")
            self.setup_visual_drag_drop()

    def setup_visual_drag_drop(self) -> None:
        """Configura indicadores visuales para drag & drop"""
        try:
            # Agregar indicadores visuales y eventos básicos
            textbox_widget = self.wallpapers_textbox._textbox

            # Configurar eventos de mouse para simular drag & drop
            textbox_widget.bind('<Button-3>', self.show_context_menu)
            textbox_widget.bind('<Double-Button-1>', self.quick_add_files)

            # Agregar texto de ayuda
            self.add_drag_drop_help_text()

            print("✅ Indicadores visuales de drag & drop configurados")

        except Exception as e:
            print(f"Error configurando indicadores: {e}")

    def on_simple_drop(self, event) -> None:
        """Maneja archivos soltados (método simple)"""
        try:
            # Obtener archivos del evento
            files = event.widget.tk.splitlist(event.data)

            # Restaurar apariencia
            event.widget.configure(bg='white')

            # Procesar archivos
            self.process_dropped_files(files)

        except Exception as e:
            print(f"Error en drop simple: {e}")

    def on_simple_drag_enter(self, event) -> None:
        """Maneja entrada de drag (método simple)"""
        try:
            event.widget.configure(bg='#E8F5E8')  # Verde claro
        except:
            pass

    def on_simple_drag_leave(self, event) -> None:
        """Maneja salida de drag (método simple)"""
        try:
            event.widget.configure(bg='white')
        except:
            pass

    def show_context_menu(self, event) -> None:
        """Muestra menú contextual con opciones"""
        try:
            import tkinter.messagebox as msgbox

            result = msgbox.askyesnocancel(
                "Agregar Archivos",
                "¿Cómo quieres agregar archivos?\n\n"
                "• SÍ: Abrir selector de archivos\n"
                "• NO: Ver ayuda de drag & drop\n"
                "• CANCELAR: Cerrar este menú",
                icon="question"
            )

            if result is True:
                self.add_wallpaper()
            elif result is False:
                msgbox.showinfo(
                    "Ayuda Drag & Drop",
                    "🖱️ Para arrastrar archivos:\n\n"
                    "1. Abre el Explorador de Windows\n"
                    "2. Selecciona imágenes o videos\n"
                    "3. Arrástralos a esta área de texto\n"
                    "4. Suéltalos para agregarlos\n\n"
                    "📝 Si no funciona:\n"
                    "• Usa el botón 'Agregar Imagen/Video'\n"
                    "• Haz doble clic aquí para selector rápido"
                )

        except Exception as e:
            print(f"Error mostrando menú: {e}")

    def quick_add_files(self, event) -> None:
        """Selector rápido de archivos con doble clic"""
        try:
            self.add_wallpaper()
        except Exception as e:
            print(f"Error en selector rápido: {e}")

    def setup_windows_drag_drop(self) -> None:
        """Configura drag & drop usando Windows API"""
        try:
            import ctypes
            from ctypes import wintypes

            # Obtener el handle de la ventana del textbox
            textbox_widget = self.wallpapers_textbox._textbox
            hwnd = textbox_widget.winfo_id()

            # Configurar la ventana para aceptar archivos arrastrados
            ctypes.windll.shell32.DragAcceptFiles(hwnd, True)

            # Configurar eventos para manejar los archivos
            textbox_widget.bind('<Map>', self.on_textbox_mapped)

            # Agregar indicador visual
            self.add_drag_drop_indicator()

            print("Drag & drop configurado exitosamente")

        except Exception as e:
            print(f"Error configurando Windows drag & drop: {e}")
            raise e

    def setup_tkinterdnd2(self) -> None:
        """Configura drag & drop usando tkinterdnd2"""
        try:
            import tkinterdnd2 as tkdnd

            # Hacer que la ventana soporte DnD
            try:
                self.root.tk.call('package', 'require', 'tkdnd')
            except:
                # Si falla, intentar cargar de otra manera
                pass

            # Configurar el textbox para aceptar archivos
            textbox_widget = self.wallpapers_textbox._textbox

            # Registrar el widget para recibir drops
            textbox_widget.drop_target_register(tkdnd.DND_FILES)

            # Configurar eventos
            textbox_widget.dnd_bind('<<Drop>>', self.on_tkdnd_drop)
            textbox_widget.dnd_bind('<<DragEnter>>', self.on_tkdnd_enter)
            textbox_widget.dnd_bind('<<DragLeave>>', self.on_tkdnd_leave)

            # Agregar indicador visual
            self.add_drag_drop_indicator()

            print("✅ tkinterdnd2 configurado correctamente")

        except Exception as e:
            print(f"❌ Error con tkinterdnd2: {e}")
            raise ImportError("tkinterdnd2 no disponible")

    def setup_windows_drag_drop_simple(self) -> None:
        """Configura drag & drop usando Windows API simplificado"""
        try:
            import ctypes
            from ctypes import wintypes

            # Obtener el widget del textbox
            textbox_widget = self.wallpapers_textbox._textbox

            # Configurar para aceptar archivos arrastrados
            def configure_drop_target():
                try:
                    hwnd = textbox_widget.winfo_id()
                    ctypes.windll.shell32.DragAcceptFiles(hwnd, True)

                    # Configurar un manejador simple
                    textbox_widget.bind('<Button-3>', self.show_drop_menu)

                except Exception as e:
                    print(f"Error configurando drop target: {e}")

            # Ejecutar después de que el widget esté mapeado
            self.root.after(100, configure_drop_target)

        except Exception as e:
            print(f"Error en Windows drag & drop: {e}")
            raise e

    def show_drop_menu(self, event) -> None:
        """Muestra menú contextual para simular drag & drop"""
        try:
            import tkinter.messagebox as msgbox

            result = msgbox.askyesno(
                "Agregar Archivos",
                "¿Quieres agregar archivos de imagen o video?\n\n"
                "Nota: El drag & drop nativo no está disponible.\n"
                "Usa el botón 'Agregar Imagen/Video' en su lugar.",
                icon="question"
            )

            if result:
                self.add_wallpaper()

        except Exception as e:
            print(f"Error mostrando menú: {e}")

    def on_tkdnd_drop(self, event) -> None:
        """Maneja archivos soltados con tkinterdnd2"""
        try:
            # Obtener archivos del evento
            files = self.root.tk.splitlist(event.data)

            # Procesar archivos
            self.process_dropped_files(files)

        except Exception as e:
            print(f"Error en tkdnd drop: {e}")

    def on_tkdnd_enter(self, event) -> None:
        """Maneja entrada de drag con tkinterdnd2"""
        try:
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='#E8F5E8')  # Verde claro
        except:
            pass

    def on_tkdnd_leave(self, event) -> None:
        """Maneja salida de drag con tkinterdnd2"""
        try:
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='white')
        except:
            pass

    def setup_drag_drop_alternative(self) -> None:
        """Método alternativo para drag & drop usando tkinterdnd2"""
        try:
            import tkinterdnd2 as tkdnd

            # Convertir la ventana principal para soportar DnD
            self.root = tkdnd.Tk()

            # Configurar el textbox para aceptar archivos
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.drop_target_register(tkdnd.DND_FILES)
            textbox_widget.dnd_bind('<<Drop>>', self.on_drop_files)
            textbox_widget.dnd_bind('<<DragEnter>>', self.on_drag_enter_alt)
            textbox_widget.dnd_bind('<<DragLeave>>', self.on_drag_leave_alt)

        except ImportError:
            # Si no está disponible tkinterdnd2, usar método básico
            self.setup_drag_drop_basic()

    def on_textbox_mapped(self, event) -> None:
        """Maneja cuando el textbox se mapea en la ventana"""
        try:
            import ctypes
            from ctypes import wintypes

            # Configurar el procesamiento de mensajes de Windows para drag & drop
            textbox_widget = self.wallpapers_textbox._textbox

            # Crear un procedimiento de ventana personalizado
            def wndproc(hwnd, msg, wparam, lparam):
                WM_DROPFILES = 0x0233
                if msg == WM_DROPFILES:
                    self.handle_dropped_files(wparam)
                    return 0
                # Llamar al procedimiento original
                return ctypes.windll.user32.CallWindowProcW(
                    textbox_widget.original_wndproc, hwnd, msg, wparam, lparam
                )

            # Establecer el nuevo procedimiento
            WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p,
                                         ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p)
            new_wndproc = WNDPROC(wndproc)

            hwnd = textbox_widget.winfo_id()
            textbox_widget.original_wndproc = ctypes.windll.user32.SetWindowLongPtrW(
                hwnd, -4, new_wndproc  # GWL_WNDPROC = -4
            )

        except Exception as e:
            print(f"Error configurando procedimiento de ventana: {e}")

    def handle_dropped_files(self, hdrop) -> None:
        """Maneja archivos soltados usando Windows API"""
        try:
            import ctypes
            from ctypes import wintypes

            # Obtener número de archivos
            file_count = ctypes.windll.shell32.DragQueryFileW(
                hdrop, 0xFFFFFFFF, None, 0)

            files = []
            for i in range(file_count):
                # Obtener longitud del nombre del archivo
                length = ctypes.windll.shell32.DragQueryFileW(
                    hdrop, i, None, 0)

                # Crear buffer y obtener el nombre del archivo
                buffer = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.shell32.DragQueryFileW(
                    hdrop, i, buffer, length + 1)

                files.append(buffer.value)

            # Liberar el handle
            ctypes.windll.shell32.DragFinish(hdrop)

            # Procesar los archivos
            if files:
                self.process_dropped_files(files)

        except Exception as e:
            print(f"Error manejando archivos arrastrados: {e}")

    def setup_drag_drop_basic(self) -> None:
        """Método básico de drag & drop usando eventos de Windows"""
        try:
            # Solo agregar indicadores visuales sin eventos complejos
            self.add_drag_drop_help_text()

            # Configurar eventos visuales básicos de forma segura
            try:
                textbox_widget = self.wallpapers_textbox._textbox
                textbox_widget.bind('<Enter>', self.on_textbox_enter)
                textbox_widget.bind('<Leave>', self.on_textbox_leave)
            except:
                # Si falla la configuración de eventos, continuar sin ellos
                pass

        except Exception as e:
            print(f"No se pudo configurar drag & drop: {e}")
            # Continuar la ejecución sin drag & drop

    def add_drag_drop_indicator(self) -> None:
        """Agrega indicador visual para drag & drop"""
        # Agregar texto de ayuda al textbox cuando esté vacío
        current_text = self.wallpapers_textbox.get("1.0", tk.END).strip()
        if not current_text or current_text == "No hay imágenes o videos configurados":
            self.wallpapers_textbox.delete("1.0", tk.END)
            self.wallpapers_textbox.insert("1.0",
                                           "📋 Lista de fondos de pantalla\n\n"
                                           "💡 Puedes:\n"
                                           "   • Usar el botón '➕ Agregar Imagen/Video'\n"
                                           "   • Arrastrar archivos aquí desde el explorador\n"
                                           "   • Usar una carpeta con el modo carpeta\n\n"
                                           "🎬 Formatos soportados:\n"
                                           "   • Imágenes: JPG, PNG, BMP\n"
                                           "   • Videos: MP4, AVI, MOV, WMV, MKV, etc."
                                           )

    def add_drag_drop_help_text(self) -> None:
        """Agrega texto de ayuda para drag & drop"""
        try:
            current_text = self.wallpapers_textbox.get("1.0", tk.END)
            if not current_text.strip() or "No hay imágenes o videos configurados" in current_text:
                # Mostrar indicador completo cuando esté vacío
                self.wallpapers_textbox.delete("1.0", tk.END)
                self.wallpapers_textbox.insert("1.0",
                                               "📋 Lista de fondos de pantalla\n\n"
                                               "💡 Puedes agregar archivos de estas formas:\n"
                                               "   • Usar el botón '➕ Agregar Imagen/Video'\n"
                                               "   • Arrastrar archivos desde el Explorador de Windows\n"
                                               "   • Usar una carpeta con el modo carpeta\n\n"
                                               "🎬 Formatos soportados:\n"
                                               "   • Imágenes: JPG, PNG, BMP\n"
                                               "   • Videos: MP4, AVI, MOV, WMV, MKV, etc.\n\n"
                                               "🖱️ Para arrastrar archivos:\n"
                                               "   1. Abre el Explorador de Windows\n"
                                               "   2. Selecciona tus imágenes o videos\n"
                                               "   3. Arrástralos a esta área\n"
                                               "   4. ¡Se agregarán automáticamente!"
                                               )
            elif "Consejo:" not in current_text:
                help_text = (
                    "\n\n💡 Consejo: También puedes arrastrar archivos desde el "
                    "Explorador de Windows directamente a esta lista."
                )
                self.wallpapers_textbox.insert(tk.END, help_text)
        except Exception as e:
            print(f"Error agregando texto de ayuda: {e}")

    def on_drag_enter(self, event) -> None:
        """Maneja cuando se arrastra algo sobre el textbox"""
        try:
            # Cambiar apariencia para indicar que se puede soltar
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='#E3F2FD')  # Azul claro
            return 'copy'
        except:
            pass

    def on_drag_enter_alt(self, event) -> None:
        """Método alternativo para drag enter"""
        try:
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='#E8F5E8')  # Verde claro
        except:
            pass

    def on_drag_motion(self, event) -> None:
        """Maneja el movimiento durante el arrastre"""
        return 'copy'

    def on_drag_leave(self, event) -> None:
        """Maneja cuando se sale del área de arrastre"""
        try:
            # Restaurar apariencia normal
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='white')
        except:
            pass

    def on_drag_leave_alt(self, event) -> None:
        """Método alternativo para drag leave"""
        try:
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='white')
        except:
            pass

    def on_drop(self, event) -> None:
        """Maneja cuando se sueltan archivos"""
        try:
            # Restaurar apariencia
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='white')

            # Obtener archivos arrastrados
            files = event.data.split()
            self.process_dropped_files(files)

        except Exception as e:
            print(f"Error en drag & drop: {e}")

    def on_drop_files(self, event) -> None:
        """Maneja archivos soltados (método alternativo)"""
        try:
            # Restaurar apariencia
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(bg='white')

            # Procesar archivos
            files = self.root.tk.splitlist(event.data)
            self.process_dropped_files(files)

        except Exception as e:
            print(f"Error procesando archivos: {e}")

    def on_textbox_enter(self, event) -> None:
        """Maneja cuando el mouse entra al textbox"""
        try:
            # Cambiar cursor para indicar que se puede arrastrar
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(cursor="hand2")
        except:
            pass

    def on_textbox_leave(self, event) -> None:
        """Maneja cuando el mouse sale del textbox"""
        try:
            # Restaurar cursor normal
            textbox_widget = self.wallpapers_textbox._textbox
            textbox_widget.configure(cursor="")
        except:
            pass

    def on_textbox_click(self, event) -> None:
        """Maneja clic en textbox (método básico)"""
        pass

    def on_textbox_drag(self, event) -> None:
        """Maneja arrastre en textbox (método básico)"""
        pass

    def on_textbox_release(self, event) -> None:
        """Maneja liberación en textbox (método básico)"""
        pass

    def process_dropped_files(self, files) -> None:
        """Procesa los archivos arrastrados y soltados"""
        if not files:
            return

        # Obtener lista actual de fondos
        wallpapers = self.config_manager.get("wallpapers", [])
        added_files = []
        invalid_files = []

        # Extensiones válidas
        valid_image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        valid_video_extensions = {'.mp4', '.avi', '.mov',
                                  '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        valid_extensions = valid_image_extensions | valid_video_extensions

        for file_path in files:
            # Limpiar la ruta del archivo
            file_path = file_path.strip('{}').strip('"').strip("'")

            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Verificar extensión
                file_ext = Path(file_path).suffix.lower()

                if file_ext in valid_extensions:
                    # Agregar si no está ya en la lista
                    if file_path not in wallpapers:
                        wallpapers.append(file_path)
                        added_files.append(file_path)
                else:
                    invalid_files.append(file_path)

        # Guardar cambios si se agregaron archivos
        if added_files:
            self.config_manager.set("wallpapers", wallpapers)
            self.config_manager.save_config()
            self.refresh_wallpaper_list()

            # Mostrar mensaje de éxito
            file_count = len(added_files)
            image_count = sum(1 for f in added_files if Path(
                f).suffix.lower() in valid_image_extensions)
            video_count = file_count - image_count

            success_msg = f"✅ Se agregaron {file_count} archivo(s):\n"
            if image_count > 0:
                success_msg += f"   • {image_count} imagen(es)\n"
            if video_count > 0:
                success_msg += f"   • {video_count} video(s)\n"

            messagebox.showinfo("Archivos Agregados", success_msg)

        # Mostrar advertencia si hay archivos inválidos
        if invalid_files:
            invalid_msg = f"⚠️ Se ignoraron {len(invalid_files)} archivo(s) con formato no soportado:\n\n"
            for file in invalid_files[:5]:  # Mostrar solo los primeros 5
                invalid_msg += f"• {os.path.basename(file)}\n"

            if len(invalid_files) > 5:
                invalid_msg += f"... y {len(invalid_files) - 5} más\n"

            invalid_msg += "\n🎬 Formatos soportados:\n"
            invalid_msg += "• Imágenes: JPG, JPEG, PNG, BMP\n"
            invalid_msg += "• Videos: MP4, AVI, MOV, WMV, MKV, FLV, WEBM, M4V"

            messagebox.showwarning("Archivos No Soportados", invalid_msg)

        # Si no se agregó nada
        if not added_files and not invalid_files:
            messagebox.showinfo(
                "Sin Cambios", "Los archivos ya están en la lista o no son válidos.")
