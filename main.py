import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json
import os, getpass as gt

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate 
import widgets,pliego,publicacion,disposicion_llamado
import dispo_ad_tree
import dictamen_adj, parametros
import evaluacion_ofertas, disposicion_ampliacion

class Main:
    def __init__(self, master):
        
        self.master =master
        self.color = "#F5C377"
        self.frame_sup = tk.Frame(self.master ,bg = self.color)
        self.frame_sup.pack(fill="x", side = "top")

        self.frame = tk.Frame(self.master )
        self.frame.pack(fill="both", expand = 1)

        self.titulo = tk.Label(self.frame_sup,font ="Calibri 14 bold",fg ="white",text ="CompraMaster", bg = self.color)
        self.titulo.pack(fill ="x", side = "left", padx = 5)

        self.main = Arbol(self.frame)
        self.main.pack()

class Arbol(ttk.Frame):
    def __init__(self, master, frame_class = None ):
        ttk.Frame.__init__(self, master)
        self.pack(side = "left", fill = tk.BOTH, expand= 1)
        
        # main frame
        self.frame_left = tk.Frame(self)
        self.frame_left.pack(side = "left", fill = "y", pady = 5, padx=5)

        self.frame_right = tk.Frame(self)
        self.frame_right.pack(side = "right", fill = "both", expand = 1, pady = 5, padx=5)

        # options frames 
        self.frame_publicacion = publicacion.Main(self.frame_right)
        self.frame_pliego = pliego.Main(self.frame_right)
        self.disposicion_llamado =  disposicion_llamado.MainWindow(self.frame_right)
        self.disposicion_adjudicacion = dispo_ad_tree.Main(self.frame_right)
        self.dictamen_adjudicacion = dictamen_adj.Main(self.frame_right)
        self.evaluador_ofertas = evaluacion_ofertas.Main(self.frame_right)
        self.dispo_ampliacion = disposicion_ampliacion.MainWindow(self.frame_right)


       
        self.blank_frame = tk.Frame(self.frame_right, width=500,height=500)
        self.blank_frame.pack(fill = "both", expand = 1)

        self.blank_label = tk.Label(self.blank_frame, text ="Elija un documento", pady = 200, padx = 200)
        self.blank_label.pack(fill = "both", expand=1)

        self.parameters_dict = {
            "PLIEGO":self.frame_pliego,
            "DISPOSICION DE LLAMADO":self.disposicion_llamado,
            "DICTAMEN DE LLAMADO":self.frame_publicacion,
            "DISPOSICION DE ADJUDICACION (beta)": self.disposicion_adjudicacion,
            "DICTAMEN DE ADJUDICACION (beta)": self.dictamen_adjudicacion,
            "COMPARAR OFERTAS": self.evaluador_ofertas,
            "DISPOSICION DE AMPLIACION":self.dispo_ampliacion
            }


        self.parameters =ttk.Button(self.frame_left,
                                    cursor="hand2",
                                    text ="parametros",
                                    command=self.open_parameters)
        self.parameters.pack(anchor="w")

        # arbol de opciones 
        self.arbol = ttk.Treeview(self.frame_left)     
        self.boton_ = HideShowButton(self.frame_left,
                                     self.arbol)
            
        # set para el arbol de opciones 
        self.arbol.pack(side = "left",
                        fill = "y")
        self.arbol.bind('<ButtonRelease-1>',
                        self.select_item)


        self.arbol.column("#0",width = 280) #Omitir la columna fantasma.
        self.arbol.heading("#0",
                           text="opciones".capitalize())

        self.create_rows()

        self.hide_frames()

    def open_parameters(self):
        """abre la sub ventana para los parametros grales"""
        sub_window = tk.Toplevel()
        sub_window.resizable(0,0)
        sub_window.title("Parametros Generales")
        sub_window.grab_set()

        parametros.Main(sub_window)



    def create_rows(self):
        """create the tree's row"""
        count = 0 
        for options in self.parameters_dict:
            count += 1
            print(options, count)
            self.main_value = self.arbol.insert(parent = "",  index = tk.END, iid = count, text = options )

    def hide_frames(self):
        """hide all frames created"""
        try:
            for frames  in self.parameters_dict:
                self.parameters_dict[frames].frame.pack_forget()
        except:
            print("ERROR")

    def show_frame(self, frame):
        """show just a frame"""
        frame.frame.pack(fill = "both", expand = 1)

    def update_frame(self,frame):
        """update the frame"""
        frame.update()

    

    def select_item(self, a):   # added self and a (event)
        """select a row"""
        try:
            test_str_library = self.arbol.item(self.arbol.selection())["text"]
            print(test_str_library)
            self.blank_frame.pack_forget()
            self.hide_frames()
            self.show_frame(self.parameters_dict[test_str_library])
            try:
                """intentar ejecutar la funcion 'update' en caso de que la tenga"""
                self.update_frame(self.parameters_dict[test_str_library])
            except Exception as e:
                print(e)

        except:
            self.blank_frame.pack(fill = "both", expand = 1)
            print("")


class HideShowButton:
    def __init__(self, parent, tree):
        # parameters
        self.parent = parent
        self.tree = tree

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side = "left", fill = "y")

        # button widget
        self.button_hide = tk.Button(self.frame, text = "◄",cursor="hand2",
                                    bd = 2,relief="groove", width=1, height=20,
                                    command= self.hidden_treeview)
        self.button_hide.pack(side = "left", fill = "y", padx = 3)

    def hidden_treeview(self):
        self.button_hide.config(command =self.show_treeview, text ="►" )
        self.tree.pack_forget()
    
    def show_treeview(self):
        self.button_hide.config(command =self.hidden_treeview, text ="◄" )
        self.tree.pack(side = "left", fill = "y")


if __name__ == "__main__":
    root = tk.Tk()
    datos = Arbol(root)
    root.title("COMPRA-MASTER")
    root.mainloop()
