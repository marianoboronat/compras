import tkinter as tk
from tkinter import ttk
import widgets

from docxtpl import DocxTemplate


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
        self.parent = parent


        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        self.config = widgets.ConfigFrame(self.frame)

        self.main_frame = ttk.LabelFrame(self.frame, text = "Generar Disposicion de llamado", padding=10 )
        self.main_frame.pack(fill = "x")



        # widgets        
        self.ley = widgets.TagsAndEntry(self.main_frame,"Ley",5,0)
        self.ley.data.set("6.588")
        self.ley_bloc = BlockButton(self.main_frame, 5,3,self.ley)

        self.anio = widgets.TagsAndEntry(self.main_frame,"Año",10,0)
        self.anio.data.set("2023")
        self.anio_bloc = BlockButton(self.main_frame, 10,3,self.anio)

        self.detalle = widgets.TagsAndEntry(self.main_frame,"detalle",20,0)
        # self.detalle.entry.config()
        self.expediente_electronico = widgets.TagsAndEntry(self.main_frame,"Expediente Electrónico",30,0)
        self.numero_proceso = widgets.TagsAndEntry(self.main_frame,"N° de Proceso",40,0) 
        self.solicitud_gasto = widgets.TagsAndEntry(self.main_frame,"Solicitud de Gasto",50,0)
        self.numero_pliego = widgets.TagsAndEntry(self.main_frame,"Numero Pliego",60,0)
        self.precio = widgets.TagsAndEntry(self.main_frame,"Precio(con puntos y comas)",65,0)
        self.precio_a_letras = widgets.TagsAndEntry(self.main_frame,"Precio en letras",70,0)
        self.fecha_recepcion = widgets.FechaDividido(self.main_frame, "Fecha de Recepcion", 80,0)
        self.fecha_recepcion.frame_main.grid(columnspan = 3)
        self.submit = ttk.Button(self.main_frame, cursor = "hand2", text = "Crear Dispocicion Llamado",
                                     command = self.get_data)
        self.submit.grid(column = 0, row = 99, columnspan = 3)


        self.context = {
            "ley":None,
            "anio":None,
            "anio_dos_cifras":None,
            "detalle":None,
            "expediente_electronico":None,
            "numero_proceso":None,
            "numero_pliego":None,
            "solicitud_gasto":None,
            "precio":None,
            "precio_a_letras":None,
            
            "fecha_recepcion_dia":None,
            "fecha_recepcion_mes":None,
            "fecha_recepcion_anio":None,


            }


    def get_data(self):
        self.context["ley"] = self.ley.get()
        self.context["anio"] = self.anio.get()
        self.context["anio_dos_cifras"] = self.anio.get()[2:]

        self.context["detalle"] = self.detalle.get()
        self.context["expediente_electronico"] = self.expediente_electronico.get()
        self.context["numero_proceso"] = self.numero_proceso.get()
        self.context["solicitud_gasto"] = self.solicitud_gasto.get()
        self.context["precio"] = self.precio.get()
        self.context["precio_a_letras"] = self.precio_a_letras.get().upper()
        self.context["numero_pliego"] = self.numero_pliego.get()
        self.context["fecha_recepcion_dia"] = self.fecha_recepcion.get()[0]
        self.context["fecha_recepcion_mes"] = self.fecha_recepcion.get()[1].upper()
        self.context["fecha_recepcion_anio"] = self.fecha_recepcion.get()[2]
        
        print(self.context)
        self.create_document()

    def create_document(self):
        document = DocxTemplate("templates/DISPOLLAMADO_CME.docx")
        document.render(self.context)
        document.save(f"DISPOSICIONLLAMADO-455-{self.context['numero_proceso']}-CME{self.context['anio_dos_cifras']}.docx")


if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
    print("holas")
