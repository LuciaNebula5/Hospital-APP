# main.py - Aplicacion principal Hospital

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from PIL import Image, ImageTk
from config import *
from ventana_consulta import VentanaConsulta
from configuracion_usu import VentanaConfiguracion

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital - Gestion Medica")
        self.root.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.root.configure(bg=COLOR_FONDO)
        
        self.pacientes = []
        self.citas = []
        
        self.cargar_datos()
        self.crear_interfaz()
    
    def cargar_datos(self):
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.pacientes = data.get("pacientes", [])
                    self.citas = data.get("citas", [])
            except:
                self.pacientes = []
                self.citas = []
        else:
            self.guardar_datos()
    
    def guardar_datos(self):
        data = {
            "pacientes": self.pacientes,
            "citas": self.citas
        }
        with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def crear_interfaz(self):
        # Titulo principal HOSPITAL
        titulo_principal = tk.Label(
            self.root,
            text="HOSPITAL",
            font=FUENTE_TITULO_GRANDE,
            bg=COLOR_FONDO,
            fg=COLOR_BOTON
        )
        titulo_principal.pack(pady=(15, 10))
        
        # Frame principal dividido
        container = tk.Frame(self.root, bg=COLOR_FONDO)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Imagenes medicas
        self.crear_panel_imagenes(container)
        
        # Panel derecho - Citas y pacientes
        self.crear_panel_citas(container)

    def crear_panel_imagenes(self, parent):
        panel_izq = tk.Frame(parent, bg=COLOR_PANEL, relief=tk.RIDGE, borderwidth=2)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Contenedor superior
        contenido_superior = tk.Frame(panel_izq, bg=COLOR_PANEL)
        contenido_superior.pack(fill=tk.BOTH, expand=True)
        
        # Titulo
        titulo = tk.Label(
            contenido_superior,
            text="IMÁGENES MÉDICAS",
            font=FUENTE_TITULO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        )
        titulo.pack(pady=15)
        
        # Boton ver galeria
        btn_galeria = tk.Button(
            contenido_superior,
            text="Ver Galería de Anatomía",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            width=25,
            height=2,
            command=self.abrir_galeria
        )
        btn_galeria.pack(pady=20)
        
        # Texto informativo
        info_text = tk.Label(
            contenido_superior,
            text="Aquí puedes ver imágenes\npara mostrar a tus pacientes\n en sus citas",
            font=FUENTE_NORMAL,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            justify=tk.CENTER
        )
        info_text.pack(pady=20)
        
        # Boton de configuracion en la parte inferior
        btn_config = tk.Button(
            panel_izq,
            text="Configuración",
            font=FUENTE_BOTON,
            bg="#9C27B0",
            fg="white",
            width=20,
            height=2,
            command=self.abrir_configuracion
        )
        btn_config.pack(side=tk.BOTTOM, pady=15, padx=10)
    
    def crear_panel_citas(self, parent):
        panel_der = tk.Frame(parent, bg=COLOR_PANEL, relief=tk.RIDGE, borderwidth=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Titulo
        titulo = tk.Label(
            panel_der,
            text="PACIENTES Y CITAS",
            font=FUENTE_TITULO,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        )
        titulo.pack(pady=15)
        
        # Botones de accion
        btn_frame = tk.Frame(panel_der, bg=COLOR_PANEL)
        btn_frame.pack(pady=10)
        
        btn_nuevo_pac = tk.Button(
            btn_frame,
            text="Nuevo Paciente",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            width=15,
            command=self.crear_paciente
        )
        btn_nuevo_pac.pack(side=tk.LEFT, padx=5)
        
        btn_nueva_cita = tk.Button(
            btn_frame,
            text="Nueva Cita",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            width=15,
            command=self.crear_cita
        )
        btn_nueva_cita.pack(side=tk.LEFT, padx=5)
        
        # Lista de citas
        self.lista_frame = tk.Frame(panel_der, bg=COLOR_PANEL)
        self.lista_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.actualizar_lista_citas()
    
    def actualizar_lista_citas(self):
        # Limpiar lista
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        if not self.citas:
            label_vacio = tk.Label(
                self.lista_frame,
                text="No hay citas programadas",
                font=FUENTE_NORMAL,
                bg=COLOR_PANEL,
                fg="#888888"
            )
            label_vacio.pack(pady=20)
            return
        
        # Mostrar citas
        for cita in self.citas:
            paciente = self.buscar_paciente(cita['paciente_id'])
            if paciente:
                self.crear_item_cita(cita, paciente)
    
    def crear_item_cita(self, cita, paciente):
        item_frame = tk.Frame(
            self.lista_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=1
        )
        item_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Informacion
        info_text = f"{paciente['nombre']} {paciente['apellidos']}\nHora: {cita['hora']}"
        
        btn = tk.Button(
            item_frame,
            text=info_text,
            font=FUENTE_NORMAL,
            bg="white",
            fg=COLOR_TEXTO,
            anchor='w',
            justify=tk.LEFT,
            relief=tk.FLAT,
            command=lambda: self.abrir_consulta(paciente)
        )
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Boton eliminar
        btn_eliminar = tk.Button(
            item_frame,
            text="X",
            font=FUENTE_BOTON,
            bg="#FF4444",
            fg="white",
            width=3,
            command=lambda: self.eliminar_cita(cita)
        )
        btn_eliminar.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def crear_paciente(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Paciente")
        ventana.geometry("400x280")
        ventana.configure(bg=COLOR_FONDO)
        
        # Nombre
        tk.Label(ventana, text="Nombre:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack(pady=5)
        entry_nombre = tk.Entry(ventana, font=FUENTE_NORMAL, width=30)
        entry_nombre.pack(pady=5)
        
        # Apellidos
        tk.Label(ventana, text="Apellidos:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack(pady=5)
        entry_apellidos = tk.Entry(ventana, font=FUENTE_NORMAL, width=30)
        entry_apellidos.pack(pady=5)
        
        # Edad
        tk.Label(ventana, text="Edad:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack(pady=5)
        entry_edad = tk.Entry(ventana, font=FUENTE_NORMAL, width=30)
        entry_edad.pack(pady=5)
        
        def guardar():
            nombre = entry_nombre.get().strip()
            apellidos = entry_apellidos.get().strip()
            edad = entry_edad.get().strip()
            
            if not nombre or not apellidos:
                messagebox.showerror("Error", "Nombre y apellidos son obligatorios")
                return
            
            paciente = {
                "id": len(self.pacientes) + 1,
                "nombre": nombre,
                "apellidos": apellidos,
                "edad": edad,
                "motivo": "",
                "sintomas": "",
                "dolor": "",
                "notas": ""
            }
            
            self.pacientes.append(paciente)
            self.guardar_datos()
            ventana.destroy()
        
        btn_guardar = tk.Button(
            ventana,
            text="Guardar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            width=15,
            command=guardar
        )
        btn_guardar.pack(pady=20)
    
    def crear_cita(self):
        if not self.pacientes:
            messagebox.showwarning("Aviso", "Primero crea un paciente")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Nueva Cita")
        ventana.geometry("400x250")
        ventana.configure(bg=COLOR_FONDO)
        
        # Seleccionar paciente
        tk.Label(ventana, text="Selecciona paciente:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack(pady=10)
        
        paciente_var = tk.StringVar()
        paciente_options = [f"{p['id']} - {p['nombre']} {p['apellidos']}" for p in self.pacientes]
        
        paciente_menu = tk.OptionMenu(ventana, paciente_var, *paciente_options)
        paciente_menu.config(font=FUENTE_NORMAL, width=30)
        paciente_menu.pack(pady=5)
        
        # Hora
        tk.Label(ventana, text="Hora (ej: 10:30):", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack(pady=10)
        entry_hora = tk.Entry(ventana, font=FUENTE_NORMAL, width=30)
        entry_hora.pack(pady=5)
        
        def guardar():
            seleccion = paciente_var.get()
            hora = entry_hora.get().strip()
            
            if not seleccion or not hora:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            paciente_id = int(seleccion.split(" - ")[0])
            
            cita = {
                "id": len(self.citas) + 1,
                "paciente_id": paciente_id,
                "hora": hora
            }
            
            self.citas.append(cita)
            self.guardar_datos()
            self.actualizar_lista_citas()
            #messagebox.showinfo("Exito", "Cita creada correctamente")
            ventana.destroy()
        
        btn_guardar = tk.Button(
            ventana,
            text="Guardar",
            font=FUENTE_BOTON,
            bg=COLOR_BOTON,
            fg="white",
            width=15,
            command=guardar
        )
        btn_guardar.pack(pady=20)
    
    def abrir_consulta(self, paciente):
        VentanaConsulta(self.root, paciente, self.guardar_paciente)
    
    def guardar_paciente(self, paciente_actualizado):
        for i, p in enumerate(self.pacientes):
            if p['id'] == paciente_actualizado['id']:
                self.pacientes[i] = paciente_actualizado
                break
        self.guardar_datos()
    
    def eliminar_cita(self, cita):
        if messagebox.askyesno("Confirmar", "Eliminar esta cita?"):
            self.citas = [c for c in self.citas if c['id'] != cita['id']]
            self.guardar_datos()
            self.actualizar_lista_citas()
    
    def buscar_paciente(self, paciente_id):
        for p in self.pacientes:
            if p['id'] == paciente_id:
                return p
        return None
    
    def abrir_galeria(self):
        if not os.path.exists(CARPETA_IMAGENES):
            os.makedirs(CARPETA_IMAGENES)
            messagebox.showinfo("Info", "Coloca imagenes en la carpeta 'img_anatomia'")
            return
        
        imagenes = [f for f in os.listdir(CARPETA_IMAGENES) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not imagenes:
            messagebox.showinfo("Info", "No hay imagenes en la carpeta 'img_anatomia'")
            return
        
        # Ventana galeria
        ventana = tk.Toplevel(self.root)
        ventana.title("Galeria de Anatomia")
        ventana.geometry("615x600")
        ventana.configure(bg=COLOR_FONDO)
        
        # Frame con scroll
        canvas = tk.Canvas(ventana, bg=COLOR_FONDO)
        scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=COLOR_FONDO)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar imagenes
        for img_name in imagenes:
            try:
                img_path = os.path.join(CARPETA_IMAGENES, img_name)
                img = Image.open(img_path)
                img.thumbnail((600, 400))
                photo = ImageTk.PhotoImage(img)
                
                label_img = tk.Label(frame_scroll, image=photo, bg=COLOR_FONDO)
                label_img.image = photo
                label_img.pack(pady=10)
                
                label_nombre = tk.Label(
                    frame_scroll,
                    text=img_name,
                    font=FUENTE_NORMAL,
                    bg=COLOR_FONDO
                )
                label_nombre.pack(pady=5)
            except:
                pass
    
    def abrir_configuracion(self):
        VentanaConfiguracion(self.root, self.reiniciar_app)
    
    def reiniciar_app(self):
        # Cerrar ventana actual
        self.root.destroy()
        
        # Crear nueva ventana con la configuracion actualizada
        import importlib
        import config
        importlib.reload(config)
        
        nueva_root = tk.Tk()
        nueva_app = HospitalApp(nueva_root)
        nueva_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()