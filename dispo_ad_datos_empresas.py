import tkinter as tk
from tkinter import ttk,filedialog as fd
from tkinter.filedialog import askopenfilename
import datetime, json, os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree, read_excel as xl
import admin_json


class Main:
    def __init__(self, parent, frame_next):
        """permite la navegacion de multiples frames en uno.
        el parametro 'sub_frames_list' debe ser una lista de frames u 
        objetos con un frame como atributo cuyo nombre debe ser 'frame'
        """
        #parameters
        self.parent = parent
        self.frame_next = frame_next
        #1
        self.contratacion = None

        # main frame
        self.frame = tk.Frame(self.parent)
        # self.frame.pack(side = "top", fill = "both", expand =1)
        
        self.title_frame = widgets.HeadingFrame(self.frame, "3 - Cargar datos por empresa")

        # frame para los botones de anterior y siguiente
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        # frame para intercambiar los subframes
        self.frame_screen = tk.Frame(self.frame, padx = 5, pady= 5)
        self.frame_screen.pack(expand= 1,  fill = "both", side = "bottom")
      
        self.sub_frames_list = None


        self.first_frame_button = tk.Button(self.frame_sup,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="1<<", cursor = "hand2", command = self.first_frame)
        self.first_frame_button.pack(side ="left", padx =3)
        
        self.before_button = tk.Button(self.frame_sup,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="<", cursor = "hand2", command = self.before_frame)
        self.before_button.pack(side ="left", padx =3)

        self.next_button = tk.Button(self.frame_sup,relief = "groove",width= 5,font = "Calibri 12",
                                    text =">", cursor = "hand2", command = self.next_frame)
        self.next_button.pack(side ="left", padx =3)

        self.last_frame_button = tk.Button(self.frame_sup,relief = "groove",width= 5,font = "Calibri 12",
                                       text =">>", cursor = "hand2", command = self.last_frame)
        self.last_frame_button.pack(side ="left", padx =3)

        self.numero_frame = 0

        self.counter = 0

    

    def next(self):
        print("pasar al siguiente frame 4- desestimaciones")
        self.counter+=1
        self.get_all_data()
        # permite no volver a instanciar los objetos del nextframe
        # creandolo solo una vez
        if self.counter <=1:            
            self.frame_next.crear_pagination(self.contratacion)
        else:
            pass

    def get_all_data(self):
        """devuelve todos los datos de todas las empresas"""
        for frame in self.sub_frames_list:
            frame.get_data()

    #pagination
    def next_frame(self):
        """permite pasar al siguiente frame"""
        try:            
            #carga los datos de la empresa
            self.sub_frames_list[self.numero_frame].get_data()

            self.numero_frame += 1
            if self.numero_frame > len(self.sub_frames_list)-1:
                self.numero_frame =len(self.sub_frames_list)-1
            else:
                self.hide_frame()
                try:
                    #toma el frame principal para empaquetarlo
                    self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
                except:                    
                    self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
                print("frame posterior", self.numero_frame)
        except Exception as e:
            print(e, "error en el metodo 'next_frame': dispo_ad_datos_empresas.py")

    def before_frame(self):
        """permite pasar al frame anterior"""
        try:
            #carga los datos de la empresa
            self.sub_frames_list[self.numero_frame].get_data()

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

    def reset(self):
        self.hide_frame()
        delete_classes = [x.__del__() for x in self.sub_frames_list]

        self.sub_frames_list = 0
        


    def first_frame(self):
        """pasa al primer frame"""
        try:
            #carga los datos de la empresa
            self.sub_frames_list[self.numero_frame].get_data()
            self.numero_frame =0
            self.hide_frame()
            try:
                self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
            except:
                self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
            print("primer frame", self.numero_frame)

        except Exception as e:
            print(e)

    def last_frame(self):
        """pasa al ultimo frame"""
        try:
            #carga los datos de la empresa
            self.sub_frames_list[self.numero_frame].get_data()
            self.numero_frame =len(self.sub_frames_list)-1
            self.hide_frame()
            try:
                self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
            except:
                self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
            print("primer frame", self.numero_frame)

        except Exception as e:
            print(e)

    def hide_frame(self):
        for frame in self.sub_frames_list:
            try:
                frame.frame.pack_forget()
            except:
                frame.pack_forget()

    def generar_lista_frames(self):
        """genera una lista de objetos 'FrameEmpresa'
        de las empresas que figuren"""
        lista_empresas = admin_json.lista_empresas_con_datos_completos(self.contratacion)
        lista_frames = []

        if lista_empresas == None:
            print("error, verificar el numero de contratacion seleccionado")
        else:
            # print(lista_empresas)
            count = 0
            for datos_empresa in lista_empresas:
                count +=1
                datos_empresa["#"] = count
                
                datos_empresa["cantidad_empresas"] = len(lista_empresas) 
                print(datos_empresa)
                frame_empresa = FrameEmpresa(self.frame_screen,self.contratacion,datos_empresa )
                lista_frames.append(frame_empresa)
        
        return lista_frames

    def crear_pagination(self, contratacion):
        print("creando paginacion para la desestimacion")
        # 1) reasinarle el numero de contratacion en la propiedad 'self.contratacion'
        self.contratacion = contratacion
        # 2) reasignar la propiedad 'self.sub_frames_list'
        #    la funcion propia de la clase "self.generar_lista_frames()"
        #    para generar la lista de frames de la clase 'FrameEmpresa'         
        self.sub_frames_list = self.generar_lista_frames()
        self.last_frame_button.config(text =f">>{len(self.sub_frames_list)}")
        
        # 3) luego ocultar todas las instacias        
        self.hide_frame()
        # 4) generar el primer objeto de la lista de instancias
        try:
            self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
        except:
            print("There are not frames")


