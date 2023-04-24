import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json
import os, getpass as gt

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate 
import widgets,pliego,publicacion,disposicion_llamado, dispocision_adjudicacion as da

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
        self.disposicion_adjudicacion = da.Main(self.frame_right)

       
        self.blank_frame = tk.Frame(self.frame_right, width=500,height=500)
        self.blank_frame.pack(fill = "both", expand = 1)

        self.blank_label = tk.Label(self.blank_frame, text ="Elija un documento", pady = 200, padx = 200)
        self.blank_label.pack(fill = "both", expand=1)

        self.options_dict = {
            "PUBLICACION":self.frame_publicacion,
            "PLIEGO":self.frame_pliego,
            "DISPOSICION DE LLAMADO":self.disposicion_llamado,
            "DISPOSICION DE ADJUDICACION": self.disposicion_adjudicacion
            }


        # arbol de opciones 
        self.arbol = ttk.Treeview(self.frame_left)     

        # set para el arbol de opciones 
        self.arbol.pack(side = "left", fill = "y")
        self.arbol.bind('<ButtonRelease-1>', self.select_item)



        
        self.arbol.column("#0",width = 280) #Omitir la columna fantasma.
        self.arbol.heading("#0", text="opciones".capitalize())

        self.create_rows()

        self.hide_frames()


    def create_rows(self):
        """create the tree's row"""
        count = 0 
        for options in self.options_dict:
            count += 1
            print(options, count)
            self.main_value = self.arbol.insert(parent = "",  index = tk.END, iid = count, text = options )

    def hide_frames(self):
        """hide all frames created"""
        try:
            for frames  in self.options_dict:
                self.options_dict[frames].frame.pack_forget()
        except:
            print("ERROR")

    def show_frame(self, frame):
        """show just a frame"""
        frame.frame.pack(fill = "both", expand = 1)

    def select_item(self, a):   # added self and a (event)
        """select a row"""
        try:
            test_str_library = self.arbol.item(self.arbol.selection())["text"]
            print(test_str_library)
            self.blank_frame.pack_forget()
            self.hide_frames()
            self.show_frame(self.options_dict[test_str_library])
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
    root.title("Compras")
    # root.state("zoomed")
    root.mainloop()
