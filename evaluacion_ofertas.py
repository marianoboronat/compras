import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json
import os, getpass as gt
import widgets

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate 
import read_excel
import read_excel_comparacion as xl
import comparador_windows as cw
#este modulo compara las ofertas presentadas por las empresas.


excel_comparacion = "PROCESOS PARA TESTEAR/comparacion.xlsx"
excel_renglones= "PROCESOS PARA TESTEAR/renglones.xlsx"

class Main:
    def __init__(self, master):
        # parameters
        self.master =master
        
        # frames
        self.frame = tk.Frame(self.master )
        self.frame.pack(fill="both", expand = 1)

        #frame path
        self.path_frame = tk.LabelFrame(self.frame, text ="Exceles", padx = 5, pady= 5)
        self.path_frame.pack(fill = "x", padx = 5, pady= 5)

        self.excel_ofertas = widgets.SelectorFile(self.path_frame, "Excel Comparativo", 0,0)
        self.excel_renglones = widgets.SelectorFile(self.path_frame, "Excel Renglones", 1,0)

        # frame para los botones de anterior y siguiente
        
        self.frame_pagination = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_pagination.pack(side = "top", fill = "x")        

        self.excel = None

        # lista de frames , para la paginacion
        self.lista_frames_renglones = []
        self.page = 0


        # botones de la paginacion

        self.comparar = tk.Button(self.frame_pagination,relief = "groove",width= 10,font = "Calibri 10 bold",
                                       text ="COMPARAR", cursor = "hand2", command = self.leer_excel)
        self.comparar.pack(side ="right", padx =3)

       

        self.first_frame_button = tk.Button(self.frame_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="1<<", cursor = "hand2", command = self.first_page)
        self.first_frame_button.pack(side ="left", padx =3)
        
        self.before_button = tk.Button(self.frame_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="<", cursor = "hand2", command = self.previous_page)
        self.before_button.pack(side ="left", padx =3)

        self.data_pagina = tk.StringVar()        
        self.data_pagina.set("1")     
        self.pagina = ttk.Entry(self.frame_pagination,width= 5,font = "calibri 14", textvariable=self.data_pagina)
        self.pagina.pack(side ="left", padx =3)
        self.pagina.bind("<Return>", self.seleccionar_pagina)
        self.pagina.bind("<Up>", lambda x: self.next_page())
        self.pagina.bind("<Down>", lambda x: self.previous_page())
        self.pagina.bind("<Control-Up>", lambda x: self.last_page())
        self.pagina.bind("<Control-Down>", lambda x: self.first_page())

        self.next_button = tk.Button(self.frame_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                    text =">", cursor = "hand2", command = self.next_page)
        self.next_button.pack(side ="left", padx =3)

        self.last_frame_button = tk.Button(self.frame_pagination,relief = "groove",width= 5,font = "Calibri 12",
                                       text =">>", cursor = "hand2", command = self.last_page)
        self.last_frame_button.pack(side ="left", padx =3)
        
        self.count = 0 
    def seleccionar_pagina(self, e):
        try:
            numero_pagina = int(self.data_pagina.get())
            if numero_pagina > len(self.lista_frames_renglones):            
                self.hide_frame()
                self.page = len(self.lista_frames_renglones)
                self.data_pagina.set(self.page)            
                self.lista_frames_renglones[self.page-1].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
            elif numero_pagina < 1:                 
                self.hide_frame()            
                self.page = 0            
                self.data_pagina.set("1")            
                self.lista_frames_renglones[self.page].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
            else:            
                self.page = numero_pagina-1
                self.hide_frame()
                self.lista_frames_renglones[self.page].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
        except:
            print("Ingrese un valor válido.")                             
            self.hide_frame()    
            self.page = 0
            self.data_pagina.set(1)    
            self.lista_frames_renglones[self.page].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
    
    def generar_frame_contratacion(self):
        """genera un frame para ver los datos principales de la contratacion"""


    def leer_excel(self):
        """lee los exceles"""
        ofertas = self.excel_ofertas.get()
        renglones = self.excel_renglones.get()

        # crea el objeto ExcelReader para leer los datos de los exceles cargados
        self.excel = xl.ExcelReader(ofertas, renglones)
        self.generar_multiples_frames()

    
    def next_page(self):
        """esto va a la pagina siguiente"""
        self.page += 1
        self.data_pagina.set(self.page)
        if self.page > len(self.lista_frames_renglones)-1:
            self.page = len(self.lista_frames_renglones)-1
        else:
            self.hide_frame()
            try:
                print("siguiente pagina: ",self.page+1)
                self.lista_frames_renglones[self.page].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
            except:
                print("error en next_page")

    def previous_page(self):        
        """esto va a la pagina siguiente"""
        self.page -= 1
        self.data_pagina.set(self.page)
        if self.page < 0:
            self.page = 0            
            self.data_pagina.set(self.page+1)
        else:
            self.hide_frame()
            try:
                print("pagina anterior: ",self.page+1)
                self.lista_frames_renglones[self.page].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)
            except:
                print("error en next_page")

    def first_page(self):
        """dirige a la primera pagina"""
        self.page = 0
        self.hide_frame()
        self.lista_frames_renglones[0].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)

    def last_page(self):
        """dirige a la ultima pagina"""
        self.page = len(self.lista_frames_renglones)-1
        self.hide_frame()
        self.lista_frames_renglones[-1].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)

    def hide_frame(self):
        """oculta todos los frames, instancias y almacenados en la
        lista 'self.lista_frames_renglones' para la paginacion"""
        
        self.data_pagina.set(self.page+1)
        for frame in self.lista_frames_renglones:
            frame.frame.pack_forget()

    def generar_multiples_frames(self):



        self.count += 1
        if self.count == 1:
            try:
                contratacion = DatosContratacion(self.frame, self.excel)
            except:
                print("error al crear la contratacion")
                
            renglones = self.excel.renglones_pedidos()
            for renglon in renglones:
                # print(renglon)
                frame_renglon = FrameRenglon(self.frame, self.excel)
                frame_renglon.set_widgets(renglon[0], self.excel)

                self.lista_frames_renglones.append(frame_renglon)

            # mostrar solo la primera pagina
            self.last_frame_button.config(text = f">>{len(self.lista_frames_renglones)}")
            self.hide_frame()
            self.lista_frames_renglones[0].frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)


