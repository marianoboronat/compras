#crea las sub ventanas del comparador de precios.
import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json
import os, getpass as gt
import widgets, tree



class WindowDescription:
    def __init__(self,parent, texto):
        self.parent = parent
        self.parent.title("Descripción")
        self.texto = texto
        
        #raiz de la ventana
        self.frame = tk.LabelFrame(self.parent, text ="Descripción")
        self.frame.pack(fill = "both", expand=1, padx = 5, pady =5)
        
        self.descripcion = tk.Text(self.frame,
                                    font="Calibri 12",
                                    width = 50,
                                    height=10,
                                    bd= 3,
                                    relief = "groove")
        
        self.descripcion.pack(fill = "both", expand=1, padx = 5, pady =5)
        self.descripcion.insert(tk.END,self.texto )

class TreeDescription:
    def __init__(self,parent, head, rows):
        self.parent = parent
        self.parent.title("Descripción")
        self.head = head
        self.rows = rows
        
        #raiz de la ventana
        self.frame = tk.LabelFrame(self.parent, text ="Descripción")
        self.frame.pack(fill = "both", expand=1, padx = 5, pady =5)

        self.tree = tree.TreeviewData(self.frame)
        self.tree.head(self.head)
        self.tree.write_rows(self.rows)
        


if __name__ == "__main__":
    root = tk.Tk()

    frame = WindowDescription(root ,"Ya no sentís una vergüenza encima?\nHola")
    # frame.title("COMPRA-MASTER")
    root.mainloop()