class Prerrogativa:
    def __init__(self, parent, fila, columna):

        """frame para añadir los precios con prerrogativas."""
        self.parent = parent 
        self.fila = fila
        self.columna = columna


        self.boton = tk.Button(self.parent,text="Más opciones ▼",bd =0,command=self.hide_show_frame,
                                 fg = "blue", cursor="hand2")
        self.boton.grid(column = self.columna, row = self.fila, sticky="w")

        self.frame = tk.LabelFrame(self.parent, text ="Prerrogativa de Precio",padx = 5,pady = 5)
        self.hidden_frame = True

        self.prerrogativa = widgets.TagsAndEntry(self.frame, "Precio Anterior", 0,0)
        self.prerrogativa.entry.config(width=15)
        self.prerrogativa_letras = widgets.TagsAndEntryWithLink(self.frame,"en letras",1,0,
                                                                   "https://www.letrasnumeros.com/")
        self.prerrogativa_letras.entry.config(width=30)
        
    
    def disabled(self):
        self.boton.config(state="disabled")

 

    def hide_show_frame(self):
        if self.hidden_frame == False:
            self.hidden_frame = True
            self.boton.config( text ="Más opciones ▼")
            self.frame.grid_forget()
      
        elif self.hidden_frame == True:
            self.hidden_frame = False
            self.boton.config( text ="Menos opciones ▲")
            self.frame.grid(column = self.columna, row = self.fila+1, columnspan=2, sticky="we" )      
    



