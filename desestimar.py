import tkinter as tk
from tkinter import ttk,filedialog as fd
from tkinter.filedialog import askopenfilename
import datetime, json, os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree,  read_excel as xl
import admin_json, generar_texto

class Main:    
    def __init__(self, parent):
        """esta clase se inserta dentro de la clase Desestimar"""
        #parameters
        self.parent = parent
        self.contratacion = None
        

        # frames
        self.frame = tk.Frame(self.parent)
        # self.frame.pack(fill = "both",expand = 1, pady = 5, padx = 5)

        self.title_frame = widgets.HeadingFrame(self.frame, "4 - Desestimar Renglones")

        # lista de objetos instanciados del frame 'Desestimar'
        self.sub_frames_list = None
        # frame para los botones de anterior y siguiente
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")


        # botones
        self.first_frame_button = tk.Button(self.frame_sup,relief = "groove",width= 5,font = "Calibri 12",
                                       text ="1<<", cursor = "hand2", command = self.first_frame)
        self.first_frame_button.pack(side ="left", padx =3)

        self.before_button = tk.Button(self.frame_sup,width= 5,relief = "groove",font = "Calibri 12",
                                       text ="<", cursor = "hand2", command = self.before_frame)
        self.before_button.pack(side ="left", padx =3)

        self.next_button = tk.Button(self.frame_sup,width= 5,relief = "groove",font = "Calibri 12",
                                    text =">", cursor = "hand2", command = self.next_frame)
        self.next_button.pack(side ="left", padx =3)

        self.last_frame_button = tk.Button(self.frame_sup,relief = "groove",width= 5,font = "Calibri 12",
                                text =">>", cursor = "hand2", command = self.last_frame)
        self.last_frame_button.pack(side ="left", padx =3)


        self.numero_frame = 0

    def next(self):
        generar_documento = generar_texto.GenerateDocument(self.contratacion)
        generar_documento.create_word_file()

    def crear_pagination(self, contratacion):
        print("creando paginacion para la desestimacion")
        # 1) reasinarle el numero de contratacion en la propiedad 'self.contratacion'
        self.contratacion = contratacion
        # 2) reasignar la propiedad 'self.sub_frames_list'
        #    la funcion propia de la clase "self.generar_lista_frames()"
        #    para generar la lista de frames 'FrameEmpresa'         
        self.sub_frames_list = self.generar_lista_frames()
        self.last_frame_button.config(text = f">>{len(self.sub_frames_list)}")
        # 3) luego ocultar todas las instacias        
        self.hide_frame()
        # 4) generar el primer objeto de la lista de instancias
        try:
            self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
        except:
            print("There are not frames")


    #pagination
    def first_frame(self):
        """pasa al primer frame"""
        try:
            #carga los datos de la empresa
            self.sub_frames_list[self.numero_frame].frame_empresa.get_data()
            self.numero_frame =0
            self.hide_frame()
            try:
                self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
            except:
                self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
            print("primer frame", self.numero_frame)

        except Exception as e:
            print(e)
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
            print(e)

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



    def last_frame(self):
        """pasa al ultimo frame"""
        try:
            #carga los datos de la empresa
            self.sub_frames_list[self.numero_frame].frame_empresa.get_data()
            self.numero_frame =len(self.sub_frames_list)-1
            self.hide_frame()
            try:
                self.sub_frames_list[self.numero_frame].frame.pack(fill="both", expand =1)
            except:
                self.sub_frames_list[self.numero_frame].pack(fill="both", expand =1)
            print("primer frame", self.numero_frame)

        except Exception as e:
            print(e)


    def generar_lista_frames(self):
        """almacena en una lista todos los objetos instanciados
        de la clase Desestimar, tomando los datos de las empresas"""
        lista = []
        lista_empresas =admin_json.lista_empresas_con_datos_completos(self.contratacion)
        cantidad_empresas = len(lista_empresas)
        count  = 0
        for em in lista_empresas:
            count += 1 
            print(em)
            frame = Desestimar(self.frame, self.contratacion, em["empresa"])
            frame.frame_empresa.frame.config(text =f"Empresa {count} de {cantidad_empresas}")

            lista.append(frame)

        return lista
    
    def hide_frame(self):
        
        for frame in self.sub_frames_list:
            try:
                frame.frame.pack_forget()
            except:
                frame.pack_forget()

class FrameDatos:
    def __init__(self, parent,contratacion,  empresa):
        """esta clase se inserta dentro de la clase Desestimar"""
        #parameters
        self.parent = parent
        self.contratacion = contratacion
        self.empresa = empresa

        # frames
        self.frame = tk.LabelFrame(self.parent,pady = 5, padx = 5,text = "",font = "Calibri 14")
        self.frame.pack(fill = "x", padx =5)

        # widgets
        self.nombre_empresa = widgets.TagsAndEntry(self.frame, "nombre de Empresa", 10, 0)
        self.nombre_empresa.disabled()
        
        self.renglones_adj = widgets.TagsAndEntry(self.frame, "Renglones Adjudicados", 30, 0)
        self.renglones_adj.entry.config(width=10)
        self.renglones_adj.disabled()

        self.check = widgets.CheckBox(self.frame, "Desestimar Administrativamente", 30, 2)
        self.check.uncheck()

        self.label_info_check = tk.Label(self.frame, text ="", fg = "red", font= "Calibri 12 bold")
        self.label_info_check.grid(row = 40, column=0, columnspan=3, sticky="we")
        
        self.datos = admin_json.datos_empresa( self.contratacion, self.empresa) 
        
              
        if len(self.datos["renglones_adjudicados"]) >0:
            self.check.desabilitar()
        else:
            self.check.habilitar()


        
        self.get_data()

    def get_data(self):
        self.nombre_empresa.data.set(self.datos["empresa"])
        self.renglones_adj.data.set(len(self.datos["renglones_adjudicados"]))

