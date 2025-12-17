# ventana_consulta.py - Ventana de consulta del paciente

import tkinter as tk
from tkinter import messagebox
from config import *

class VentanaConsulta:
    def __init__(self, parent, paciente, guardar_callback):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Consulta")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg=COLOR_FONDO)
        
        self.paciente = paciente
        self.guardar_callback = guardar_callback
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg=COLOR_FONDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Titulo
        titulo = tk.Label(
            main_frame,
            text="HISTORIA CLÍNICA",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        titulo.pack(pady=(0, 15))
        
        # Informacion del paciente
        info_label = tk.Label(
            main_frame,
            text=f"Paciente: {self.paciente['nombre']} {self.paciente['apellidos']}",
            font=FUENTE_NORMAL,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        info_label.pack(pady=(0, 20))
        
        # Campo: Motivo de consulta
        self.crear_campo(main_frame, "Motivo de consulta:", "motivo", 3)
        
        # Campo: Que siente
        self.crear_campo(main_frame, "Que siente:", "sintomas", 3)
        
        # Campo: Donde le duele
        self.crear_campo(main_frame, "Donde le duele:", "dolor", 2)
        
        # Campo: Notas adicionales
        self.crear_campo(main_frame, "Notas adicionales:", "notas", 3)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=COLOR_FONDO)
        btn_frame.pack(pady=20)
        
        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            width=15,
            height=2,
            command=self.guardar
        )
        btn_guardar.pack(side=tk.LEFT, padx=10)
        
        btn_volver = tk.Button(
            btn_frame,
            text="Volver",
            font=FUENTE_BOTON,
            bg="#888888",
            fg="white",
            width=15,
            height=2,
            command=self.ventana.destroy
        )
        btn_volver.pack(side=tk.LEFT, padx=10)
    
    def crear_campo(self, parent, label_text, campo_key, altura):
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            font=FUENTE_NORMAL,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            anchor='w'
        )
        label.pack(fill=tk.X, pady=(10, 5))
        
        # Text widget
        text_widget = tk.Text(
            parent,
            height=altura,
            font=FUENTE_NORMAL,
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        text_widget.pack(fill=tk.X, pady=(0, 5))
        
        # Cargar datos existentes
        if campo_key in self.paciente:
            text_widget.insert('1.0', self.paciente[campo_key])
        
        # Guardar referencia
        setattr(self, f"text_{campo_key}", text_widget)
    
    def guardar(self):
        # Obtener valores
        self.paciente['motivo'] = self.text_motivo.get('1.0', tk.END).strip()
        self.paciente['sintomas'] = self.text_sintomas.get('1.0', tk.END).strip()
        self.paciente['dolor'] = self.text_dolor.get('1.0', tk.END).strip()
        self.paciente['notas'] = self.text_notas.get('1.0', tk.END).strip()
        
        # Llamar callback
        self.guardar_callback(self.paciente)
        
        messagebox.showinfo("Exito", "Datos guardados correctamente")
        self.ventana.destroy()