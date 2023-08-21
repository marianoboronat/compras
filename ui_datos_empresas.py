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


class Pagination:
    def __init__(self, parent, contratacion):
        """permite la navegacion de multiples frames en uno.
        el parametro 'sub_frames_list' debe ser una lista de frames u 
        objetos con un frame como atributo cuyo nombre debe ser 'frame'
        """
        #parameters
        self.parent = parent
        self.contratacion =contratacion

        # main frame
        self.frame = tk.Frame(self.parent)
        self.frame.pack(side = "top", fill = "both", expand =1)
        
        # frame para los botones de anterior y siguiente
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        # frame para intercambiar los subframes
        self.frame_screen = tk.Frame(self.frame, padx = 5, pady= 5)
        self.frame_screen.pack(expand= 1,  fill = "both", side = "bottom")
        
        self.sub_frames_list = None
        

        
        self.before_button = tk.Button(self.frame_sup,relief = "groove",font = "Calibri 10",
                                       text ="◄ Anterior", cursor = "hand2", command = self.before_frame)
        self.before_button.pack(side ="left", padx =5)

        self.next_button = tk.Button(self.frame_sup,relief = "groove",font = "Calibri 10",
                                    text ="Siguiente ►", cursor = "hand2", command = self.next_frame)
        self.next_button.pack(side ="left", padx =5)

        self.hide_frame()
        self.numero_frame = 0

        try:
            self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
        except:
            print("There are not frames")

    def next_frame(self):
        """permite pasar al siguiente frame"""
        try:
            self.numero_frame += 1
            if self.numero_frame > len(self.sub_frames_list)-1:
                self.numero_frame =len(self.sub_frames_list)-1
            else:
                self.hide_frame()
                try:
                    self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
                except:                    
                    self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
                print("frame posterior", self.numero_frame)
        except Exception as e:
            print(e, "#59287")

    
    def before_frame(self):
        """permite pasar al frame anterior"""
        try:
            self.numero_frame -= 1
            if self.numero_frame < 0:
                self.numero_frame =0
            else:
                self.hide_frame()
                try:
                    self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
                except:
                    self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
                print("frame anterior", self.numero_frame)

        except Exception as e:
            print(e)

    def hide_frame(self):
        for frame in self.sub_frames_list:
            try:
                frame.frame.pack_forget()
            except:
                frame.pack_forget()

    def generar_lista_frames(self, numero_contratacion):
        """genera una lista de objetos 'FrameEmpresa'
        de las empresas que figuren"""
        lista_empresas = admin_json.lista_empresas(numero_contratacion)
        lista_frames = []

        if lista_empresas == None:
            print("error, verificar el numero de contratacion seleccionado")
        else:
            print(lista_empresas)
            count = 0
            for datos_empresa in lista_empresas:
                count +=1
                datos_empresa["#"] = count
                print(datos_empresa)
                frame_empresa = FrameEmpresa(self.frame_screen,datos_empresa )
                lista_frames.append(frame_empresa)
        
        self.sub_frames_list = lista_frames



class FrameEmpresa:
    def __init__(self,parent, data):
        """el parametro "datos" debe ser un diccionario con los datos:
        "nombre_empresa", "renglones_totales", "renglones_adjudicados",
        "renglones_desestimados", "monto_total"
        """
        #parametros
        self.parent = parent
        self.data = data
        #propiedades
        self.fuentes = widgets.NORMAL_FONT

        # datos
        self.nombre_empresa = f"{data['#']} - {data['empresa']}"
        self.numero_cuit = data["cuit"]
        # self.data_renglones_totales = data["renglones_totales"]
        self.data_renglones_adjudicados = f'{" - ".join(data["renglones_adjudicados"])}'
        self.data_renglones_desestimados = f'{" - ".join(data["renglones_desestimados"]["economicamente"])}'
        self.data_adjudicado = data["precio_total"]
        self.renglones_totales = len(data["renglones_adjudicados"]) + len(data["renglones_desestimados"]["economicamente"])
        
        #frames
        self.frame = tk.LabelFrame(self.frame_screen, text = self.nombre_empresa.upper(),
                                    font = "Calibri 20 bold" )
        self.frame.pack(expand=  1, fill = "both", pady = 5, padx = 5)
        

        #widgets
        self.n_cuit = widgets.TagsAndEntry(self.frame, "N° CUIT", 0,0)
        self.n_cuit.data.set(self.numero_cuit)

        self.data_renglones_totales = tk.StringVar()
        self.lb_renglones_totales = tk.Label(self.frame, text ="Renglones Totales:",font=self.fuentes )
        self.lb_renglones_totales.grid(row = 10, column=0, sticky="e")
        self.entry_renglones_totales = tk.Entry(self.frame,bd = 3,font=self.fuentes, state="disabled", textvariable=self.data_renglones_totales )
        self.entry_renglones_totales.grid(row = 15, column=0, sticky="we",padx = 5, pady = 5, columnspan=2 )
        self.data_renglones_totales.set(self.renglones_totales)

        self.data_adjudicados = tk.StringVar()
        self.lb_renglones_adjudicados = tk.Label(self.frame, text =f"Renglones Adjudicados ({len(self.data['renglones_adjudicados'])}):",font=self.fuentes )
        self.lb_renglones_adjudicados.grid(row = 20, column=0, sticky="e")
        self.entry_renglones_adjudicados = tk.Entry(self.frame, textvariable=self.data_adjudicados ,bd = 3,font=self.fuentes, state="disabled")
        self.entry_renglones_adjudicados.grid(row = 25, column=0, sticky="we",padx = 5, pady = 5, columnspan=2 )
        self.data_adjudicados.set(self.data_renglones_adjudicados)

        self.data_desestimados = tk.StringVar()
        self.lb_renglones_desestimados = tk.Label(self.frame, text =f"Renglones Desestimados ({len(data['renglones_desestimados']['economicamente'])}):",font=self.fuentes )
        self.lb_renglones_desestimados.grid(row = 30, column=0, sticky="e")
        self.entry_renglones_desestimados = tk.Entry(self.frame, textvariable=self.data_desestimados ,bd = 3,font=self.fuentes, state="disabled")
        self.entry_renglones_desestimados.grid(row = 35, column=0, sticky="we",padx = 5, pady = 5, columnspan=2 )
        self.data_desestimados.set(self.data_renglones_desestimados)


        self.monto_adjudicado = widgets.TagsAndEntry(self.frame, "Monto total adjudicado", 40,0)
        self.monto_adjudicado.data.set(data["precio_total"])
        self.monto_adjudicado.disabled()

        self.monto_adjudicado_letras = widgets.TagsAndEntry(self.frame, "en letras", 50,0)
        
        if self.data_adjudicado == 0:
            self.monto_adjudicado_letras.disabled()
        else:
            self.monto_adjudicado_letras.enable()
            

    def get_data(self):
        pass


if __name__== "__main__":
    root = tk.Tk()
    ventana = Pagination(root,"455-2243-CME21" )
    root.mainloop()