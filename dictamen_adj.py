
import tkinter as tk
from tkinter import ttk, messagebox
import os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

import datetime
from docxtpl import DocxTemplate
import widgets

from docxtpl import DocxTemplate
import widgets, tree,  read_excel as xl
import admin_json


class Main:
    def __init__(self, parent):
        """permite crear un dictamen de adjudicacion
        """
        #parameters
        self.parent = parent

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill = "x")

        self.info = widgets.InfoFrame(self.frame)

        self.title_frame = widgets.HeadingFrame(self.frame, "Crear Dictamen de Adjudicación (CME)")
   
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")



        self.contratacion = None

        self.frame_widgets = tk.LabelFrame(self.frame, text ="Datos basicos del dictamen", pady = 5, padx= 5)
        self.frame_widgets.pack(fill ="x", pady = 5, padx= 5)

        self.arbol = tree.TreeviewData(self.frame)
        self.arbol.frame.pack(pady = 5, padx = 5)
        self.arbol.head({"N° PROCESO":{"width":150},"DETALLE":{"width":600, "anchor":"w"}})
        self.write_rows_tree()

        # widgets

        self.disp_fc = widgets.DocumentoSade(self.frame_widgets, "Dispo Adjudicación","DISFC",0,0)
        self.disp_fc.entry.config(width=4)
        self.fecha_publicacion = widgets.FechaDividido(self.frame_widgets, "Fecha publicación", 10,0) 
        self.fecha_publicacion.frame_main.grid(columnspan=3)


        # botones
        self.submit_button = tk.Button(self.frame_sup,relief ="groove" ,
                font = "Calibri 10 bold",cursor = "hand2", text = "GENERAR DOCUMENTO", command=self.verificar_entradas)
        self.submit_button.pack(side ="left", padx =5)

        self.open_template = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "VER PLANTILLA",
                                command = self.abrir_plantilla)
        self.open_template.pack(side ="right", padx =5)

        self.cleaner = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "LIMPIAR",
                                command = self.limpiar)
        self.cleaner.pack(side ="right", padx =5)

        self.limpiar()


    def update(self):
        print("actualizado")
        self.write_rows_tree()


    def abrir_plantilla(self):
        os.startfile(f"templates\DICTAMENADJUDICACION_CME.docx")

    def write_rows_tree(self):
        values = admin_json.open_json(admin_json.file)
        # contrataciones = [list(x.keys())[0] for x in values]
        lista = []

        for proceso in values:
            contratacion = list(proceso.keys())[0] 
            detalle = proceso[contratacion]["detalle"].upper()

            lista.append([contratacion,detalle])


        self.arbol.write_rows(lista)

    def limpiar(self):
        
        fecha_maniana= self.fecha_maniana()
        parametros = widgets.open_json("bd/parametros.json")
        self.disp_fc.data_anio.set(parametros["anio"])
        self.disp_fc.data_reparticion.set(parametros["reparticion_siglas"])

        self.fecha_publicacion.data_day.set(fecha_maniana[0]),
        self.fecha_publicacion.mes_consultas.data.set(widgets.MESES[int(fecha_maniana[1])-1]),
        self.fecha_publicacion.data_year.set(fecha_maniana[2])
        

        self.disp_fc.data.set("")

    def verificar_entradas(self):
        """verifica si todas las entradas necesarias fueron cargadas"""

        entradas = [
            self.disp_fc.data.get(),
            self.fecha_publicacion.get_fecha_numeros("-") 
        ]
        count = 0
        for entrada in entradas:
            if entrada == "":
                count+=1

        if count >1:
            print("se deben llenar todas las entradas")

        else:
            self.generate_file()
                
    def context(self):
        try:
            contratacion = self.arbol.element_clicked()[0]

            print(contratacion)
            parametros = widgets.open_json("bd/parametros.json")
            datos = admin_json.datos_basicos_contratacion(contratacion)
            empresas = admin_json.empresas_con_adjudicacion(contratacion)
            lista = [ f'{x} (CUIT N°{empresas[x][:2]}-{empresas[x][2:-1]}-{empresas[x][-1]})' for x in empresas]
            

            context = {
                "detalle":datos["detalle"],
                "contratacion":contratacion,
                "expediente":datos["expediente"],
                "disposicion_fc":self.disp_fc.get(),
                "anio":parametros["anio"],
                "publicacion_1":self.fecha_publicacion.get_fecha_numeros("/"),
                "publicacion":self.fecha_publicacion.get_fecha_numeros("-"),
                "lista_empresas":lista,
                
                "monto_adjudicado":xl.agregar_comas_precio(float(datos["monto_adjudicado"])),            
                "monto_adjudicado_letras":datos["monto_adjudicado_letras"].upper(),            
                "expediente":datos["expediente"],
            }
            
            self.info.success(f"Dictamen generado. 'DICTAMENADJUDICACION{''.join(context['contratacion'].split('-'))}'")
            return context

        except:
            self.info.warning("Seleccionar una contratación.")


    def generate_file(self):
        context = self.context()
        document = DocxTemplate("templates/DICTAMENADJUDICACION_CME.docx")
        document.render(context)

        name_document = f"DICTAMENADJUDICACION{''.join(context['contratacion'].split('-'))}.docx"
        document.save(f"{name_document}")
        #abrir el documento automaticamente
        os.startfile(f"{name_document}")
        # self.info.success(f"el documento creado {name_document}")
        
        messagebox.showinfo(message=f"El documento '{name_document}' fue creado con exito.\nGUARDAR EL ARCHIVO COMO .doc (Word 97)", title="Documento Creado")
    

        # self.info.success("Cargado exitosamente")
        # self.info.warning("Error: Hubo un Error al intentar crear el archivo")

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
    # print(ventana.write_rows_tree())
    root.mainloop()