class DatosContratacion:
    def __init__(self, parent, excel):
        """datos de la contratacion"""
        # parameters
        self.parent = parent
        self.excel = excel

        self.frame = tk.LabelFrame(self.parent, text ="Datos de la Contratación", pady = 5, padx = 5)
        self.frame.pack(fill ="x", padx = 5, pady = 5)

        self.contratacion = widgets.TagsAndEntry(self.frame,"Contratacion",0,0)
        self.contratacion.entry.config(state = "disabled")


        
        self.precio_estimado = widgets.TagsAndEntry(self.frame, "Precio Estimado T.", 0,2)
        self.precio_estimado.entry.config(state = "disabled")

        self.detalle = widgets.TagsAndEntry(self.frame, "Detalle", 1,0)
        self.detalle.entry.grid(columnspan = 99)
        self.detalle.entry.config(state = "disabled", width=60)
        
        self.cantidad_desiertos = widgets.TagsAndEntry(self.frame, "Desiertos",2,0 )   
        self.btn_desiertos = tk.Button(self.frame,
                                        text ="desiertos",
                                        cursor = "hand2",
                                        command=self.list_desiertos)
        self.btn_desiertos.grid(row = 2,column = 2, sticky = "w",padx = 5)      

        self.fracasado_widget = widgets.TagsAndEntry(self.frame, "Fracasados",2,3 )
        self.btn_fracaso = tk.Button(self.frame,
                                    text ="fracasados",
                                    cursor = "hand2",
                                    command=self.list_fracasados)
        self.btn_fracaso.grid(row = 2,column = 5, sticky = "w",padx = 5)      
        
        self.set_wigets()

    def list_desiertos(self):
        """permite abrir una ventana emergente para los desiertos"""
        sub_window = tk.Toplevel()
        sub_window.resizable(0,1)
        sub_window.title("Parametros Generales")
        sub_window.grab_set()

        desiertos = self.excel.desiertos()
        print(desiertos)
        cw.TreeDescription(sub_window,["Desiertos"],desiertos)    
    
    def list_fracasados(self):
        """permite abrir una ventana emergente para los fracasados"""
        sub_window = tk.Toplevel()
        sub_window.resizable(0,1)
        sub_window.title("Parametros Generales")
        sub_window.grab_set()

        fracasados = self.excel.renglones_fracasados()
        print(fracasados)
        cw.TreeDescription(sub_window,["Desiertos"],fracasados)

    def set_wigets(self):
        datos = self.excel.datos_contratacion()
        self.contratacion.data.set(datos[0])
        self.detalle.data.set(datos[1])
        self.precio_estimado.data.set(f"${datos[2].split(' ')[1]}")

        desiertos = self.excel.desiertos()
        self.cantidad_desiertos.entry.config(state = "disabled")
        self.cantidad_desiertos.label.config(text = f"Desiertos ({len(desiertos)}): ")
        self.cantidad_desiertos.data.set(desiertos)

        
        fracasados = self.excel.renglones_fracasados()
        cant_fracasados = len(fracasados)

        self.fracasado_widget.data.set(fracasados)
        self.fracasado_widget.entry.config(state = "disabled")
        self.fracasado_widget.label.config(text = f"Fracasados ({cant_fracasados}): ")


