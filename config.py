# config.py - Configuracion y colores

import json
import os

def cargar_config_usuario():
    if os.path.exists("config_usuario.json"):
        try:
            with open("config_usuario.json", 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "color_fondo": "#E8F4F8",
        "color_boton": "#FF69B4",
        "fuente": "Arial",
        "tamano_fuente": 11
    }

# Cargar configuracion del usuario
CONFIG_USU = cargar_config_usuario()

# Colores
COLOR_FONDO = CONFIG_USU.get("color_fondo", "#E8F4F8")
COLOR_PANEL = "#FFFFFF"
COLOR_BOTON = CONFIG_USU.get("color_boton", "#FF69B4")
COLOR_BOTON_HOVER = "#FF1493"
COLOR_TEXTO = "#333333"
COLOR_BORDE = "#DDDDDD"

# Fuentes
FUENTE_BASE = CONFIG_USU.get("fuente", "Arial")
TAMANO_BASE = CONFIG_USU.get("tamano_fuente", 11)

FUENTE_TITULO = (FUENTE_BASE, 18, "bold")
FUENTE_TITULO_GRANDE = (FUENTE_BASE, 28, "bold")
FUENTE_NORMAL = (FUENTE_BASE, TAMANO_BASE)
FUENTE_BOTON = (FUENTE_BASE, TAMANO_BASE, "bold")

# Dimensiones
ANCHO_VENTANA = 1000
ALTO_VENTANA = 650

# Archivos
import sys

def obtener_ruta_base():
    """Obtiene la ruta base de la aplicacion, funciona en EXE y en Python"""
    if getattr(sys, 'frozen', False):
        # Si esta empaquetado como EXE
        return os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como script Python
        return os.path.dirname(os.path.abspath(__file__))

RUTA_BASE = obtener_ruta_base()
ARCHIVO_DATOS = os.path.join(RUTA_BASE, "citas.json")
CARPETA_IMAGENES = os.path.join(RUTA_BASE, "img_anatomia")