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
import dispo_ad_datos_empresas as frame_empresas
import desestimar


class Exceles:
    def __init__(self, parent, frame_next):
        """primer paso: carga de exceles."""
        #parameters
        self.parent = parent
        self.frame_next = frame_next

        # frames
        self.frame = tk.Frame(self.parent)
        self.title_frame = widgets.HeadingFrame(self.frame, "1 - Cargar Exceles")
        self.frame_widgets = tk.Frame(self.frame)
        self.frame_widgets.pack(fill = "x")
        
        # data
        self.data_recomendacion = tk.StringVar()
        self.data_renglones = tk.StringVar()

        # widgets
        self.label_recomendacion = ttk.Label(self.frame_widgets,cursor = "hand2",font = "Calibri 12",text ="Excel de Recomendacion: ")
        self.label_recomendacion.grid(column = 0, row = 0, pady = 3,sticky="e")  
        self.label_recomendacion.bind("<Button-1>",lambda x: self.focus_entry(self.label_xl_recomendacion))
        

        self.label_xl_recomendacion = ttk.Entry(self.frame_widgets,font = "Calibri 12",width = 50, textvariable=self.data_recomendacion)
        self.label_xl_recomendacion.grid(column = 1, row = 0, pady = 3)

        self.xl_recomendacion = ttk.Button(self.frame_widgets,width=6,cursor = "hand2", text ="Abrir", command = self.open_excel_recomendacion)
        self.xl_recomendacion.grid(column = 2, row = 0, pady = 3, padx = 3)

        self.label_renglones = ttk.Label(self.frame_widgets,cursor = "hand2",font = "Calibri 12",text ="Excel de Renglones: ")
        self.label_renglones.grid(column = 0, row = 1, pady = 3,sticky="e")
        self.label_renglones.bind("<Button-1>",lambda x: self.focus_entry(self.label_xl_renglones))

        self.label_xl_renglones = ttk.Entry(self.frame_widgets,font = "Calibri 12",width = 50,textvariable=self.data_renglones)
        self.label_xl_renglones.grid(column = 1, row = 1, pady = 3)

        self.xl_renglones = ttk.Button(self.frame_widgets,width=6,cursor = "hand2", text ="Abrir", command = self.open_excel_renglones)
        self.xl_renglones.grid(column = 2, row = 1, pady = 3, padx = 3)


        self.label_recordatorio = tk.Label(self.frame_widgets, text="RECORDATORIO:\nABRIR LOS DOS ARCHIVOS EXCEL Y PRESIONAR 'HABILITAR EDICION', GUARDAR Y CERRAR.", bg="yellow", font="Calibri 12 bold")
        self.label_recordatorio.grid(column = 0, row = 2, columnspan=3, pady = 5)

        # self.boton_procesar = ttk.Button(self.frame_widgets, text ="PROCESAR EXCELES ", command = self.cargar_datos_basicos,cursor = "hand2")
        # self.boton_procesar.grid(column = 0, row = 2, columnspan=3, pady = 5)

        self.counter = 0


    # methods
    def focus_entry(self,entry):
        try:
            entry.focus()
        except:
            print("La entrada de texto fue destruida")


    def next(self):
        if self.data_recomendacion.get() == "" or self.data_renglones.get() == "" :
            print("por favor engresar exceles correctamente")
        else:       
            self.counter += 1
            if self.counter <=1:
                self.cargar_datos_basicos()
            else:
                pass

    def open_excel_recomendacion(self):
        self.xl_recomendacion = fd.askopenfilename()
        self.data_recomendacion.set(self.xl_recomendacion)
        print(self.xl_recomendacion)
        return self.xl_recomendacion
    
    def open_excel_renglones(self):
        self.excel_renglones = fd.askopenfilename()
        self.data_renglones.set(self.excel_renglones)
        print(self.excel_renglones)
        return self.excel_renglones

    def cargar_datos_basicos(self):
        # tomar el n° de contratacion
        contratacion = admin_json.JsonAdmin(self.data_recomendacion.get(), self.data_renglones.get())
        if contratacion.agregar_proceso() == "False":
            print("Error al cargar los exceles")
        elif contratacion.agregar_proceso() != "False":
            # cargar los datos en el 2°frame: 'DatosGenerales'.
            self.frame_next.set_widgets(contratacion.agregar_proceso())
            print(contratacion.agregar_proceso())
        # return contratacion        