class FrameRenglon:
    def __init__(self, parent, excel):
        # parameters
        self.parent = parent
        self.excel = excel
        
        # propierties
        self.FONT_BOLD = "Calibri 14 bold"
        # frames
        self.frame = tk.LabelFrame(self.parent, text =f"Renglón", font = "Calibri 16 bold", padx =5, pady = 5)
        self.frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)

        self.frame_dato = tk.Frame(self.frame,  padx = 5, pady= 5)
        self.frame_dato.pack(fill ="x", padx = 5,pady = 5)

        self.frame_container = tk.Frame(self.frame)
        self.frame_container.pack(fill ="both", expand=1)

        # widgets
        # se cargan los datos basicos del renglon

        self.data_descripcion = tk.StringVar()
        
        self.descripcion_lbl = tk.Label(self.frame_dato,text ="Descripción:", font= "Calibri 12",)
        self.descripcion_lbl.grid(row= 0, column = 0,sticky="e", padx = 5, pady = 2)
        self.entry_descripcion_renglon = ttk.Entry(self.frame_dato,state = "disabled",width=80, textvariable=self.data_descripcion, font= "Calibri 12")
        self.entry_descripcion_renglon.grid(row= 0, column = 1,columnspan= 5,sticky="w")

        self.btn_descripcion_renglon = tk.Button(self.frame_dato,
                                                bd = 4,
                                                cursor="hand2",
                                                relief="groove",
                                                text ="Description",
                                                command=self.window_description)
        self.btn_descripcion_renglon.grid(row= 0, column = 6,sticky="w", padx =5)

        self.lbl_precio_estimado = tk.Label(self.frame_dato,text ="Precio Est.", font= "Calibri 12")
        self.lbl_precio_estimado.grid(row= 10, column = 0,sticky="e", padx = 5, pady = 2)
        self.precio_estimado = tk.Label(self.frame_dato,width=20,text ="", font= "Calibri 12",
                                        bd = 2,relief = "groove")
        self.precio_estimado.grid(row= 10, column = 1, sticky="w")


        self.lbl_precio_20_porciento = tk.Label(self.frame_dato,text ="Precio Est. + 20%", font= "Calibri 12")
        self.lbl_precio_20_porciento.grid(row= 10, column = 2,sticky="e", padx = 5, pady = 2)
        self.precio_20_porciento = tk.Label(self.frame_dato,width=20,text ="", font= "Calibri 12",
                                        bd = 2,relief = "groove")
        self.precio_20_porciento.grid(row= 10, column = 3, sticky="w")    

        self.lbl_tipo_partida = tk.Label(self.frame_dato,text ="Partida", font= "Calibri 12")
        self.lbl_tipo_partida.grid(row= 10, column = 4,sticky="e", padx = 5, pady = 2)
        self.numero_tipo_partida = tk.Label(self.frame_dato,width=20,text ="", font= "Calibri 12",
                                        bd = 2,relief = "groove")
        self.numero_tipo_partida.grid(row= 10, column = 5, sticky="w")  

        # self.precio_20_porciento = widgets.TagsAndEntry(self.frame_dato, "Precio est. + 20% $",10,0)

        self.container = None
    
    def set_widgets(self,numero_renglon,excel):
        """setatea los datos al los widgets"""
        precio_estimado = excel.ofertas_x_renglon(numero_renglon)[f'{numero_renglon}']['precio_estimado']
        txt_descripcion = excel.renglones_pedidos()[numero_renglon-1][3]
        tipo_partida = excel.renglones_pedidos()[numero_renglon-1][1]

        self.data_descripcion.set(f"{txt_descripcion}")
        self.frame.config(text=f"Renglon N°{numero_renglon}")
        self.precio_estimado.config(text=f"$ {precio_estimado}")
        self.precio_20_porciento.config(text= "$ %.2f" %  (precio_estimado + precio_estimado*20/100))
        self.numero_tipo_partida.config(text= tipo_partida)
        self.generar_container(excel,numero_renglon)


    def generar_container(self,excel, numero_renglon):
        self.container = FilasContainer(self.frame_container,excel,numero_renglon)
        self.container.generar_filas()

    def window_description(self):
        """window extra"""
        sub_window = tk.Toplevel()
        sub_window.resizable(0,0)
        sub_window.title("Parametros Generales")
        sub_window.grab_set()

        cw.WindowDescription(sub_window,self.data_descripcion.get())
        
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
        self.frame = tk.Frame(self.parent, bd =0,)
        self.frame.pack(fill ="both", expand= 1, padx = 5,pady = 5)


        self.scrollbar = widgets.Scrollbar(self.frame)
        # widgets

        self.title = widgets.HeadingFrame(self.frame, "Ofertas")
        self.filas_header = FilaOfertaHeader(self.frame)

    def generar_filas(self):        
        if self.count == 0:
            renglones = self.excel.renglones_pedidos()
            ofertas = list(self.excel.ofertas_x_renglon(self.renglon).values())[0]["ofertas"]
            if len(ofertas)>0:
                precio_estimado = [x[5] for x in renglones if x[0]==self.renglon][0]
                # print("renglon: ", self.renglon, "precio estimado: ",precio_estimado)
                # print("ofertas",ofertas)
                counter= 0
                for oferta in ofertas:
                    counter+=1
                    instancia = FilaOferta(self.frame,self.renglon,oferta,precio_estimado)                    
                    if counter ==1 and instancia.porcentaje < 20:
                        instancia.mejor_oferta()
                # print(ofertas)
                self.count +=1
            else:
                tk.Label(self.frame, text = "Renglón desierto.",font=("Calibri 12 bold"),fg ="white",bg ="grey" ).pack(fill = "x")
        else:
            print("filas ya generadas")

