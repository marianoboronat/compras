import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree

class RenglonFrame:
    def __init__(self, parent):
        #parameters
        self.parent = parent
        self.texto =  "Registrar Renglon"

        self.frame = tk.LabelFrame(self.parent, text = self.texto, font ="Calibri 16 bold")
        self.frame.pack(fill = "x", padx = 5, pady =5)
        #properties
        
        # lista de valores
        self.lista_valores = []

        self.nombre_renglon = widgets.TagsAndEntry(self.frame,"nombre del renglon",0, 0)
        # self.cuit_empresa =widgets.TagsAndEntry(self.frame,"CUIT (con guiones)",10, 0)
        self.register = ttk.Button(self.frame, text ="Registrar empresa", command= self.add_data)
        self.register.grid(row = 50,column = 0, columnspan=2, pady = 5, padx = 5)
        self.register.bind("<Return>",lambda x: self.add_data())
        
        self.arbol_de_prueba = tree.TreeviewData(self.parent)
        self.arbol_de_prueba.head(["EMPRESA", "CUIT"])
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
            self.nombre_empresa.entry.focus()
        else:
            self.lista_valores.append([get_empresa,get_cuit,""])
            self.arbol_de_prueba.write_rows(self.lista_valores)
            self.clean()

class EmpresaFrame:
    def __init__(self, parent):
        #parameters
        self.parent = parent
        self.texto =  "Registrar Empresa"

        self.frame = tk.LabelFrame(self.parent, text = self.texto, font ="Calibri 16 bold")
        self.frame.pack(fill = "x", padx = 5, pady =5)
        #properties
        
        # lista de valores
        self.lista_valores = []

        self.nombre_empresa = widgets.TagsAndEntry(self.frame,"nombre de la empresa",0, 0)
        self.cuit_empresa =widgets.TagsAndEntry(self.frame,"CUIT (con guiones)",10, 0)
        self.register = ttk.Button(self.frame, text ="Registrar empresa", command= self.add_data)
        self.register.grid(row = 50,column = 0, columnspan=2, pady = 5, padx = 5)
        self.register.bind("<Return>",lambda x: self.add_data())
        
        self.arbol_de_prueba = tree.TreeviewData(self.parent)
        self.arbol_de_prueba.head(["EMPRESA", "CUIT"])
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
            self.nombre_empresa.entry.focus()
        else:
            self.lista_valores.append([get_empresa,get_cuit,""])
            self.arbol_de_prueba.write_rows(self.lista_valores)
            self.clean()
        

class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        #properties
        self.empresa_register = EmpresaFrame(self.parent)

        # self.frame = tk.Frame(self.parent)
        # self.frame.pack(fill = "both", expand=1)

        




if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    
    root.mainloop()