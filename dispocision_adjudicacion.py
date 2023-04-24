import tkinter as tk
from tkinter import ttk,filedialog as fd
import datetime, json, os

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

        self.boton = tk.Button(self.frame, text ="Excel de ", command = None)
        self.boton.pack()
    
    def abrir_excel(self):
        print("abriendo excel") 

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

        self.frame_info = tk.Frame(self.frame)
        self.frame_info.grid(column = 0 , row = 0, columnspan=3, sticky="we")

        self.info = widgets.InfoFrame(self.frame_info)

        self.info.info("")
        
        # widgets
        self.anio = widgets.TagsAndEntryBlock(self.frame, "Año", 3,0)
        self.anio.data.set(widgets.open_json("parametros.json")["parametros"]["anio"])
        self.anio.block_entry()

        self.label_expediente = widgets.TagsAndEntry(self.frame, "Numero de expediente", 5,0)
        self.label_expediente.entry.config(width = 10)
        
        self.nombre_proceso = widgets.TagsAndEntry(self.frame, "Nombre del proceso", 10,0)
        self.nombre_proceso.entry.config(width = 32)
        
        self.numero_proceso = widgets.TagsAndEntry(self.frame, "Numero de proceso", 20,0)
        self.numero_proceso.entry.config(width = 10)
        self.monto_estimado = widgets.TagsAndEntry(self.frame, "Monto estimado\n(en numeros con puntos y coma)", 30,0)
        self.monto_estimado_letras = widgets.TagsAndEntry(self.frame, "Monto estimado(EN LETRAS)", 40,0)

        self.fecha_recepcion = widgets.FechaDividido(self.frame, "Fecha limite de Recepcion de ofertas", 50,0)
        self.fecha_recepcion.frame_main.grid(columnspan=3)
        self.fecha_recepcion.delimitador_1.config(text="de")
        self.fecha_recepcion.delimitador_2.config(text="de")

        self.cantidad_firmas = widgets.TagsAndEntry(self.frame, "Cantidad de Firmas interesadas", 60,0)
        self.cantidad_firmas.entry.config(width=5)
        
        self.submit_button = ttk.Button(self.frame, text ="Agregar Proceso",cursor = "hand2", command = self.add_proceso)
        self.submit_button.grid(row = 70, column = 0, columnspan=3)

        self.cleaner_button = ttk.Button(self.frame, text ="Limpiar",cursor = "hand2", command = self.clean)
        self.cleaner_button.grid(row = 80, column = 0, columnspan=3)

    def clean(self):
        self.numero_proceso.data.set("")
        self.nombre_proceso.data.set("")
        self.label_expediente.data.set("")
        self.monto_estimado.data.set("")
        self.cantidad_firmas.data.set("")

        self.monto_estimado_letras.data.set("")
        self.fecha_recepcion.clean()

    def add_proceso(self):
        context = {
            "anio":self.anio.data.get(),
            "numero_proceso": self.numero_proceso.data.get(),
            "nombre_proceso":self.nombre_proceso.data.get(),
            "expediente":self.label_expediente.data.get(),
            "monto_sugerido":self.monto_estimado.data.get(),
            "monto_sugerido_en_letras":self.monto_estimado_letras.get(),
            "fecha_limite_dia":self.fecha_recepcion.get()[0],
            "fecha_limite_mes":self.fecha_recepcion.get()[1],
            "fecha_limite_anio":self.fecha_recepcion.get()[2],
            "cantidad_firmas_revisadas":self.cantidad_firmas.data.get()
            }
        valid = 0
        for data in context:
            print(f"{context[data]}")
            if context[data] == "":
                valid += 1

        if valid > 0:
            self.info.warning(f"error se deben llenar todas las entradas")
            print("error se deben llenar todas las entradas")
        else:
            try:
                self.info.success(f"se ingreso correctamente")
                set_data = db.add_proceso(context)
            except Exception as e:
                self.info.warning(f"hay un error: {e}")
                print(f"{e}")
            
class PasoDos:
    def __init__(self, parent):
        # parameters
        self.parent = parent


        # frames
        self.frame = ttk.LabelFrame(self.parent,padding=10, text ="Datos Principales", width=700)
        self.frame.pack(fill = "both", expand = 1, padx = 10, pady= 10)

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

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side = "top", fill = "x")
        
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        self.frame_screen = tk.Frame(self.frame, padx = 5, pady= 5)
        self.frame_screen.pack(expand= 1,  fill = "both", side = "bottom")

        self.paso_uno = PasoUno(self.frame_screen)
        self.paso_dos = PasoDos(self.frame_screen)
        self.paso_tres = Exceles(self.frame_screen)
        self.frame_list = [self.paso_uno,self.paso_dos , self.paso_tres]

        self.before_button = tk.Button(self.frame_sup, text ="◄ Anterior", cursor = "hand2", command = self.before_frame)
        self.before_button.pack(side ="left")

        self.next_button = tk.Button(self.frame_sup, text ="Siguiente ►", cursor = "hand2", command = self.next_frame)
        self.next_button.pack(side ="left")

        self.hide_frame()
        self.numero_frame = 0
        self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)


    def next_frame(self):            
        try:
            self.numero_frame += 1
            if self.numero_frame > len(self.frame_list)-1:
                self.numero_frame =len(self.frame_list)-1
            else:
                self.hide_frame()
                self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)
                print("frame posterior", self.numero_frame)
        except Exception as e:
            print(e)

    
    def before_frame(self):
        try:
            self.numero_frame -= 1
            if self.numero_frame < 0:
                self.numero_frame =0
            else:
                self.hide_frame()
                self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)
                print("frame anterior", self.numero_frame)
        except Exception as e:
            print(e)

    def hide_frame(self):
        for frame in self.frame_list:
            frame.frame.pack_forget()
            

if __name__== "__main__":
    root = tk.Tk()
    root.geometry("800x500")

    ventana = Main(root )
    root.mainloop()