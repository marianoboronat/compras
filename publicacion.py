
import tkinter as tk
from tkinter import ttk, messagebox
import os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

import datetime
from docxtpl import DocxTemplate
import widgets


class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        #propierties
        # get current date
        self.date_current = datetime.datetime.now()
        self.current_year = self.date_current.year
        self.parametros = widgets.open_json("bd/parametros.json")
        self.tipos_contrataciones = self.parametros["tipos_contrataciones"]

        # frames
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill = "both", expand = 1)
        
        self.info = widgets.InfoFrame(self.frame)
        # self.config = widgets.ConfigFrame(self.frame)

        self.title_frame = widgets.HeadingFrame(self.frame, "Crear Dictamen de Llamado (Contratación Menor)")

        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        self.main_frame = ttk.Frame(self.frame, padding = 10)
        self.main_frame.pack(fill = "x", padx = 7, pady = 7)    

        #widgets
        self.tipo_contratacion = widgets.TagsAndOptions(self.main_frame,"tipo de Contratación",10,0,["CME","CDI","LPU"])
        self.tipo_contratacion.data.set("CME")
        self.tipo_contratacion.desplegable.config(width=10)
        self.tipo_contratacion.desplegable.grid(sticky="w")
        self.tipo_contratacion.desplegable.bind('<<ComboboxSelected>>',
                                                lambda x: self.cambiar_tipo_contratacion())

        self.contratacion = self.tipos_contrataciones[self.tipo_contratacion.data.get()]

        self.detalle = widgets.TagsAndEntry(self.main_frame, "Detalle", 20, 0)
        self.detalle.entry.config(width=35)

        # widgets para el numero de proceso
        self.proceso_numero = widgets.NumeroBac(self.main_frame, "N° Proceso", "CME",25,0)
        self.proceso_numero.siglas_tipo.config(state = "disabled")
        self.proceso_numero.tipo_document.set(self.tipo_contratacion.data.get())

        self.numero_expediente = widgets.DocumentoSade(self.main_frame,"Expediente Electrónico","EX",30,0)
        self.numero_disposicion = widgets.DocumentoSade(self.main_frame,"Disposición Llamado","DI",40,0)
        self.numero_disposicion.entry.config(width =5)
        self.fecha_apertura = widgets.FechaDividido(self.main_frame, "Fecha de Apertura",50, 0)
        self.fecha_fin_consultas = widgets.FechaDividido(self.main_frame, "Fecha final de consultas\n(dos días anterior a la apertura)",60, 0)
        self.fecha_publicacion = widgets.FechaDividido(self.main_frame, "Fecha de publicacion",70,0)   

        
        self.submit_button = tk.Button(self.frame_sup,relief ="groove" ,font = "Calibri 10 bold",
                                       cursor = "hand2", text = "GENERAR DOCUMENTO", command= self.verify_all_entries)
        self.submit_button.pack(side ="left", padx =5)

        self.open_template = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "VER PLANTILLA",
                                command = self.abrir_plantilla)
        self.open_template.pack(side ="right", padx =5)

        self.cleaner = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "LIMPIAR",
                                command = self.limpiar)
        self.cleaner.pack(side ="right", padx =5)



        # setea los datos de los parametros
        self.set_widgets()

    def cambiar_tipo_contratacion(self):
        """al cambiar el combobox de 'self.tipo_contratacion' de contratacion
        cambia las siglas de los tipos de contrataciones.
        """
        siglas = self.tipo_contratacion.data.get()
        print(self.tipos_contrataciones)
        
        if siglas =="CME":
            self.proceso_numero.tipo_document.set(siglas)
            self.contratacion = self.tipos_contrataciones[siglas]
            self.title_frame.title.config(text ="Crear Dictamen de Llamado (Contratación Menor)")
            print("esto es una contratacion menor", self.contratacion)
        
        elif siglas =="CDI":
            self.proceso_numero.tipo_document.set(siglas)
            self.contratacion = self.tipos_contrataciones[siglas]
            self.title_frame.title.config(text ="Crear Dictamen de Llamado (Contratación Directa)")
            print("esto es una contratacion directa", self.contratacion)
            
        elif siglas =="LPU":
            self.proceso_numero.tipo_document.set(siglas)
            self.contratacion = self.tipos_contrataciones[siglas]
            self.title_frame.title.config(text ="Crear Dictamen de Llamado (Licitación Pública)")
            print("esto es una licitacion publica", self.contratacion)

    def verify_all_entries(self):
        valid = 0
        context = self.get_data()
        for data in context:
            # print(f"{context[data]}")
            if context[data] == "":
                valid += 1

        if valid > 0:
            self.info.warning(f"error se deben llenar todas las entradas")
            print("error se deben llenar todas las entradas")
        else:
            try:
                
                self.generate_file(context)
                #subir a la bd
            except Exception as e:
                self.info.warning(f"hay un error: {e}")
                print(f"{e}")

    def limpiar(self):
        self.detalle.limpiar()
        self.proceso_numero.limpiar()
        self.numero_expediente.limpiar()
        self.numero_disposicion.limpiar()
        self.fecha_apertura.limpiar()
        self.fecha_fin_consultas.limpiar()
        self.fecha_publicacion.limpiar()        
        self.detalle.entry.focus()

        self.set_widgets()

    def get_data(self):  
        parametros = widgets.open_json("bd/parametros.json")            
        self.context = {
            "anio":parametros["anio"],
            "detalle":self.detalle.get(),
            "detalle_mayusc":self.detalle.get().upper(),
            "anio_dos_cifras": parametros["anio"][2:],
            "reparticion_siglas":parametros["reparticion_siglas"],

            "numero_expediente":"-".join(self.numero_expediente.get().split("-")[1:]),
            "proceso":self.proceso_numero.get(),
            "numero_disposicion":self.numero_disposicion.get().split("-")[2],    
                    
                    
            "tipo_contratacion":self.contratacion,
            "fecha_apertura":self.fecha_apertura.get_fecha_numeros("/"),      
            "dia_consultas":self.fecha_fin_consultas.get()[0],
            "mes_consultas":self.fecha_fin_consultas.get()[1],
            "anio_consultas":self.fecha_fin_consultas.get()[2],
            "fecha_inicio":self.fecha_publicacion.get_fecha_numeros("-")
        }        

        return self.context


    def abrir_plantilla(self):
        os.startfile(f"templates\PUBLICACION.docx")
    
    def generate_file(self, context):
        try:
            document = DocxTemplate("templates/PUBLICACION.docx")
            document.render(context)
            name_path = f""
            name_document = f'PUBLICACION{"".join(context["proceso"].split("-"))}.docx'
            document.save(f"{name_path}{name_document}")
            #abrir el documento automaticamente
            os.startfile(f"{name_path}{name_document}")
            self.info.success(f"el documento creado {name_document} fue ubicado en la carpeta {name_path}")
            
            messagebox.showinfo(message=f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}", title="Documento Creado")
        
        except Exception as e: 
            print(e ,"ocurrio un error")
            self.info.success("Cargado exitosamente")
            # self.info.warning("Error: Hubo un Error al intentar crear el archivo")
    
    def set_widgets(self):
        """setea los datos de parametros"""
        parametros = widgets.open_json("bd/parametros.json")
        self.proceso_numero.data_num_reparticion.set(parametros["reparticion_num"])
        self.proceso_numero.data_anio.set(str(parametros["anio"])[2:])

        self.numero_expediente.data_anio.set(str(parametros["anio"]))
        self.numero_expediente.data_reparticion.set(parametros["reparticion_siglas"])

        self.numero_disposicion.data_anio.set(str(parametros["anio"]))
        self.numero_disposicion.data_reparticion.set(parametros["reparticion_siglas"])

        self.fecha_apertura.data_year.set(str(parametros["anio"]))
        self.fecha_fin_consultas.data_year.set(str(parametros["anio"]))


        fecha_maniana= self.fecha_maniana()        
        self.fecha_publicacion.data_day.set(fecha_maniana[0]),
        self.fecha_publicacion.mes_consultas.data.set(widgets.MESES[int(fecha_maniana[1])-1]),
        self.fecha_publicacion.data_year.set(fecha_maniana[2])


        

    def fecha_maniana(self):
        """Calcula la fecha posterior a la actual"""
        hoy = datetime.datetime.now()

        dia = int(hoy.strftime("%d"))
        mes = int(hoy.strftime("%m"))
        anio = int(hoy.strftime("%Y"))

        # calcular el dia de mañana
        try:
            dia+=1
            maniana_completo = datetime.datetime(anio, mes, dia)

            dia_maniana = int(maniana_completo.strftime("%d"))
            mes_maniana = int(maniana_completo.strftime("%m"))
            anio_maniana = int(maniana_completo.strftime("%Y"))
            return [dia_maniana, mes_maniana, anio_maniana]
        except:
            try:
                dia = 1
                mes +=1
                maniana_completo = datetime.datetime(anio, mes, dia)
                
                dia_maniana = int(maniana_completo.strftime("%d"))
                mes_maniana = int(maniana_completo.strftime("%m"))
                anio_maniana = int(maniana_completo.strftime("%Y"))
                return [dia_maniana, mes_maniana, anio_maniana]

            except:
                dia = 1
                mes = 1
                anio += 1
                maniana_completo = datetime.datetime(anio, mes, dia)

                
                dia_maniana = int(maniana_completo.strftime("%d"))
                mes_maniana = int(maniana_completo.strftime("%m"))
                anio_maniana = int(maniana_completo.strftime("%Y"))
                return [dia_maniana, mes_maniana, anio_maniana]



if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    root.mainloop()