class FrameEmpresa:
    def __init__(self,parent,contratacion, empresa):
        """el parametro "empresa" debe ser un diccionario con los datos:
        "nombre_empresa", "renglones_totales", "renglones_adjudicados",
        "renglones_desestimados", "monto_total"
        """
        #parametros
        self.parent = parent
        self.contratacion = contratacion
        self.empresa = empresa["empresa"]

        self.numero_empresa = empresa["#"]
        self.cantidad_empresas = empresa["cantidad_empresas"]

        #propiedades
        self.fuentes = widgets.NORMAL_FONT

        #frames
        self.frame = tk.LabelFrame(self.parent, text = f"Empresa {self.numero_empresa} de {self.cantidad_empresas}",
                                   font="Calibri 14",  padx = 5, pady = 5 )
        self.frame.pack(expand=  1, fill = "both", pady = 5, padx = 5)
        
        #widgets
        self.empresa_widget = widgets.TagsAndEntry(self.frame,"Empresa" , 0,0)
        self.empresa_widget.entry.config(width = 35)       

        self.n_cuit = widgets.TagsAndEntry(self.frame, "N° CUIT (sin guiones)", 10,0)

        self.doc_complementaria = widgets.CheckBox( self.frame, "Documentacion complementaria",20 ,0)
        self.doc_complementaria.check_box.grid(columnspan=2)

        self.monto_adjudicado = widgets.TagsAndEntry(self.frame, "Monto total adjudicado", 30,0)        
        self.monto_adjudicado.disabled()

        self.precio_estimado_letras = widgets.TagsAndEntryWithLink(self.frame,
                                                                   "Precio Adjudicado\nen letras",40,0,
                                                                   "https://www.letrasnumeros.com/")
        self.precio_estimado_letras.entry.config(width=32)

        self.frame_prerrogativa = Prerrogativa(self.frame,50,0)

        self.set_widgets()

    def __del__(self):
        print("objeto destruido")

    def get_data_json(self):
        """toma los datos directos del json, para despues setearlo en 
        los widgets"""
        lista_empresas = admin_json.lista_empresas_con_datos_completos(self.contratacion)
        datos_json = {}
        for x in lista_empresas:
            # print(x["empresa"])
            if x["empresa"] == self.empresa:
                # print(x)
                datos_json["empresa"] = x["empresa"]
                datos_json["cuit"] = x["cuit"]
                datos_json["doc_complementaria"] = x["doc_complementaria"]
                datos_json["precio_total"] = x["precio_total"]
                datos_json["precio_total_letras"] = x["precio_total_letras"]
                datos_json["renglones_adjudicados"] = x["renglones_adjudicados"]

                #unir renglones desestimados
                datos_json["desestimados"] = x["renglones_desestimados"]["economicamente"]
                datos_json["desestimados"].extend(x["renglones_desestimados"]["administrativo"])
                datos_json["desestimados"].extend(x["renglones_desestimados"]["tecnicamente"])

                datos_json["monto_anterior"] = x["monto_anterior"]
                datos_json["monto_anterior_letras"] = x["monto_anterior_letras"]


        return datos_json

    def set_widgets(self):
        """setea todos los widgets"""
        # datos
        json_data = self.get_data_json()

        # seteos
        self.empresa_widget.data.set(json_data['empresa'])
        self.n_cuit.data.set(json_data["cuit"])

        self.monto_adjudicado.data.set(json_data["precio_total"])        
        

        if json_data["doc_complementaria"] == True:
            self.doc_complementaria.check()
        else :
            self.doc_complementaria.uncheck()


        if json_data["precio_total"] > 0.0:
            """si el existe un precio adjudicado que se habilite
            el precio en letras y la prerrogativa"""
            self.precio_estimado_letras.enable()
            self.precio_estimado_letras.data.set(json_data["precio_total_letras"])
            self.frame_prerrogativa.prerrogativa.data.set(json_data["monto_anterior"])
            self.frame_prerrogativa.prerrogativa_letras.data.set(json_data["monto_anterior_letras"])

        else:
            self.precio_estimado_letras.disabled()
            self.frame_prerrogativa.disabled()


    def get_data(self):
        """guarda los datos en el JSON"""
        datos_json = self.get_data_json()
        datos = {
            "empresa":self.empresa_widget.get(),
            "cuit":f'{self.n_cuit.get()}',
            "doc_complementaria": self.doc_complementaria.checked(),
            "precio_total_letras": self.precio_estimado_letras.get(),
            "monto_anterior": self.frame_prerrogativa.prerrogativa.get(),
            "monto_anterior_letras" : self.frame_prerrogativa.prerrogativa_letras.get()
        }

        #se modifica el valor del parametro contructor del objecto
        self.empresa = datos["empresa"]
        admin_json.modificar_datos_empresa(self.contratacion,datos_json["empresa"],datos )
        # self.set_widgets()






if __name__== "__main__":
    x1 = "PROCESOS/455-2053-CME20/Recomendacion-455-2053-CME20.xlsx"
    x2 = "PROCESOS/455-2053-CME20/Detalle-producto-05072023.xlsx"

    root = tk.Tk()

    excel = xl.LeerExcel(x1, x2)

    ventana = Main(root, excel)
    ventana.frame.pack()
    ventana.crear_pagination(excel)

    boton_reset = tk.Button(root, text="resetear", command=ventana.reset)
    boton_reset.pack(side = "top")
    root.mainloop()