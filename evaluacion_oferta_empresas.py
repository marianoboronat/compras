import openpyxl
import time
import admin_json
import json
import tkinter as tk
import read_excel
import read_excel_comparacion as xl
import widgets


class Main:
    def __init__(self, parent, excel):
        # parameters        
        self.parent = parent
        self.excel_obj = excel
        
        # frames
        self.frame = tk.Frame(self.parent )
        self.frame.pack(fill="both", expand = 1)

        # En este frame se alojaran todas los frames instanciados
        self.frames_pagination= tk.Frame(self.frame )
        self.frames_pagination.pack(fill="both", expand = 1, pady = 5, padx = 5)

        # frame para los botones de anterior y siguiente
        self.header_pagination = tk.Frame(self.frames_pagination, bg = "#B6B6B6", padx = 5, pady= 5)
        self.header_pagination.pack(side = "top", fill = "x")    

        self.first_frame_button = tk.Button(self.header_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="1<<", cursor = "hand2", command = self.first_frame)
        self.first_frame_button.pack(side ="left", padx =3)
        
        self.before_button = tk.Button(self.header_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="<", cursor = "hand2", command = self.previous_frame)
        self.before_button.pack(side ="left", padx =3)
        self.next_button = tk.Button(self.header_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                    text =">", cursor = "hand2", command = self.next_frame)
        self.next_button.pack(side ="left", padx =3)

        self.last_frame_button = tk.Button(self.header_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                       text =">>", cursor = "hand2", command = self.last_frame)
        self.last_frame_button.pack(side ="left", padx =3)

        self.last_frame_button.config(text = f">>{len(self.excel_obj.lista_empresas())}" )

        # lista de frames para la paginacion
        self.lista_frames = []
        self.number_frame = 0

        self.pagination()
    
    def next_frame(self):
        """pasa al siguiente frame"""
        self.number_frame += 1
        if self.number_frame > len(self.lista_frames)-1:
            self.number_frame = len(self.lista_frames)-1
        else:
            self.hide_frames()
            try:
                print("siguiente pagina: ",self.number_frame+1)
                self.lista_frames[self.number_frame].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
            except:
                print("error en next_page")

    def previous_frame(self):
        """pasa al frame anterior"""
        self.number_frame -= 1
        if self.number_frame < 0:
            self.number_frame = 0            
        else:
            self.hide_frames()
            try:
                print("pagina anterior: ",self.number_frame+1)
                self.lista_frames[self.number_frame].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
            except:
                print("error en next_page")

    def last_frame(self):
        """ultimo frame"""
        self.hide_frames()
        self.number_frame=len(self.excel_obj.lista_empresas())-1
        self.lista_frames[self.number_frame].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)


    def first_frame(self):
        """primer frame"""
        self.hide_frames()
        self.number_frame=0
        self.lista_frames[self.number_frame].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)




    def hide_frames(self):
        """oculta todas los frames para la paginacion"""
        for f in self.lista_frames:
            f.frame.pack_forget()

    def pagination(self):
        """crea la paginacion para las empresas
        que se presentaron en esta contratacion"""
        self.empresas = self.excel_obj.lista_empresas()
        for empresa in self.empresas:
            frameEmpresa_instancia = FramesEmpresa(self.frames_pagination, empresa)
            self.lista_frames.append(frameEmpresa_instancia)

        self.hide_frames()
        self.lista_frames[0].frame.pack(fill="both", expand = 1, padx = 5,pady = 5)

class FramesEmpresa:
    def __init__(self, parent, empresa):
        # parameters        
        self.parent = parent
        self.empresa = empresa
        
        # frames
        self.frame = tk.LabelFrame(self.parent, text =self.empresa , font = "Calibri 16 bold")
        self.frame.pack(fill="both", expand = 1, padx = 5,pady = 5)

        self.frame_widgets = tk.Frame(self.frame )
        self.frame_widgets.pack(fill="x", pady = 5)

        # widgets
        # -renglones totales que se prensento la empresa
        self.renglones_totales_data = tk.StringVar()
        self.renglones_totales = tk.Label(self.frame_widgets, text ="Renglones Presentados: ", font= "Calibri 12")
        self.renglones_totales.grid(row = 0, column= 0, sticky = "e")
        self.renglones_totales_entrada = tk.Entry(self.frame_widgets,textvariable=self.renglones_totales_data, font= "Calibri 12", relief ="groove", bd = 2)
        self.renglones_totales_entrada.grid(row = 0, column= 1, sticky = "e")

        self.mejores_ofertas_data = tk.StringVar()
        self.mejores_ofertas = tk.Label(self.frame_widgets, text ="Mejores Ofertas: ", font= "Calibri 12")
        self.mejores_ofertas.grid(row = 1, column= 0, sticky = "e")
        self.mejores_ofertas_entrada = tk.Entry(self.frame_widgets,textvariable=self.renglones_totales_data, font= "Calibri 12", relief ="groove", bd = 2)
        self.mejores_ofertas_entrada.grid(row = 1, column= 1, sticky = "e")

        self.ofertas_aptas_data = tk.StringVar()
        self.ofertas_aptas = tk.Label(self.frame_widgets, text ="Ofertas Aptas: ", font= "Calibri 12")
        self.ofertas_aptas.grid(row = 2, column= 0, sticky = "e")
        self.ofertas_aptas_entrada = tk.Entry(self.frame_widgets,textvariable=self.renglones_totales_data, font= "Calibri 12", relief ="groove", bd = 2)
        self.ofertas_aptas_entrada.grid(row = 2, column= 1, sticky = "e")

        self.desestimaciones_data = tk.StringVar()
        self.desestimaciones = tk.Label(self.frame_widgets, text ="Ofertas Desestimadas: ", font= "Calibri 12")
        self.desestimaciones.grid(row = 3, column= 0, sticky = "e")
        self.desestimaciones_entrada = tk.Entry(self.frame_widgets,textvariable=self.renglones_totales_data, font= "Calibri 12", relief ="groove", bd = 2)
        self.desestimaciones_entrada.grid(row = 3, column= 1, sticky = "e")

    def set_widgets(self):
        """setea todos los datos de los widgets"""

class FilasContainer:
    def __init__(self, parent, excel, renglon):
        """genera multiples filas de ofertas de un renglon determinado"""
        # parameters
        self.parent = parent
        self.excel = excel
        self.renglon = renglon

        
        # propierties
        self.lista_filas = []
        self.count = 0

        # frames
        self.frame = tk.Frame(self.parent, bd =0, padx = 5,pady = 5)
        self.frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)

        # widgets

        self.title = widgets.HeadingFrame(self.frame, "Renglones ofertados")

    def generar_filas(self):
        """genera todas las filas de los renglones presentados"""


class FilaRenglones:
    def __init__(self, parent):
        # parameters        
        self.parent = parent
        
        # frames
        self.frame = tk.Frame(self.parent )
        self.frame.pack(fill="both", expand = 1)


excel_comparacion = "PROCESOS PARA TESTEAR/comparacion.xlsx"
excel_renglones= "PROCESOS PARA TESTEAR/renglones.xlsx"


if __name__ == "__main__":
    root = tk.Tk()
    # datos = FilaOferta(root,"empresa_1", 355787)
    excel= xl.ExcelReader(excel_comparacion, excel_renglones)
    frame = Main(root, excel)

    root.title("COMPRA-MASTER")
    root.mainloop()

