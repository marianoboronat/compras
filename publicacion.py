
import tkinter as tk
from tkinter import ttk

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets


class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill = "both", expand = 1)
        self.config = widgets.ConfigFrame(self.frame)
        self.main_frame = ttk.LabelFrame(self.frame, text ="Generar Publicación", padding = 10)
        self.main_frame.pack(fill = "x", padx = 7, pady = 7)    

        self.firmante = widgets.TagsAndEntryBlock(self.main_frame, "Firmante", 0, 0)
        self.firma_rol = widgets.TagsAndEntryBlock(self.main_frame, "Firma rol", 3, 0)
        self.firmante.disabled()
        self.firma_rol.disabled()
        self.detalle = widgets.TagsAndEntry(self.main_frame, "Detalle", 5, 0)
        self.detalle.entry.config(width=35)
        self.proceso = widgets.TagsAndEntry(self.main_frame, "N° Proceso", 10, 0)
        self.anio = widgets.TagsAndEntry(self.main_frame, "Año", 20, 0)
        self.numero_expediente = widgets.TagsAndEntry(self.main_frame, "N° Expediente",30, 0)
        self.fecha_apertura = widgets.TagsAndEntry(self.main_frame, "Fecha de Apertura",40, 0)
        self.numero_disposicion = widgets.TagsAndEntry(self.main_frame, "Numero disposicion",50, 0)
        self.fecha_consulta = widgets.FechaDividido(self.main_frame, "Fecha consulta(mes en letras)",60,0)
        self.fecha_consulta.frame_main.grid(columnspan=3)
        self.fecha_inicio_vencimiento = widgets.TagsAndEntry(self.main_frame, "Fecha Inicio y Vencimiento",70,0)

        self.submit_button = ttk.Button(self.main_frame, text = "GENERAR PUBLICACION", command=self.get_data)
        self.submit_button.grid(columnspan=3)
        

        self.context = {
            "anio":None,
            "detalle":None,
            "anio_dos_cifras":None,
            "numero_expediente":None,
            "proceso":None,
            "numero_disposicion":None,            
            "fecha_apertura":None,         
            "fecha_inicio":None,
            "dia_consultas":None,
            "mes_consultas":None,
            "anio_consultas":None,
            "firmante":None,
            "firma_rol":None
        }

    def get_data(self):
        self.context["anio"]=self.anio.get(),
        self.context["detalle"] = self.detalle.get()
        self.context["anio_dos_cifras"]=self.anio.get()[2:]
        self.context["numero_expediente"]=self.numero_expediente.get()
        self.context["proceso"]=self.proceso.get()
        self.context["numero_disposicion"]=self.numero_disposicion.get()
        self.context["fecha_apertura"]=self.fecha_apertura.get()
        self.context["dia_consultas"]=self.fecha_consulta.get()[0]
        self.context["mes_consultas"]=self.fecha_consulta.get()[1].capitalize()
        self.context["anio_consultas"]=self.fecha_consulta.get()[2]
        self.context["fecha_inicio"]=self.fecha_inicio_vencimiento.get()
        self.context["firmante"]=self.firmante.get().upper()
        self.context["firma_rol"]=self.firma_rol.get().upper()
        

        print(self.context)

        self.generate_file()


    
    def generate_file(self):
        document = DocxTemplate("templates/PUBLICACION.docx")
        document.render(self.context)
        document.save(f"PUBLICACION455{self.context['proceso']}CME{self.context['anio_dos_cifras']}.docx")


if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    root.mainloop()