class FilaOfertaHeader:
    def __init__(self, parent):        
        # parameters
        self.parent = parent
        
        # propierties
        self.FONT = "Calibri 12"
        self.FONT_BOLD = "Calibri 12 bold"
        
        # frames
        self.frame = tk.Frame(self.parent, pady = 3, cursor="hand2")
        self.frame.pack(fill = "x", anchor="center")
        
        # widgets
        self.expand = tk.Label(self.frame, text =" ", font = self.FONT_BOLD)
        self.expand.grid(row = 0, column =0, sticky="we" , padx =5)

        self.recomendacion = tk.Label(self.frame, text ="RECOMEN-\nDACIÓN", width=20, font = self.FONT_BOLD)
        self.recomendacion.grid(row = 0, column = 10, sticky="we")

        self.opcion = tk.Label(self.frame, text =f"OPCION", width=10, font = self.FONT_BOLD)
        self.opcion.grid(row = 0, column = 20, sticky="we")

        self.empresa = tk.Label(self.frame, text ="EMPRESA", width=50, font = self.FONT_BOLD)
        self.empresa.grid(row = 0, column = 30, sticky="we")

        self.precio_ofertado = tk.Label(self.frame, text ="PRECIO\nUNITARIO", width=15, font = self.FONT_BOLD)
        self.precio_ofertado.grid(row = 0, column = 40, sticky="we")

        self.porcentaje_excedido = tk.Label(self.frame, text ="%\nEXCEDIDO", width=10, font = self.FONT_BOLD)
        self.porcentaje_excedido.grid(row = 0, column = 50, sticky="we")

