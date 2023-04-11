
import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets

class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        #properties
        self.date_current = datetime.datetime.now()
        self.current_year = self.date_current.year
        self.tipos_contrataciones = ["Contratacion Menor","Contratación Directa"]

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill ="both",expand = 1, anchor = "n")
        


        self.info = widgets.InfoFrame(self.frame)
        self.config = widgets.ConfigFrame(self.frame)
        self.main_frame = ttk.LabelFrame(self.frame, text ="Generar Pliego de Contratacion menor ", padding = 10)
        self.main_frame.pack(fill ="x", anchor = "n")


        # widgets
        
        self.ley = widgets.TagsAndEntryBlock(self.main_frame, "Ley (con punto)",5,0, True)
        self.ley.data.set(f"{widgets.open_parameter('ley')}")
        self.anio = widgets.TagsAndEntryBlock(self.main_frame, "Año",10,0, True)
        self.anio.data.set(self.current_year)
        self.detalle = widgets.TagsAndEntry(self.main_frame, "Detalle",20,0, True)
        self.detalle.entry.config(width =  30, font = "Arial 14")
        self.dias_entrega = widgets.TagsAndEntry(self.main_frame, "Días de Entrega(solo numeros)",30,0)
        self.dias_entrega_letras = widgets.TagsAndEntry(self.main_frame, "Días de Entrega(en letras)",40,0)
        self.tipo_de_dias = widgets.RadialButton(self.main_frame,"Tipo de Días\n(dias de entrega)",50,0,
                                                    ["hábiles", "corridos"],"h")
        self.tipo_de_dias.label_frame.grid(columnspan=2)
        self.especificaciones_tecnicas = widgets.RadialButton(self.main_frame,"¿Especificaciones Técnicas?",60,0,
                                            ["no","si" ],"h")
        self.especificaciones_tecnicas.label_frame.grid(columnspan=2)


        self.submit_button = ttk.Button(self.main_frame, text = "GENERAR PLIEGO", command=self.get_data)
        self.submit_button.grid(columnspan=3)        
        self.cleaner = ttk.Button(self.main_frame, cursor = "hand2", text = "Limpiar",
                                command = self.clean)
        self.cleaner.grid(column = 0, row = 100, columnspan = 3)

        self.context = {
            "template_file":None, #nombre del archivo de la plantilla
            "especificaciones_tecnicas":None, #"B – ESPECIFICACIONES TÉCNICAS"
            "contratacion":None,
            "contratacion_mayusc":None, 
            "codigo_contratacion":None, #ej: CME
            "numero_articulo":None,#segun el tipo de contratacion
            "ley":None,
            "anio":None,
            "anio_dos_cifras":None,
            "detalle":None,
            "detalle_mayuscula":None,
            "dias_entrega":None,
            "dias_entrega_letra":None,
            "tipo_de_dias":None
        }

    def clean(self):
        pass
    def get_data(self):        
        self.context["contratacion"] = self.get_contratacion()
        self.context["ley"] = self.ley.get()
        self.context["anio"] = self.anio.get()
        self.context["anio_dos_cifras"] = self.anio.get()[2:]
        self.context["detalle"] = self.detalle.get()
        self.context["detalle_mayuscula"] = self.detalle.get().upper()
        self.context["dias_entrega"] = self.dias_entrega.get()
        self.context["dias_entrega_letra"] = self.dias_entrega_letras.get().upper()
        self.get_contratacion()
        self.get_tipo_dia()
        self.get_especificaciones_tecnicas()
        
        self.generate_file()
    
    def get_especificaciones_tecnicas(self):
        esp_tecnica = self.especificaciones_tecnicas.get()
        if esp_tecnica == 1:
            self.context["especificaciones_tecnicas"] = ""
            
        elif esp_tecnica == 2:
            self.context["especificaciones_tecnicas"] = "B. ESPECIFICACIONES TÉCNICAS"


    def get_tipo_dia(self):
        tipo_dia = self.tipo_de_dias.get()
        print(tipo_dia)
        if tipo_dia == 1:
            self.context["tipo_de_dias"] = "hábiles"
        elif tipo_dia == 2:
            self.context["tipo_de_dias"] = "corridos"


    def get_contratacion(self):
        contratacion = self.options_contrataciones.get()
        if contratacion == 1:
            self.context["template_file"] = "PLIEGO_CME.docx"
            self.context["contratacion"] = "Contratación Menor"
            self.context["contratacion_mayusc"] = self.context["contratacion"].upper()
            self.context["codigo_contratacion"] = "CME"
            self.context["numero_articulo"] = "38"
        elif contratacion == 2:
            self.context["template_file"] = "PLIEGO_CDI.docx"
            self.context["contratacion"] = "Contratación Directa"
            self.context["contratacion_mayusc"] = self.context["contratacion"].upper()
            self.context["codigo_contratacion"] = "CDI"
            self.context["numero_articulo"] = "28"

        print(contratacion)


    def generate_file(self):
        try:
            document = DocxTemplate(f"templates/{self.context['template_file']}")
            document.render(self.context)
            document.save(f"PLIEGO{self.context['codigo_contratacion']}{self.context['detalle']}.docx")
            self.info.info("Documento creado satisfactoriamente")
        except: 
            self.info.warning("Error")



if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    
    root.mainloop()