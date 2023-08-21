import tkinter as tk
from tkinter import ttk,filedialog
import datetime, json
import os, getpass as gt

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from docxtpl import DocxTemplate 

#este modulo compara las ofertas presentadas por las empresas.

class Main:
    def __init__(self, master):
        
        self.master =master
        self.frame = tk.Frame(self.master )
        self.frame.pack(fill="both", expand = 1)

        self.label = tk.Label(self.frame,text="holas")

if __name__ == "__main__":
    root = tk.Tk()
    datos = Main(root)
    root.title("COMPRA-MASTER")
    root.mainloop()
