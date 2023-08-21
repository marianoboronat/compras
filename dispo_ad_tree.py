import tkinter as tk
from tkinter import ttk,filedialog as fd
from tkinter.filedialog import askopenfilename
import datetime, json, os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate
import widgets, tree,  read_excel as xl
import admin_json,dispocision_adjudicacion as adj


class Main:
    def __init__(self, parent):
        """permite la navegacion de multiples frames en uno.
        el parametro 'sub_frames_list' debe ser una lista de frames u 
        objetos con un frame como atributo cuyo nombre debe ser 'frame'
        """
        #parameters
        self.parent = parent

        # main frame
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill ="both", expand = 1,)


        self.title_frame = widgets.HeadingFrame(self.frame, "Crear Disposición de Adjudicación (CME)")

        # frame para el arbol
        self.frame_1 = tk.Frame(self.frame)
        self.frame_1.pack(fill ="both", expand = 1, side= "top")

        # frame para cargar la nueva dispo
        self.frame_2 = tk.Frame(self.frame)

        self.dispo_ajd_main = adj.Main(self.frame)
        self.dispo_ajd_main.frame.pack_forget()

        self.frame_sup = tk.Frame(self.frame_1, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(fill ="x",side= "top")

        # self.frame_screen = tk.Frame(self.frame_1, padx = 5, pady= 5)
        # self.frame_screen.pack(expand= 1,  fill = "both", side = "top")

        #tree
        self.arbol = tree.TreeviewData(self.frame_1)
        self.arbol.frame.pack(fill = "both",expand = 1,side ="top",pady = 5, padx = 5)
        self.arbol.head({"N° PROCESO":{"width":110},"DETALLE":{"width":600, "anchor":"w"}})
        self.write_rows_tree()


        # botones
        self.submit_button = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10 bold",cursor = "hand2",
                        text = "AGREGAR PROCESO", command=self.ocultar_frame_2)
        self.submit_button.pack(side ="left", padx =5)

        self.open_template = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "VER PLANTILLA",
                                command = self.abrir_plantilla)
        self.open_template.pack(side ="right", padx =5)

        self.delete_button = tk.Button(self.frame_sup,relief ="groove" ,
                        font = "Calibri 10", cursor = "hand2", text = "ELIMINAR",
                                command = self.eliminar_contratacion)
        self.delete_button.pack(side ="right", padx =5)

    def ocultar_frame_2(self):
        self.frame_1.pack_forget()        
        self.dispo_ajd_main.frame.pack(fill ="both", expand = 1, side= "top")

    def abrir_plantilla(self):
        os.startfile(f"templates\DISPOADJUDICACION_CME.docx")

    def eliminar_contratacion(self):
        contratacion_seleccionada = self.arbol.element_clicked()[0]
        admin_json.eliminar_contratacion(contratacion_seleccionada)
        self.write_rows_tree()

    def write_rows_tree(self):
        values = admin_json.open_json(admin_json.file)
        # contrataciones = [list(x.keys())[0] for x in values]
        lista = []

        for proceso in values:
            contratacion = list(proceso.keys())[0] 
            detalle = proceso[contratacion]["detalle"].upper()

            lista.append([contratacion,detalle])

        self.arbol.write_rows(lista)

if __name__== "__main__":
    root = tk.Tk()
    ventana = Main(root)
    ventana.frame.pack(fill ="both", expand=1)
    root.mainloop()