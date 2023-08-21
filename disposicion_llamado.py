import tkinter as tk
from tkinter import ttk, messagebox
import widgets
import webbrowser
import os

from docxtpl import DocxTemplate
import datetime
import read_excel as xl

class BlockButton:
    def __init__(self, parent, fila, columna, entrada=None):
        # parametros
        self.parent = parent
        self.entrada = entrada

        self.boton = tk.Button(self.parent, text ="block", command = self.block_command)
        self.boton.grid(row = fila, column = columna )
        self.block = True
        self.block_command()

    def block_command(self):
        if self.block == True:
            self.block = False
            self.entrada.disabled()
            print("bloquear")
        elif self.block == False:
            self.block = True
            self.entrada.enable()
            print("desbloquear")


class MainWindow:
    def __init__(self, parent):
        # parameters
        self.parent = parent

        #propierties
        # get current date
        self.date_current = datetime.datetime.now()
        self.current_year = self.date_current.year
        self.parametros = widgets.open_json("bd/parametros.json")
        self.tipos_contrataciones = self.parametros["tipos_contrataciones"]


        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill = "x")
        
        self.info = widgets.InfoFrame(self.frame)        
        
        self.title_frame = widgets.HeadingFrame(self.frame, "Crear Disposición de llamado (Contratación Menor)")

        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")
        # self.config = widgets.ConfigFrame(self.frame)

        self.main_frame = ttk.Frame(self.frame, padding=10 )
        self.main_frame.pack(fill = "x")



        # widgets
        self.tipo_contratacion = widgets.TagsAndOptions(self.main_frame,"tipo de Contratación",10,0,["CME","CDI","LPU"])
        self.tipo_contratacion.data.set("CME")
        self.tipo_contratacion.desplegable.config(width=10)
        self.tipo_contratacion.desplegable.grid(sticky="w")
        self.tipo_contratacion.desplegable.bind('<<ComboboxSelected>>',
                                                lambda x: self.cambiar_tipo_contratacion())

        
        self.contratacion = self.tipos_contrataciones[self.tipo_contratacion.data.get()]
        print("tipo de contratacion", self.contratacion)

        self.detalle = widgets.TagsAndEntry(self.main_frame,"Detalle",20,0)
        self.detalle.entry.config(width=42)

        self.ex_electronico = widgets.DocumentoSade(self.main_frame,"N° Expediente","EX",30,0)
        self.proceso_numero = widgets.NumeroBac(self.main_frame, "N° de Proceso",["CME","CDI","LPU"],40,0)
        self.proceso_numero.tipo_document.set(self.tipo_contratacion.data.get())
        self.proceso_numero.siglas_tipo.config(state = "disabled")

        self.sg_numero = widgets.NumeroBac(self.main_frame, "Solicitud de Gasto","SG",50,0)
        self.sg_numero.tipo_document.set("SG")
        self.sg_numero.siglas_tipo.config(state = "disabled")

        self.pliego = widgets.DocumentoSade(self.main_frame,"N° Pliego","PLIEG",60,0)

        self.precio = widgets.TagsAndEntry(self.main_frame,"Precio Estimado",65,0)
        self.precio.entry.grid(columnspan = 99 )
        self.precio.info_frame = self.info
        self.precio.info_text = "Escribir el precio estimado de la contratación, los decimales con punto. Ej: 1500.5"

        self.precio_a_letras = widgets.TagsAndEntryWithLink(self.main_frame,"Precio en letras",70,0,
                                                            "https://www.letrasnumeros.com/")
        self.precio_a_letras.info_text="Cargar en letras el precio estimado de la contratación. No es necesario escribir en mayúsculas."
        self.precio_a_letras.info_frame = self.info

        self.fecha_recepcion = widgets.FechaDividido(self.main_frame, "fecha límite para\nrecepción de ofertas", 80,0)

        # botones
        self.submit_button = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10 bold",cursor = "hand2", text = "GENERAR DOCUMENTO", command=self.verify_all_entries)
        self.submit_button.pack(side ="left", padx =5)

        self.open_template = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "VER PLANTILLA",
                                command = self.abrir_plantilla)
        self.open_template.pack(side ="right", padx =5)

        self.cleaner = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "LIMPIAR",
                                command = self.limpiar)
        self.cleaner.pack(side ="right", padx =5)

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
            self.title_frame.title.config(text = "Crear Disposición de llamado (Contratación Menor)")
            print("esto es una contratacion menor", self.contratacion)
        
        elif siglas =="CDI":
            self.proceso_numero.tipo_document.set(siglas)
            self.contratacion = self.tipos_contrataciones[siglas]
            self.title_frame.title.config(text = "Crear Disposición de llamado (Contratación Directa)")
            print("esto es una contratacion directa", self.contratacion)
            
        elif siglas =="LPU":
            self.proceso_numero.tipo_document.set(siglas)
            self.contratacion = self.tipos_contrataciones[siglas]
            self.title_frame.title.config(text = "Crear Disposición de llamado (Licitación Pública)")
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
                self.info.success(f"se ingreso correctamente")
            except Exception as e:
                self.info.warning(f"hay un error: {e}")
                print(f"{e}")

    def get_data(self):        
        parametros = widgets.open_json("bd/parametros.json")
        
        self.context = {
            "anio":parametros["anio"],
            "ley":parametros["ley"],
            "anio_dos_cifras":parametros["anio"][2:],
            "decreto_reglamentario":parametros["decreto_reglamentario"],
            "art_informatizacion_contrataciones":parametros["art_informatizacion_contrataciones"],
            "art_seleccion_ofertas":parametros["art_seleccion_ofertas"],
            "art_cme":parametros["art_cme"],
            "reparticion_siglas":parametros["reparticion_siglas"],

            "detalle":self.detalle.get(),
            "detalle_mayusc":self.detalle.get().upper(),
            #expediente electronico
            "expediente_electronico":self.ex_electronico.get().split("-")[2],
            "ee_anio":self.ex_electronico.get().split("-")[1],
            "ee_reparticion":self.ex_electronico.get().split("-")[-1],

            "tipo_contratacion":self.contratacion,
            "numero_proceso":self.proceso_numero.get(),
            "numero_pliego":self.pliego.get(),
            "solicitud_gasto":self.sg_numero.get(),
            "precio":xl.agregar_comas_precio(float(self.precio.get())),
            "precio_a_letras":self.precio_a_letras.get().upper(),
            
            "fecha_recepcion_dia":self.fecha_recepcion.get()[0],
            "fecha_recepcion_mes":self.fecha_recepcion.get()[1],
            "fecha_recepcion_anio":self.fecha_recepcion.get()[2],
            }

        return self.context

    def abrir_plantilla(self):
        os.startfile(f"templates\DISPOLLAMADO_CME.docx")

    def generate_file(self, context):
        try:
            
            siglas = self.tipo_contratacion.data.get()
            if siglas == "CME":
                document = DocxTemplate("templates/DISPOLLAMADO_CME.docx")
            elif siglas == "CDI":
                document = DocxTemplate("templates/DISPOLLAMADO_CDI.docx")
            elif siglas == "LPU":
                document = DocxTemplate("templates/DISPOLLAMADO_LPU.docx")

            document.render(context)
            name_path = f"{widgets.open_parameter('path_output')}"
            name_document = f"DISPOLLAMADO{context['numero_proceso']}.docx"
            # guardar archivo generado
            document.save(f"{name_document}")

            self.info.success(f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}")            
            messagebox.showinfo(message=f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}", title="Documento Creado")
            
            # abre el archivo generado automaticamente
            os.startfile(f"{name_document}")
        except Exception as e: 
            self.info.warning(f"Error: Hubo un Error al intentar crear el archivo\n{e}")



    def limpiar(self):
        print("limpiar entradas")
        self.detalle.limpiar()
        self.ex_electronico.limpiar()
        self.proceso_numero.limpiar()
        self.sg_numero.limpiar()
        self.pliego.limpiar()
        self.precio.limpiar()
        self.precio_a_letras.limpiar()
        self.fecha_recepcion.limpiar()

        self.set_widgets()


    def set_widgets(self):

        parametros = widgets.open_json("bd/parametros.json")
        self.ex_electronico.data_reparticion.set(parametros["reparticion_siglas"])
        self.ex_electronico.data_anio.set(parametros["anio"])

        self.proceso_numero.data_anio.set(parametros["anio"][2:])
        self.proceso_numero.data_num_reparticion.set(parametros["reparticion_num"])

        self.sg_numero.data_anio.set(parametros["anio"][2:])
        self.sg_numero.data_num_reparticion.set(parametros["reparticion_num"])

        self.pliego.data_anio.set(parametros["anio"])
        self.pliego.data_reparticion.set(parametros["reparticion_siglas"])

        self.fecha_recepcion.data_year.set(parametros["anio"])

if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)

    root.mainloop()
