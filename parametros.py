import tkinter as tk
from tkinter import ttk,filedialog as fd
from tkinter.filedialog import askopenfilename
import datetime, json, os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree,  read_excel as xl
import admin_json
import dispo_ad_datos_empresas as frame_empresas
import desestimar


class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        #frames
        self.frame = tk.Frame(self.parent)
        self.frame.pack(side = "top", fill = "both", expand =1, padx=5, pady =5)

        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        self.frame_widgets = tk.Frame(self.frame, padx = 5, pady= 5)
        self.frame_widgets.pack(side = "top", fill = "x")

        self.datos_grales = tk.LabelFrame(self.frame_widgets, text ="Datos Generales", padx = 5, pady= 5)
        self.datos_grales.pack(side = "top", fill = "x")
        self.art_leyes = tk.LabelFrame(self.frame_widgets, text ="Artículos", padx = 5, pady= 5)
        self.art_leyes.pack(side = "top", fill = "x")
        self.firmantes = tk.LabelFrame(self.frame_widgets, text ="Firmantes", padx = 5, pady= 5)
        self.firmantes.pack(side = "top", fill = "x")


        # propierties        
        self.date_current = datetime.datetime.now()
        self.current_year = self.date_current.year

        # widgets
        # datos grales
        self.anio = widgets.TagsAndEntry(self.datos_grales,"Año",0,0)
        self.reparticion_nombre = widgets.TagsAndEntry(self.datos_grales,"Nombre Repartición",25,0)
        self.reparticion = widgets.TagsAndEntry(self.datos_grales,"Repartición",30,0)   
        self.reparticion_num = widgets.TagsAndEntry(self.datos_grales,"Reparticion número",40,0)


        # Articulos

        
        self.ley = widgets.TagsAndEntry(self.art_leyes,"Texto consolidado Ley N°",0,0)
        self.decreto_reglamentario = widgets.TagsAndEntry(self.art_leyes,"Decreto reglamentario",10,0)
        self.art_cme = widgets.TagsAndEntry(self.art_leyes,"Art. Contratación Menor",20,0)
        self.art_cme.entry.config(width=7)

        self.art_cdi = widgets.TagsAndEntry(self.art_leyes,"Art. Contratación Directa",30,0)
        self.art_cdi.entry.config(width=7)

        self.art_lpu = widgets.TagsAndEntry(self.art_leyes,"Art. Licitación Pública",40,0)
        self.art_lpu.entry.config(width=7)
        
        self.informatizacion_contrataciones= widgets.TagsAndEntry(self.art_leyes,"Informatización de las contrataciones",50,0)
        self.informatizacion_contrataciones.entry.config(width=7)
        
        self.art_seleccion_ofertas = widgets.TagsAndEntry(self.art_leyes,"Criterio de selección de las Ofertas",60,0)
        self.art_seleccion_ofertas.entry.config(width=7)

        
        self.art_personas_habilitadas = widgets.TagsAndEntry(self.art_leyes,"Persona Habilitadas",70,0)
        self.art_personas_habilitadas.entry.config(width=7)
        self.art_personas_no_habilitadas = widgets.TagsAndEntry(self.art_leyes,"Persona no Habilitadas",80,0)
        self.art_personas_no_habilitadas.entry.config(width=7)

        # firmantes
        self.director = widgets.TagsAndEntry(self.firmantes,"Firmante Director",0,0)
        self.gerente_operativo = widgets.TagsAndEntry(self.firmantes,"Firmante Gerente Op.",10,0)

        self.set_widget()

        # boton
        self.next_button = tk.Button(self.frame_sup,relief = "groove",font = "Calibri 10",
                                      text ="GUARDAR", cursor = "hand2", command = self.get_data)
        self.next_button.pack(side ="left", padx =5)


    def get_data(self):
        """guardar los datos cargados al json"""
        widgets.save_json(widgets.parameters_file,"anio", self.anio.get())
        widgets.save_json(widgets.parameters_file,"ley", self.ley.get())
        widgets.save_json(widgets.parameters_file,"reparticion_nombre", self.reparticion_nombre.get())
        widgets.save_json(widgets.parameters_file,"reparticion_num", self.reparticion_num.get())
        widgets.save_json(widgets.parameters_file,"decreto_reglamentario", self.decreto_reglamentario.data.get())
        widgets.save_json(widgets.parameters_file,"art_informatizacion_contrataciones", self.informatizacion_contrataciones.data.get())
        widgets.save_json(widgets.parameters_file,"reparticion_siglas", self.reparticion.get())
        widgets.save_json(widgets.parameters_file,"art_cme", self.art_cme.get())
        widgets.save_json(widgets.parameters_file,"art_cdi", self.art_cdi.get())
        widgets.save_json(widgets.parameters_file,"art_lpu", self.art_lpu.get())
        widgets.save_json(widgets.parameters_file,"art_seleccion_ofertas", self.art_seleccion_ofertas.data.get())        
        widgets.save_json(widgets.parameters_file,"art_informatizacion_contrataciones", self.informatizacion_contrataciones.data.get())   
        widgets.save_json(widgets.parameters_file,"director", self.director.data.get())
        widgets.save_json(widgets.parameters_file,"gerente_operativo", self.gerente_operativo.data.get())
        widgets.save_json(widgets.parameters_file,"art_personas_habilitadas", self.art_personas_habilitadas.get())
        widgets.save_json(widgets.parameters_file,"art_personas_no_habilitadas", self.art_personas_no_habilitadas.get())

        
        
        
        

    def set_widget(self):
        """toma los datos del json y los pone en los widgets"""
        self.anio.data.set(f"{widgets.open_parameter('anio')}")
        self.ley.data.set(f"{widgets.open_parameter('ley')}")
        
        self.reparticion_nombre.data.set(f"{widgets.open_parameter('reparticion')}")
        self.reparticion_num.data.set(f"{widgets.open_parameter('reparticion_num')}")

        self.decreto_reglamentario.data.set(f"{widgets.open_parameter('decreto_reglamentario')}")
        self.informatizacion_contrataciones.data.set(f"{widgets.open_parameter('art_informatizacion_contrataciones')}")
        self.reparticion.data.set(f"{widgets.open_parameter('reparticion_siglas')}")
        self.art_cme.data.set(f"{widgets.open_parameter('art_cme')}")
        self.art_cdi.data.set(f"{widgets.open_parameter('art_cdi')}")
        self.art_lpu.data.set(f"{widgets.open_parameter('art_lpu')}")
        self.art_seleccion_ofertas.data.set(f"{widgets.open_parameter('art_seleccion_ofertas')}")

        self.director.data.set(f"{widgets.open_parameter('director')}")
        self.gerente_operativo.data.set(f"{widgets.open_parameter('gerente_operativo')}")
        self.art_personas_habilitadas.data.set(f"{widgets.open_parameter('art_personas_habilitadas')}")
        self.art_personas_no_habilitadas.data.set(f"{widgets.open_parameter('art_personas_no_habilitadas')}")


if __name__== "__main__":
    root = tk.Tk()
    datos_basicos = Main(root)
    root.mainloop()