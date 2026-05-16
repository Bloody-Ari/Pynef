import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

from lib import pynef


class NozzleDesignerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nozzle Designer - FreeCAD")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # Inputs (equivalentes a py_input_example.py)
        # py_input_example pide: diametro de camara, Ac/At y Ae/At
        self.chamber_diameter = tk.DoubleVar(value=12.75)
        self.ac_at = tk.DoubleVar(value=4.5)
        self.ae_at = tk.DoubleVar(value=2.5)

        # Valores derivados (se recalculan al actualizar el nozzle)
        self.throat_radius = tk.DoubleVar(value=3.005)
        self.exit_radius = tk.DoubleVar(value=5.436)
        self.chamber_cone_length = tk.DoubleVar(value=12.576)
        self.exit_cone_length = tk.DoubleVar(value=9.072)

        self.output_dir = tk.StringVar(value=Path("~/Documents").expanduser())
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
        title = ttk.Label(
            parent,
            text="Parámetros del Nozzle (mm / relaciones)",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10)

        params_frame = ttk.LabelFrame(parent, text="Diseño", padding=10)
        params_frame.pack(fill='x', padx=20, pady=10)

        # Diámetro de cámara (mm)
        ttk.Label(params_frame, text="Diámetro cámara:").grid(row=0, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.chamber_diameter, width=12).grid(
            row=0, column=1, padx=10, pady=2
        )
        ttk.Label(params_frame, text="mm").grid(row=0, column=2)

        # Ac/At
        ttk.Label(params_frame, text="Ac/At (default: 4.5):").grid(row=1, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.ac_at, width=12).grid(
            row=1, column=1, padx=10, pady=2
        )

        # Ae/At
        ttk.Label(params_frame, text="Ae/At:").grid(row=2, column=0, sticky='w', pady=2)
        ttk.Entry(params_frame, textvariable=self.ae_at, width=12).grid(
            row=2, column=1, padx=10, pady=2
        )

        # Botones
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Actualizar Nozzle",
            command=self.update_nozzle_threaded
        ).pack(side='left', padx=5)
        ttk.Button(
            btn_frame,
            text="Cargar Archivo Predeterminado",
            command=self.load_default_file_threaded
        ).pack(side='left', padx=5)
        ttk.Button(
            btn_frame,
            text="Reset Valores",
            command=self.reset_values
        ).pack(side='left', padx=5)
    
    def setup_export_tab(self, parent):
        export_frame = ttk.LabelFrame(parent, text="Configuración de Exportación", padding=10)
        export_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Nombre de archivo
        ttk.Label(export_frame, text="Nombre de archivo:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(export_frame, textvariable=self.file_name, width=20).grid(row=0, column=1, padx=10, pady=5)
        
        # Tipo de archivo
        ttk.Label(export_frame, text="Formato:").grid(row=1, column=0, sticky='w', pady=5)
        file_type_combo = ttk.Combobox(export_frame, textvariable=self.file_type, values=['stl', '3mf'], width=10)
        file_type_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        # Directorio de salida
        ttk.Label(export_frame, text="Directorio:").grid(row=2, column=0, sticky='w', pady=5)
        dir_frame = ttk.Frame(export_frame)
        dir_frame.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        ttk.Entry(dir_frame, textvariable=self.output_dir, width=25).pack(side='left')
        ttk.Button(dir_frame, text="Explorar", command=self.browse_output_dir).pack(side='left', padx=5)
        
        # Botón exportar
        ttk.Button(export_frame, text="Exportar Nozzle", 
                  command=self.export_nozzle_threaded).grid(row=3, column=0, columnspan=2, pady=20)
    
    def setup_status_tab(self, parent):
        # Text widget para mostrar estado
        self.status_text = tk.Text(parent, height=20, width=70)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    # Métodos placeholder para evitar errores
    def update_nozzle_threaded(self):
        self.status_var.set("Actualizando nozzle...")
        threading.Thread(target=self.update_nozzle, daemon=True).start()
    
    def compute_design_params(self):
        # Mismo cálculo que py_input_example.py
        # r = diametro/2
        chamber_radius = self.chamber_diameter.get() / 2.0
        ac_at = self.ac_at.get()
        ae_at = self.ae_at.get()

        chamber_area = math.pi * (chamber_radius ** 2)
        throat_area = chamber_area / ac_at
        throat_radius = math.sqrt(throat_area / math.pi)

        exit_area = throat_area * ae_at
        exit_radius = math.sqrt(exit_area / math.pi)

        tan15 = 0.26794919243  # tan(15°)
        chamber_cone_length = (chamber_radius - throat_radius) / tan15
        exit_cone_length = (exit_radius - throat_radius) / tan15

        # Guardar derivados por si los quieres inspeccionar luego
        self.throat_radius.set(throat_radius)
        self.exit_radius.set(exit_radius)
        self.chamber_cone_length.set(chamber_cone_length)
        self.exit_cone_length.set(exit_cone_length)

        return chamber_radius, chamber_cone_length, throat_radius, exit_radius, exit_cone_length

    def update_nozzle(self):
        try:
            chamber_radius, chamber_cone_length, throat_radius, exit_radius, exit_cone_length = (
                self.compute_design_params()
            )
            pynef.updateNozzle(
                chamber_radius,
                chamber_cone_length,
                throat_radius,
                exit_radius,
                exit_cone_length,
            )
            self.root.after(0, lambda: self.status_var.set("Nozzle actualizado"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error al actualizar nozzle: {e}"))
    
    def load_default_file_threaded(self):
        threading.Thread(target=self.load_default_file, daemon=True).start()
    
    def load_default_file(self):
        # Placeholder
        pynef.openDefaultFile()
        self.root.after(0, lambda: self.status_var.set("Archivo predeterminado cargado"))
    
    def reset_values(self):
        # Valores por defecto equivalentes a los usados originalmente
        # py_input_example: chamber_diameter = 12.75 => radius = 6.375
        self.chamber_diameter.set(12.75)
        self.ac_at.set(4.5)
        # el script original no fija Ae/At; mantenemos un valor razonable
        self.ae_at.set(2.5)

        self.status_var.set("Valores reseteados")

    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
    
    def export_nozzle_threaded(self):
        self.status_var.set("Exportando...")
        threading.Thread(target=self.export_nozzle, daemon=True).start()
    
    def export_nozzle(self):
        # Placeholder
        pynef.exportNozzle(self.file_name.get(), self.file_type.get(), self.output_dir.get())
        self.root.after(0, lambda: self.status_var.set("Nozzle exportado exitosamente"))

def main():
    root = tk.Tk()
    app = NozzleDesignerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
