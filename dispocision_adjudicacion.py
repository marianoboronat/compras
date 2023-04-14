import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree, data_base as db


class EmpresaFrame:
    def __init__(self, parent):
        #parameters
        self.parent = parent
        self.texto =  "Registrar Empresa"

        self.frame = ttk.LabelFrame(self.parent, text = self.texto, padding=5)
        self.frame.pack(fill = "x")
        
        self.frame_info = tk.Frame(self.frame)
        self.frame_info.grid(row = 0, column = 0, sticky="we", columnspan=2)

        self.info = widgets.InfoFrame(self.frame_info)
        
        # lista de valores
        self.lista_valores = []

        self.cuit_empresa =widgets.TagsAndEntry(self.frame,"CUIT (con guiones)",5, 0)
        self.nombre_empresa = widgets.TagsAndEntry(self.frame,"nombre de la empresa",10, 0)
        self.register = ttk.Button(self.frame, text ="Registrar empresa", cursor = "hand2", command= self.add_data)
        self.register.grid(row = 50,column = 0, columnspan=2, pady = 5, padx = 5)
        self.register.bind("<Return>",lambda x: self.add_data())
        
        self.arbol_de_prueba = tree.TreeviewData(self.parent)
        self.arbol_de_prueba.head([ "CUIT","EMPRESA"])
        # self.arbol_de_prueba.write_rows([["empresa_1","cuit_1", "renglon_"], ["empresa_2", "cuit_2", "renglon_2"]])

    def clean(self):
        self.nombre_empresa.data.set("")
        self.cuit_empresa.data.set("")        
        self.nombre_empresa.entry.focus()

    def add_data(self):
        get_empresa = self.nombre_empresa.data.get()
        get_cuit = self.cuit_empresa.data.get()
        if get_empresa == "" or get_cuit =="":
            print("Falta cargar datos")
            self.cuit_empresa.entry.focus()
        else:
            try:
                print("empresa registrada")
                db.add_empresa(get_cuit, get_empresa)
                self.lista_valores.append([ get_cuit,get_empresa,""])
                self.arbol_de_prueba.write_rows(self.lista_valores)
                self.clean()
                self.cuit_empresa.entry.focus()
            except Exception as e:
                print(f"Hubo un error al intentar cargar la empresa\n{e}")
                self.cuit_empresa.entry.focus()
                if e == "UNIQUE constraint failed: empresa.cuit":
                    self.info.warning("El numero de CUIT ya existe")
                    print(str(e))
                    self.cuit_empresa.entry.focus()

class PasoUno:
    def __init__(self, parent):
        # parameters
        self.parent = parent

        # frames
        self.frame = ttk.LabelFrame(self.parent,padding=10, text ="Datos Principales" )
        self.frame.pack(fill = "both", expand=1,padx = 10, pady= 10)
        
        # widgets
        self.label_expediente = widgets.TagsAndEntry(self.frame, "Numero de expediente", 0,0)
        self.label_expediente.entry.config(width = 10)
        
        self.nombre_proceso = widgets.TagsAndEntry(self.frame, "Nombre del proceso", 10,0)
        self.nombre_proceso.entry.config(width = 32)
        
        self.numero_proceso = widgets.TagsAndEntry(self.frame, "Numero de proceso", 20,0)
        self.numero_proceso.entry.config(width = 10)
        self.monto_estimado = widgets.TagsAndEntry(self.frame, "Monto estimado\n(en numeros con puntos y coma)", 30,0)
        self.label_expediente = widgets.TagsAndEntry(self.frame, "Monto estimado(EN LETRAS)", 40,0)

        self.fecha_recepcion = widgets.FechaDividido(self.frame, "Fecha limite de Recepcion de ofertas", 50,0)
        self.fecha_recepcion.frame_main.grid(columnspan=3)
        self.fecha_recepcion.delimitador_1.config(text="de")
        self.fecha_recepcion.delimitador_2.config(text="de")

        self.cantidad_firmas = widgets.TagsAndEntry(self.frame, "Cantidad de Firmas interesadas", 60,0)
        self.cantidad_firmas.entry.config(width=5)

class PasoDos:
    def __init__(self, parent):
        # parameters
        self.parent = parent


        # frames
        self.frame = ttk.LabelFrame(self.parent,padding=10, text ="Datos Principales", width=700)
        self.frame.pack(fill = "y", padx = 10, pady= 10)

        self.sub_frame = tk.Frame(self.frame,width=700)
        self.sub_frame.pack(fill = "y")
        self.dia_apertura = widgets.FechaDividido(self.sub_frame, "Dia de apertura", 20,0)
        self.dia_apertura.frame_main.grid(columnspan=3)
        self.dia_apertura.delimitador_1.config(text="de")
        self.dia_apertura.delimitador_2.config(text="de")

        self.empresas = EmpresaFrame(self.frame)



class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        #properties
        self.pasouno = PasoDos(self.parent)
        # self.empresa_register = EmpresaFrame(self.parent)

        # self.frame = tk.Frame(self.parent)
        # self.frame.pack(fill = "both", expand=1)

if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    root.mainloop()