class FilaOferta:
    def __init__(self, parent,renglon, datos, precio_estimado):
        # parameters
        self.parent = parent
        self.renglon = renglon
        self.datos = datos # el parametro datos debe ser un diccionario
        self.precio_estimado =  float(precio_estimado)

        # propierties
        self.FONT = "Calibri 12"
        self.FONT_BOLD = "Calibri 12 bold"

        self.porcentaje = (100 * float(self.datos[1]) / float(self.precio_estimado))-100

        #colores
        self.bg_color_leave = "#f0f0f0"
        self.fg_color_leave = "black"
        
        self.bg_color_enter = "#A8E1C9"
        self.fg_color_enter = "black"

        
        # frames
        self.frame = tk.Frame(self.parent, pady = 3, cursor="hand2", bd= 2,relief="groove",bg =self.bg_color_leave)
        self.frame.pack(fill = "x", anchor="center",pady = 5)
        self.frame.bind("<Enter>",self.enter_frame)
        self.frame.bind("<Leave>",self.leave_frame)


        self.sub_frame_main = tk.Frame(self.frame, pady = 3, cursor="hand2",bg =self.bg_color_leave)
        self.sub_frame_main.pack(fill = "x" )

        self.sub_frame_description = tk.LabelFrame(self.frame,text ="Especificación Técnica",bg=self.bg_color_leave, pady = 3, cursor="hand2", bd= 2,relief="groove")
        self.sub_frame_description.pack(fill = "x",padx = 5, pady=5 )

        self.descripcion_texto = widgets.TextArea(self.sub_frame_description,"Descripción" ,3)
        self.descripcion_texto.label.destroy()
        self.descripcion_texto.set_(self.datos[4])
        
        # widgets
        self.expand_count = 1
        self.expand = ttk.Button(self.sub_frame_main, text ="+", width=3, command = self.expand_button)
        self.expand.grid(row = 0, column =0, padx = 5)

        self.recomendacion = tk.Label(self.sub_frame_main, text ="Apto", width=20,bg =self.bg_color_leave)
        self.recomendacion.grid(row = 0, column = 10)

        self.opcion = tk.Label(self.sub_frame_main, text =f"{self.datos[-2]}",bg =self.bg_color_leave, width=10)
        self.opcion.grid(row = 0, column = 20)


        self.data_empresa = tk.StringVar()
        self.data_empresa.set(f"{self.datos[-1]}")
        self.empresa = tk.Entry(self.sub_frame_main, textvariable= self.data_empresa,bg =self.bg_color_leave,state = "disable",bd= 0, width=50, font = self.FONT)
        self.empresa.grid(row = 0, column = 30, sticky="w")

        self.precio_ofertado = tk.Label(self.sub_frame_main, text =f"$ {read_excel.agregar_comas_precio(self.datos[1])}",bg =self.bg_color_leave, width=15, font = self.FONT)
        self.precio_ofertado.grid(row = 0, column = 40, sticky="e")

        self.porcentaje_excedido = tk.Label(self.sub_frame_main, text =f"{self.porcentaje:.1f}",bg =self.bg_color_leave, width=10, font = self.FONT)
        self.porcentaje_excedido.grid(row = 0, column = 50, sticky="e")
        
        # self.calcular_porcentaje()
        self.oferta_desestimada()
        self.leave_frame("")
        self.expand_button()


    # eventos
    def enter_frame(self,e):
        self.sub_frame_description.config(bg=self.bg_color_enter)
        self.sub_frame_main.config(bg = self.bg_color_enter)
        self.frame.config(bg = self.bg_color_enter)
        self.recomendacion.config(bg = self.bg_color_enter,fg = self.fg_color_enter)
        self.opcion.config(bg = self.bg_color_enter,fg = self.fg_color_enter)
        self.empresa.config(bg = self.bg_color_enter,fg = self.fg_color_enter)
        self.porcentaje_excedido.config(bg = self.bg_color_enter,fg = self.fg_color_enter)
        self.precio_ofertado.config(bg = self.bg_color_enter,fg = self.fg_color_enter)

    def leave_frame(self,e):
        self.sub_frame_description.config(bg=self.bg_color_leave)
        self.sub_frame_main.config(bg = self.bg_color_leave)
        self.frame.config(bg = self.bg_color_leave)
        self.recomendacion.config(bg = self.bg_color_leave, fg = self.fg_color_leave)
        self.opcion.config(bg = self.bg_color_leave, fg = self.fg_color_leave)
        self.empresa.config(bg = self.bg_color_leave, fg = self.fg_color_leave)
        self.porcentaje_excedido.config(bg = self.bg_color_leave, fg = self.fg_color_leave)
        self.precio_ofertado.config(bg = self.bg_color_leave, fg = self.fg_color_leave)
    
    def expand_button(self):
        if self.expand_count == 0:
            self.frame.config(bd = 2)
            self.expand_count = 1
            self.sub_frame_description.pack(fill = "x",padx = 5, pady=5 )
            self.frame.pack(fill = "x", anchor="center", pady = 5)

        elif self.expand_count == 1:
            self.frame.config(bd = 0)
            self.expand_count = 0
            self.sub_frame_description.pack_forget()
            self.frame.pack(fill = "x", anchor="center", pady = 2)

    def oferta_desestimada(self):
        if self.porcentaje > 20:
            self.recomendacion.config(text ="Desestimado", font = self.FONT, width=18)
            self.bg_color_leave = "#F7BDBD"
            self.fg_color_leave = "black"
            
            self.bg_color_enter = "#F98585"
            self.fg_color_enter = "white"


    def mejor_oferta(self):        
        """este metodo se ejecuta con el frame container"""        
        self.bg_color_leave = "#B8DDCD"        
        self.bg_color_enter = "#88E7BF"

        self.frame.config(bg =self.bg_color_leave)
        
        self.sub_frame_main.config(bg =self.bg_color_leave)
        self.sub_frame_description.config(bg=self.bg_color_leave)
        self.recomendacion.config(bg =self.bg_color_leave, text ="Mejor Oferta", font = self.FONT_BOLD, width=17)
        self.opcion.config(bg =self.bg_color_leave,  font = self.FONT_BOLD )
        self.empresa.config(bg =self.bg_color_leave,  font = self.FONT_BOLD )
        self.precio_ofertado.config(bg =self.bg_color_leave,  font = self.FONT_BOLD )
        self.porcentaje_excedido.config(bg =self.bg_color_leave,  font = self.FONT_BOLD )


if __name__ == "__main__":
    root = tk.Tk()
    # datos = FilaOferta(root,"empresa_1", 355787)
    frame = Main(root)
    root.title("COMPRA-MASTER")
    root.mainloop()



