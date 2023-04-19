import tkinter as tk
from tkinter import ttk,filedialog as fd
import datetime, json

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree, data_base as db



class Exceles:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        self.frame = ttk.LabelFrame(self.parent, text = "Cargar Exceles")
        self.frame.pack(fill = "x")

        # self.excel_renglones = fd.askopenfilename()

        self.boton = tk.Button(self.frame, text ="Excel de ", command = self.select_file)
        self.boton.pack()
    
    def select_file(self):
        filetypes = (
            ('excel', '*.xlsx')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        # showinfo(
        #     title='Selected File',
        #     message=filename
        # )


        
    
    

class EmpresaFrame:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        self.frame = ttk.LabelFrame(self.parent, text = "Registrar Empresa")
        self.frame.pack(fill = "x")
        
        self.frame_info = tk.Frame(self.parent)
        self.frame_info.pack(fill = "x")

        self.info = widgets.InfoFrame(self.frame_info)

        # lista de valores
        self.values_list = {}

        self.cuit_empresa =widgets.TagsAndEntry(self.frame,"CUIT (con guiones)",5, 0)
        self.cuit_empresa.entry.bind("<Return>",lambda x: self.verificar_cuit_existente())

        self.nombre_empresa = widgets.TagsAndEntry(self.frame,"nombre de la empresa",10, 0)
        self.register = ttk.Button(self.frame, text ="Registrar empresa", cursor = "hand2", command= self.add_data)
        self.register.grid(row = 50,column = 0, columnspan=2, pady = 5, padx = 5)
        self.register.bind("<Return>",lambda x: self.add_data())
        
        self.tree_view = tree.TreeviewData(self.parent)
        self.tree_view.head({"ID":{"width":20}, "CUIT":{"width":75},"EMPRESA":{"width":250}})

    def clean(self):
        self.nombre_empresa.data.set("")
        self.cuit_empresa.data.set("")        
        self.nombre_empresa.entry.focus()

    def add_data(self):
        self.verificar_cuit_existente()
        get_empresa = self.nombre_empresa.data.get()
        get_cuit = self.cuit_empresa.data.get()
        
        if get_empresa == "" or get_cuit =="":
            print("Falta cargar datos")
            self.cuit_empresa.entry.focus()
        else:
            try:
                print("empresa registrada")
                # empresa registrada
                set_data = db.add_empresa(get_cuit, get_empresa)

                # consulta de empresa por cuit y almacenado en self.values_list
                data = db.get_empresa_from_cuit(get_cuit)
                self.values_list[str(data[0][0])] = data[0]
                self.tree_view.write_rows(list(self.values_list.values()))
                         
                
                self.cuit_empresa.entry.focus()
                self.info.success("Empresa registrada")
                self.clean()

            except Exception as e:
                """si el numero de cuit ya existe que lo agregue a la lista del treeview"""
                # print(f"Hubo un error al intentar cargar la empresa\n{e}")
                # self.cuit_empresa.entry.focus()
                if str(e) == "UNIQUE constraint failed: empresa.cuit":
                    print(db.get_empresa_from_cuit(get_cuit)[0][0], "hola")
                    # self.values_list[db.get_empresa_from_cuit(get_cuit)[]] = (db.get_empresa_from_cuit(get_cuit))
                    # self.verificar_cuit_existente()

    def verificar_cuit_existente(self):
        """es un evento que al presionar enter primero busca
        si el cuit ingresado ya existe"""
        get_cuit = self.cuit_empresa.data.get()

        if get_cuit == "":
            """si esta vacio que no ocurra nada"""
            print("se debe ingresar un numero de cuit")
        else:
            data = db.get_empresa_from_cuit(get_cuit)
            print(data)
            try:
                if str(data[0][1]) == str(get_cuit):
                    self.values_list[str(data[0][0])] = data[0]
                    print("el numero de cuit ya existe", self.values_list)
                    self.tree_view.write_rows(list(self.values_list.values()))
                    self.cuit_empresa.entry.focus()
                    
                    self.info.success(f"Empresa '{data[0][2]}' Agregada")
                    self.clean()
            except:
                self.nombre_empresa.entry.focus()
                print("cuit no existente :). registrando nueva empresa")


            


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
    ventana = Exceles(root)
    root.mainloop()