class DatosGenerales:
    def __init__(self, parent, frame_next):
        # parameters
        self.parent = parent
        self.frame_next = frame_next
        
        # propiedades 
        # anio actual
        self.date_current = datetime.datetime.now()
        self.current_year = self.date_current.year

        # frames
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill = "both", expand=1)

        self.title_frame = widgets.HeadingFrame(self.frame, "2 - Datos Básicos de la Contratación")

        self.main_frame = ttk.Frame(self.frame,padding=5)
        self.main_frame.pack(fill = "both", expand=1)

        self.widgets_frames = tk.Frame(self.main_frame)
        self.widgets_frames.grid(column = 0 , row = 20, columnspan=3, sticky="we")

        
        # widgets        
        self.numero_proceso = widgets.NumeroBac(self.widgets_frames, "N° de Proceso","CME",0,0)
        self.numero_proceso.disabled()

        self.expediente = widgets.DocumentoSade(self.widgets_frames, "Numero de expediente","EX", 10,0)
        self.expediente.disabled()

        self.fecha_recepcion = widgets.FechaDividido(self.widgets_frames, "Fecha de Apertura", 20,0)
        self.fecha_recepcion.frame_main.grid(columnspan=3)
        self.fecha_recepcion.delimitador_1.config(text="de")
        self.fecha_recepcion.delimitador_2.config(text="de")
        self.fecha_recepcion.disabled()

        self.detalle = widgets.TagsAndEntry(self.widgets_frames, "Detalle", 30,0)
        self.detalle.entry.config(width = 32)

        # widgets para la dispo de llamado
        self.num_dispo = widgets.DocumentoSade(self.widgets_frames, "N° Dispo Llamado","DI", 35,0)
        self.num_dispo.entry.config(width = 5)

        self.informe_grafico = widgets.DocumentoSade(self.widgets_frames, "Informe de Recomendación","IF", 37,0)

        self.precio_estimado = widgets.TagsAndEntry(self.widgets_frames, "Precio estimado", 40,0)
        self.precio_estimado.disabled()
        self.precio_estimado_letras = widgets.TagsAndEntryWithLink(self.widgets_frames,"Precio Estimado\nen letras",50,0,
                                                            "https://www.letrasnumeros.com/")
        self.precio_estimado_letras.entry.config(width=32)

        self.precio_adj_total = widgets.TagsAndEntry(self.widgets_frames, "Precio Total Adjudicado", 60,0)
        self.precio_adj_total.disabled()
        self.precio_adj_total_letras = widgets.TagsAndEntryWithLink(self.widgets_frames,"Precio Adjudicado\nen letras",70,0,
                                                            "https://www.letrasnumeros.com/")
        self.precio_adj_total_letras.entry.config(width=32)

        # Firmas confimadas interesadas
        self.cantidad_firmas = widgets.TagsAndEntry(self.widgets_frames, "Firmas interesadas", 80,0)
        self.cantidad_firmas.entry.config(width=5)

        # Firmas confimadas confirmadas
        self.cantidad_firmas_confirmadas = widgets.TagsAndEntry(self.widgets_frames, "Firmas Confirmadas", 85,0)
        self.cantidad_firmas_confirmadas.entry.config(width=5, state="disabled")

        # self.submit_button = ttk.Button(self.widgets_frames, text ="Agregar Proceso",cursor = "hand2", command = self.get_data)
        # self.submit_button.grid(row = 98, column = 0, columnspan=3)

        self.cleaner_button = ttk.Button(self.widgets_frames, text ="Limpiar",cursor = "hand2", command = self.limpiar)
        self.cleaner_button.grid(row = 99, column = 0, columnspan=3)


        # el counter es para no volver a instanciar los 
        # objetos del nextframe
        self.counter = 0


    def next(self):
        print("pasar al siguiente frame")
        self.counter+=1
        self.get_data()

        # permite no volver a instanciar los objetos del nextframe
        # creandolo solo una vez
        if self.counter <=1:            
            self.frame_next.crear_pagination(self.numero_proceso.get())
        else:
            pass


    def set_widgets(self, contratacion):
        """toma los datos basicos de la contratacion 
        directos del json, para despues setearlo en los widgets"""
        datos = admin_json.datos_basicos_contratacion(contratacion)
        expediente = datos["expediente"].split("-")
        dispo_simple = datos["num_dispo"].split("-")
        if_grafico = datos["informe_grafico"].split("-")
        parametros = widgets.open_json("bd/parametros.json")

        print(len(dispo_simple), len(if_grafico),contratacion)

        #precargados
        # seteando el numero de proceso
        self.numero_proceso.data.set(contratacion.split("-")[1])
        self.numero_proceso.data_num_reparticion.set(contratacion.split("-")[0])
        self.numero_proceso.tipo_document.set(contratacion.split("-")[2][:3])
        self.numero_proceso.data_anio.set(contratacion[-2:])

        # seteando el numero de expediente
        self.expediente.data.set(expediente[2])
        self.expediente.data_anio.set(expediente[1])
        self.expediente.data_reparticion.set(expediente[4])        


        self.fecha_recepcion.data_day.set(datos["fecha_apertura"]["dia"])
        self.fecha_recepcion.mes_consultas.data.set(str(self.fecha_recepcion.MESES[int(datos["fecha_apertura"]["mes"])-1]))        
        self.fecha_recepcion.data_year.set(datos["fecha_apertura"]["anio"])
        self.precio_estimado.data.set(datos["monto_estimado"])
        self.precio_adj_total.data.set(admin_json.monto_total_adjudicado(contratacion))
        self.cantidad_firmas_confirmadas.data.set(datos["firmas_confirmadas"])
        # self.cantidad_firmas_confirmadas_letras.data.set(datos["firmas_confirmadas_letras"])

        #cargadas a mano
        self.detalle.data.set(datos["detalle"])
        
        if len(dispo_simple)!=1:
            self.num_dispo.data.set(dispo_simple[2])
            self.num_dispo.data_anio.set(dispo_simple[1])
            self.num_dispo.data_reparticion.set(dispo_simple[-1])
        else:
            self.num_dispo.data_anio.set(expediente[1])
            self.num_dispo.data_reparticion.set(parametros["reparticion_siglas"])


        if len(if_grafico) !=1:
            self.informe_grafico.data.set(if_grafico[2])
            self.informe_grafico.data_anio.set(if_grafico[1])
            self.informe_grafico.data_reparticion.set(if_grafico[-1])
        else:
            self.informe_grafico.data_anio.set(expediente[1])            
            self.informe_grafico.data_reparticion.set(parametros["reparticion_siglas"])

        self.precio_estimado_letras.data.set(datos["monto_estimado_letras"])
        self.precio_adj_total_letras.data.set(datos["monto_adjudicado_letras"])
        self.cantidad_firmas.data.set(datos["firmas_interesadas"])
        
    def limpiar(self):
        """limpia las entradas de texto disponibles"""
        expediente = self.expediente.get().split("-")
        self.detalle.limpiar()
        self.num_dispo.limpiar()
        self.num_dispo.data_reparticion.set(expediente[-1])
        self.num_dispo.data_anio.set(expediente[1])

        self.informe_grafico.limpiar()
        self.informe_grafico.data_reparticion.set(expediente[-1])
        self.informe_grafico.data_anio.set(expediente[1])

        self.cantidad_firmas.limpiar()
        self.precio_estimado_letras.limpiar()
        self.precio_adj_total_letras.limpiar()
        
        self.detalle.focus_entry()

    def get_data(self):
        contratacion = self.numero_proceso.get()
        detalle = self.detalle.get()
        num_dispo = self.num_dispo.get()
        if_graf = self.informe_grafico.get()
        precio_est_letras = self.precio_estimado_letras.get()
        precio_adj = self.precio_adj_total.get()
        precio_adj_letras = self.precio_adj_total_letras.get()
        firmas_interes = self.cantidad_firmas.get()

        admin_json.actualizar_dato_contratacion(contratacion,"detalle",detalle )
        admin_json.actualizar_dato_contratacion(contratacion,"num_dispo",num_dispo )
        admin_json.actualizar_dato_contratacion(contratacion,"informe_grafico",if_graf )
        admin_json.actualizar_dato_contratacion(contratacion,"monto_estimado_letras",precio_est_letras )
        admin_json.actualizar_dato_contratacion(contratacion,"monto_adjudicado",precio_adj )
        admin_json.actualizar_dato_contratacion(contratacion,"monto_adjudicado_letras",precio_adj_letras )
        admin_json.actualizar_dato_contratacion(contratacion,"firmas_interesadas",firmas_interes )
        print("datos cargados")