class Desestimar:
    def __init__(self, parent,contratacion, empresa):
        #parameters
        self.parent = parent
        self.contratacion = contratacion
        self.empresa = empresa

        # frames        
        self.frame = tk.Frame(self.parent, )
        self.frame.pack( expand = 1,fill = "y")

        self.frame_empresa = FrameDatos(self.frame,self.contratacion, self.empresa)
        self.frame_empresa.check.check_box.bind("<ButtonRelease-1>", self.desestimar_admin)
        self.frame_empresa.frame.config(text =f"")

        self.frame_trees = tk.Frame(self.frame, width = 600)
        self.frame_trees.pack(fill = "y",expand = 1, pady = 5, padx = 5)

        self.frames_buttons = tk.Frame(self.frame_trees)
        
        # widgets_buttons
        self.button_right = ttk.Button(self.frames_buttons, width=7,command = self.pasar_de_a_al_b,  cursor = "hand2", text =">")
        self.button_right.pack()

        self.button_left = ttk.Button(self.frames_buttons, width=7,command = self.pasar_de_b_al_a, cursor = "hand2", text ="<")
        self.button_left.pack()

        # trees
        #tabla desestimaciones economicos
        self.tabla_a = tree.TreeviewData(self.frame_trees)
        self.tabla_a.frame.pack(side="left")
        self.tabla_a.head(["ECONÓMICOS"])
        self.escribir_tabla_a()

        self.frames_buttons.pack(fill = "y",expand = 1,side="left", pady = 5, padx = 5)

        #tabla desestimaciones tecnicos
        self.tabla_b = tree.TreeviewData(self.frame_trees)
        self.tabla_b.frame.pack(side="right")
        self.tabla_b.head(["TÉCNICOS"])
        self.escribir_tabla_b()
        
        if len(self.frame_empresa.datos["renglones_desestimados"]["administrativo"]) >0:
            self.frame_empresa.check.check()
        else:
            self.frame_empresa.check.uncheck()



    #eventos
    def desestimar_admin(self, e):
        """si al presionar el boton iz del mouse, activa: 
        que desestime administrativamente todos los renglones"""
        if self.frame_empresa.check.habilitado == True:
            data = self.frame_empresa.check.checked()
            if data == False:
                texto = """DESESTIMACIÓN ADMINISTRATIVA ACTIVA:\nDesestima todos los renglones como 'administrativo'"""
                self.frame_empresa.label_info_check.config(text =texto)
                admin_json.desestimar_administrativamente(self.contratacion, self.empresa)
                print(data, "desestimar administrativamente")
                self.escribir_tabla_a()
                self.escribir_tabla_b()
                # escribir "tabla a"           
                # escribir "tabla b"

            elif data == True:
                self.frame_empresa.label_info_check.config(text ="")
                admin_json.desestimar_economicamente(self.contratacion, self.empresa)
                print(data, "desestimar economicamente")
                self.escribir_tabla_a()
                self.escribir_tabla_b()
                # escribir "tabla a"
                # escribir "tabla b"
        else:
            print("checkbox inabilitado para ser seleccionado")


    def pasar_de_a_al_b(self):
        """pasa los items seleccionados de 'a' a 'b'"""
        #1- tomar los items seleccionados
        #2- eliminarlo de la lista "economicamente" del json
        # y agregarlo al "tecnicamente"
        items_selected= self.tabla_a.get_multiple_rows()
        admin_json.eliminar_renglones_economicos(self.contratacion, self.empresa,items_selected)
        admin_json.agregar_renglones_tecnicas(self.contratacion, self.empresa,items_selected)
        self.escribir_tabla_a()
        self.escribir_tabla_b()
        # print("pasando de la tabla economicas a tecnicas")
        pass

    def pasar_de_b_al_a(self):
        """pasa los items seleccionados de 'b' a 'a'"""

        items_selected= self.tabla_b.get_multiple_rows()
        admin_json.eliminar_renglones_tecnicos(self.contratacion, self.empresa,items_selected)
        admin_json.agregar_renglones_economicos(self.contratacion, self.empresa,items_selected)
        self.escribir_tabla_a()
        self.escribir_tabla_b()
        
        # print("pasando de la tabla tecnicas a economicas")

    def escribir_tabla_a(self):
        lista_renglones = admin_json.datos_empresa(self.contratacion, self.empresa)["renglones_desestimados"]["economicamente"]
        lista_renglones.sort()
        self.tabla_a.write_rows(lista_renglones)

    def escribir_tabla_b(self):
        lista_renglones = admin_json.datos_empresa(self.contratacion, self.empresa)["renglones_desestimados"]["tecnicamente"]
        lista_renglones.sort()
        self.tabla_b.write_rows(lista_renglones)


if __name__== "__main__":
    contratacion = "455-2243-CME21"
    empresa = "CIENTIFICA PARQUE CENTENARIO S.R.L."

    root=tk.Tk()
    datos = Main(root)
    datos.frame.pack()
    datos.crear_pagination(contratacion)
    root.mainloop()

