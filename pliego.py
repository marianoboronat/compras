
import tkinter as tk
from tkinter import ttk,filedialog, messagebox
import datetime, json
import os

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

        self.title_frame = widgets.HeadingFrame(self.frame, "Crear Pliego (CME)")

        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        # self.config = widgets.ConfigFrame(self.frame)
        self.main_frame = ttk.Frame(self.frame, padding = 10)
        self.main_frame.pack(fill ="x", anchor = "n")


        # widgets
        
        self.detalle = widgets.TagsAndEntry(self.main_frame, "Detalle",20,0, True)
        self.detalle.entry.config(width =  30)
        self.dias_entrega = widgets.TagsAndEntry(self.main_frame, "Días de Entrega(NUMEROS)",30,0)
        self.dias_entrega.entry.config(width =  7)
        self.dias_entrega_letras = widgets.TagsAndEntry(self.main_frame, "Días de Entrega(LETRAS)",40,0)
        self.tipo_de_dias = widgets.RadialButton(self.main_frame,"Días de entrega",50,0,
                                                    ["hábiles", "corridos"],"h")
        self.tipo_de_dias.label_frame.grid(columnspan=2)
        self.especificaciones_tecnicas = widgets.RadialButton(self.main_frame,"¿Especificaciones Técnicas?",60,0,
                                            ["no","si" ],"h")
        self.especificaciones_tecnicas.label_frame.grid(columnspan=2)


        self.submit_button = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10 bold",cursor = "hand2", text = "GENERAR DOCUMENTO", command=self.verify_all_entries)
        self.submit_button.pack(side ="left", padx =5)

        self.open_template = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "VER PLANTILLA",
                                command = self.abrir_plantilla)
        self.open_template.pack(side ="right", padx =5)

        self.cleaner = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "LIMPIAR",
                                command = self.limpiar)
        self.cleaner.pack(side ="right", padx =5)


    def verify_all_entries(self):
        valid = 0
        context = self.get_data()
        for data in context:
            # print(f"{context[data]}")
            if context[data] == "":
                valid += 1

        if valid > 0:
            self.info.warning(f"error se deben llenar todas las entradas")
            print("error se deben llenar todas las entradas")
        else:
            try:
                
                self.generate_file(context)
                self.info.success(f"se ingreso correctamente")
            except Exception as e:
                self.info.warning(f"hay un error: {e}")
                print(f"{e}")

    def limpiar(self):
        self.detalle.limpiar()
        self.dias_entrega.limpiar()
        self.dias_entrega_letras.limpiar()
        self.tipo_de_dias.data.set(1)
        self.especificaciones_tecnicas.data.set(1)

        self.detalle.entry.focus()
        
    def get_data(self):
        get_parameters = widgets.open_json("bd/parametros.json")
        get_parameters_data ={
                "reparticion_num": get_parameters["reparticion_num"],
                "ley": get_parameters["ley"],
                "decreto_reglamentario": get_parameters["decreto_reglamentario"],
                "reparticion_siglas": get_parameters["reparticion_siglas"],
                "reparticion": get_parameters["reparticion"],
                "art_cme":get_parameters["art_cme"]
        }
        
        self.context = {
            # "template_file":None, #nombre del archivo de la plantilla
            "numero_articulo":None,#segun el tipo de contratacion
            "ley":get_parameters["ley"],
            "anio":get_parameters["anio"],
            "anio_dos_cifras":get_parameters["anio"][2:],
            "detalle":self.detalle.get(),
            "detalle_mayuscula":self.detalle.get().upper(),
            "dias_entrega":self.dias_entrega.get(),
            "dias_entrega_letra":self.dias_entrega_letras.get(),
            "tipo_de_dias":self.get_tipo_dia(),
            "especificaciones_tecnicas":self.get_especificaciones_tecnicas(), #"B – ESPECIFICACIONES TÉCNICAS"
        }

        for parametro in get_parameters_data:
            self.context.update({parametro:get_parameters_data[parametro]})

        return self.context    

    def get_especificaciones_tecnicas(self):
        esp_tecnica = self.especificaciones_tecnicas.get()
        print(esp_tecnica)
        if esp_tecnica[0] == 2:
            return "B. Especificaciones Técnicas".upper()
        else:
            return " "


    def get_tipo_dia(self):
        tipo_dia = self.tipo_de_dias.get()
        return tipo_dia[1]

    def abrir_plantilla(self):
        os.startfile(f"templates\PLIEGO_CME.docx")
    

    def generate_file(self, context):
        try:
            document = DocxTemplate(f"templates\PLIEGO_CME.docx")
            document.render(context)
            name_path = f"{widgets.open_parameter('path_output')}"
            name_document = f"PLIEGO455CME{context['detalle']}.docx"
            document.save(f"{name_document}")
            
            os.startfile(f"{name_document}")
            
            self.info.success(f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}")
            messagebox.showinfo(message=f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}", title="Documento Creado")
        except Exception as e:
            print(e ,"ocurrio un error al intentar crear")
            # self.info.warning(f"Error: Hubo un Error al intentar crear el archivo\n{e}")



if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    
    root.mainloop()