class Main:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        #frames
        self.frame = tk.Frame(self.parent)
        self.frame.pack(side = "top", fill = "both", expand =1)
        
        self.info = widgets.InfoFrame(self.frame)

        
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        self.frame_screen = tk.Frame(self.frame, padx = 5, pady= 5)
        self.frame_screen.pack(expand= 1,  fill = "both", side = "bottom")


        # frame 4
        self.desestimaciones = desestimar.Main(self.frame_screen)

        # frame 3
        self.datos_empresas = frame_empresas.Main(self.frame_screen, self.desestimaciones)

        # frame 2
        self.datos_generales = DatosGenerales(self.frame_screen, self.datos_empresas)

        #frame 1
        self.exceles = Exceles(self.frame_screen, self.datos_generales)
        self.exceles.frame.pack()

        self.open_template = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "VER PLANTILLA",
                                command = self.abrir_plantilla)
        self.open_template.pack(side ="right", padx =5)

        # lista de frames para la paginacion
        self.frame_list = [self.exceles,self.datos_generales,self.datos_empresas,self.desestimaciones ]

        self.before_button = tk.Button(self.frame_sup,relief = "groove",font = "Calibri 10 bold",
                                     text ="< Anterior", cursor = "hand2", command = self.before_frame)
        self.before_button.pack(side ="left", padx =5)

        self.next_button = tk.Button(self.frame_sup,relief = "groove",font = "Calibri 10 bold",
                                     text ="Siguiente >", cursor = "hand2", command = self.frame_next)
        self.next_button.pack(side ="left", padx =5)




        self.hide_frame()
        self.numero_frame = 0
        self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)


    def frame_next(self):            
        try:
            # primero se llama al metodo del frame next() 
            self.frame_list[self.numero_frame].next()
            
            self.numero_frame += 1
            if self.numero_frame > len(self.frame_list)-1:
                self.numero_frame =len(self.frame_list)-1
            else:
                self.hide_frame()
                self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1,pady= 5, padx = 5)
                
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
                self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1,pady= 5, padx = 5)
                print("frame anterior", self.numero_frame)
        except Exception as e:
            print(e)

    def hide_frame(self):
        for frame in self.frame_list:
            frame.frame.pack_forget()

    def abrir_plantilla(self):
        os.startfile(f"templates\DISPOADJUDICACION_CME.docx")

if __name__== "__main__":
    root = tk.Tk()

    datos_basicos = Main(root)
    root.mainloop()