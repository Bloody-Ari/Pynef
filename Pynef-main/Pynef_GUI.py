import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from sys import path, platform
import threading

class NozzleDesignerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nozzle Designer - FreeCAD")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Variables de entrada
        self.chamber_radius = tk.DoubleVar(value=20.0)
        self.chamber_cone_length = tk.DoubleVar(value=30.0)
        self.throat_radius = tk.DoubleVar(value=5.0)
        self.exit_cone_length = tk.DoubleVar(value=40.0)
        self.exit_radius = tk.DoubleVar(value=15.0)
        
        self.output_dir = tk.StringVar(value=str(DEFAULT_OUT_DIR))
        self.file_name = tk.StringVar(value="my_nozzle")
        self.file_type = tk.StringVar(value="stl")
        
        self.create_widgets()
        self.load_default_file()
    
    def create_widgets(self):
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de diseño
        design_frame = ttk.Frame(notebook)
        notebook.add(design_frame, text="Diseño")
        
        # Pestaña de exportación
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="Exportar")
        
        # Pestaña de estado
        status_frame = ttk.Frame(notebook)
        notebook.add(status_frame, text="Estado")
        
        self.setup_design_tab(design_frame)
        self.setup_export_tab(export_frame)
        self.setup_status_tab(status_frame)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_design_tab(self, parent):
        # Título
        title = ttk.Label(parent, text="Parámetros del Nozzle (mm)", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Frame para parámetros
        params_frame = ttk.LabelFrame(parent, text="Dimensiones", padding=10)
        params_frame.pack(fill='x', padx=20, pady=10)
        
        # Chamber Radius
        ttk.Label(params_frame, text="Radio Cámara:").grid(row=0, column=0, sticky='w', pady=2)
        chamber_entry = ttk.Entry(params_frame, textvariable=self.chamber_radius, width=10)
        chamber_entry.grid(row=0, column=1, padx=10, pady=2)
        ttk.Label(params_frame, text="mm").grid(row=0, column=2)
        
        # Chamber Cone Length
        ttk.Label(params_frame, text="Long. Cono Cámara:").grid(row=1, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.chamber_cone_length, width=10).grid(row=1, column=1, padx=10, pady=2)
        ttk.Label(params_frame, text="mm").grid(row=1, column=2)
        
        # Throat Radius
        ttk.Label(params_frame, text="Radio Garganta:").grid(row=2, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.throat_radius, width=10).grid(row=2, column=1, padx=10, pady=2)
        ttk.Label(params_frame, text="mm").grid(row=2, column=2)
        
        # Exit Cone Length
        ttk.Label(params_frame, text="Long. Cono Salida:").grid(row=3, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.exit_cone_length, width=10).grid(row=3, column=1, padx=10, pady=2)
        ttk.Label(params_frame, text="mm").grid(row=3, column=2)
        
        # Exit Radius
        ttk.Label(params_frame, text="Radio Salida:").grid(row=4, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.exit_radius, width=10).grid(row=4, column=1, padx=10, pady=2)
        ttk.Label(params_frame, text="mm").grid(row=4, column=2)
        
        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Actualizar Nozzle", 
                  command=self.update_nozzle_threaded).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cargar Archivo Predeterminado", 
                  command=self.load_default_file_threaded).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Reset Valores", 
                  command=self.reset_values).pack(side='left', padx=5)
    
    def setup_export_tab(self, parent):
        export_frame = ttk.LabelFrame(parent, text="Configuración de Exportación", padding=10)
        export_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Nombre de archivo
        ttk.Label(export_frame, text="Nombre de archivo:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(export_frame, textvariable=self.file_name, width=20).grid(row=0, column=1, padx=10, pady=5)
        
        # Tipo de archivo
        ttk.Label(export_frame, text="Formato:").grid(row=1, column=0, sticky='w', pady=5)
        file_type_combo = ttk.Combobox(export_frame, textvariable=self.file_type, values=['stl', 'obj', 'ply', 'step'], width=10)
