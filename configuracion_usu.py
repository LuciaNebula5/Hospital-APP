# configuracion_usu.py - Ventana de configuracion del usuario

import tkinter as tk
from tkinter import colorchooser, messagebox
import json
import os
import sys

def obtener_ruta_base():
    """Obtiene la ruta base de la aplicacion"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

class VentanaConfiguracion:
    def __init__(self, parent, app_callback):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Configuracion")
        self.ventana.geometry("500x600")
        self.ventana.configure(bg="#F5F5F5")
        
        self.app_callback = app_callback
        self.config = self.cargar_config()
        
        self.crear_interfaz()
    
    def cargar_config(self):
        ruta_config = os.path.join(obtener_ruta_base(), "config_usuario.json")
        if os.path.exists(ruta_config):
            try:
                with open(ruta_config, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuracion por defecto
        return {
            "color_fondo": "#E8F4F8",
            "color_boton": "#FF69B4",
            "fuente": "Arial",
            "tamano_fuente": 11
        }
    
    def guardar_config(self):
        ruta_config = os.path.join(obtener_ruta_base(), "config_usuario.json")
        with open(ruta_config, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.ventana, bg="#F5F5F5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titulo
        titulo = tk.Label(
            main_frame,
            text="CONFIGURACION",
            font=("Arial", 18, "bold"),
            bg="#F5F5F5",
            fg="#333333"
        )
        titulo.pack(pady=(0, 20))
        
        # Seccion: Color de fondo
        self.crear_seccion_color(main_frame, "Color de Fondo", "color_fondo")
        
        # Seccion: Color de botones
        self.crear_seccion_color(main_frame, "Color de Botones", "color_boton")
        
        # Seccion: Fuente
        self.crear_seccion_fuente(main_frame)
        
        # Seccion: Tamano de fuente
        self.crear_seccion_tamano(main_frame)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg="#F5F5F5")
        btn_frame.pack(pady=30)
        
        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar y Aplicar",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=2,
            command=self.aplicar_config
        )
        btn_guardar.pack(side=tk.LEFT, padx=10)
        
        btn_reset = tk.Button(
            btn_frame,
            text="Restablecer",
            font=("Arial", 11, "bold"),
            bg="#FF9800",
            fg="white",
            width=15,
            height=2,
            command=self.restablecer
        )
        btn_reset.pack(side=tk.LEFT, padx=10)
        
        btn_cerrar = tk.Button(
            btn_frame,
            text="Cerrar",
            font=("Arial", 11, "bold"),
            bg="#888888",
            fg="white",
            width=15,
            height=2,
            command=self.ventana.destroy
        )
        btn_cerrar.pack(side=tk.LEFT, padx=10)
    
    def crear_seccion_color(self, parent, texto, clave):
        frame = tk.Frame(parent, bg="#FFFFFF", relief=tk.RIDGE, borderwidth=1)
        frame.pack(fill=tk.X, pady=10)
        
        label = tk.Label(
            frame,
            text=texto,
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        label.pack(side=tk.LEFT, padx=15, pady=10)
        
        color_display = tk.Label(
            frame,
            text="     ",
            bg=self.config[clave],
            relief=tk.SOLID,
            borderwidth=1,
            width=5
        )
        color_display.pack(side=tk.LEFT, padx=10)
        
        btn_elegir = tk.Button(
            frame,
            text="Elegir Color",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            command=lambda: self.elegir_color(clave, color_display)
        )
        btn_elegir.pack(side=tk.LEFT, padx=10, pady=10)
    
    def crear_seccion_fuente(self, parent):
        frame = tk.Frame(parent, bg="#FFFFFF", relief=tk.RIDGE, borderwidth=1)
        frame.pack(fill=tk.X, pady=10)
        
        label = tk.Label(
            frame,
            text="Tipo de Fuente",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        label.pack(side=tk.LEFT, padx=15, pady=10)
        
        fuentes = ["Arial", "Comic Sans MS", "Courier New", "Georgia", "Times New Roman", "Verdana"]
        self.fuente_var = tk.StringVar(value=self.config["fuente"])
        
        menu_fuente = tk.OptionMenu(frame, self.fuente_var, *fuentes)
        menu_fuente.config(font=("Arial", 10), bg="#FFFFFF", width=15)
        menu_fuente.pack(side=tk.LEFT, padx=10, pady=10)
    
    def crear_seccion_tamano(self, parent):
        frame = tk.Frame(parent, bg="#FFFFFF", relief=tk.RIDGE, borderwidth=1)
        frame.pack(fill=tk.X, pady=10)
        
        label = tk.Label(
            frame,
            text="Tamano de Fuente",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.tamano_var = tk.IntVar(value=self.config["tamano_fuente"])
        
        tamanos = [9, 10, 11, 12, 13, 14, 15]
        menu_tamano = tk.OptionMenu(frame, self.tamano_var, *tamanos)
        menu_tamano.config(font=("Arial", 10), bg="#FFFFFF", width=5)
        menu_tamano.pack(side=tk.LEFT, padx=10, pady=10)
    
    def elegir_color(self, clave, display_label):
        color = colorchooser.askcolor(initialcolor=self.config[clave])
        if color[1]:
            self.config[clave] = color[1]
            display_label.config(bg=color[1])
    
    def aplicar_config(self):
        self.config["fuente"] = self.fuente_var.get()
        self.config["tamano_fuente"] = self.tamano_var.get()
        self.guardar_config()
        
        messagebox.showinfo("Exito", "Configuracion guardada!\nLa aplicacion se reiniciara ahora")
        
        self.ventana.destroy()
        
        # Llamar callback para reiniciar la app
        if self.app_callback:
            self.app_callback()
    
    def restablecer(self):
        if messagebox.askyesno("Confirmar", "Restablecer configuracion por defecto?"):
            self.config = {
                "color_fondo": "#E8F4F8",
                "color_boton": "#FF69B4",
                "fuente": "Arial",
                "tamano_fuente": 11
            }
            self.guardar_config()
            messagebox.showinfo("Exito", "Configuracion restablecida!\nLa aplicacion se reiniciara")
            self.ventana.destroy()
            
            # Reiniciar app
            if self.app_callback:
                self.app_callback()