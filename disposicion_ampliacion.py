import tkinter as tk
from tkinter import ttk, messagebox
import widgets
import webbrowser
import os

from docxtpl import DocxTemplate
import datetime
import read_excel as xl
import tree,generar_texto

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

class Renglones:
    def __init__(self, parent):
        # parameters
        self.parent = parent

        # frames
        self.frame = tk.LabelFrame(self.parent, text ="Renglones")
        self.frame.pack(fill = "x", padx = 5, pady = 5)

        self.frame_top = tk.Frame(self.frame)
        self.frame_top.pack(fill = "x", padx = 5, pady = 5)

        self.frame_buttom = tk.Frame(self.frame)
        self.frame_buttom.pack(fill = "x", padx = 5, pady = 5)

        # widgets
        self.data_renglon = tk.StringVar()

        self.entrada = ttk.Entry(self.frame_top, textvariable = self.data_renglon)
        self.entrada.pack(side = "left", anchor="n")
        self.entrada.bind("<Return>",lambda x: self.agregar_renglon())
        
        self.add = ttk.Button(self.frame_top,text ="Agregar",command = self.agregar_renglon)
        self.add.pack(side = "left", anchor="n")
        
        self.eliminar_renglon = ttk.Button(self.frame_top,text ="Borrar",command = self.borrar_renglon)
        self.eliminar_renglon.pack(side = "left", anchor="n")

        self.tree = tree.TreeviewData(self.frame_buttom)
        self.tree.tree.pack(expand=0,fill = "x")
        self.tree.head(["Renglones"])
        self.tree.tree.pack(side = "bottom", anchor="s")
        self.count =0

        # self.submit = tk.Button(self.frame_buttom, text ="submit", command = self.get_values)
        # self.submit.pack()

        self.lista = []


    def limpiar(self):
        self.tree.reset_tree()
        self.lista.clear()

    def get_values(self):
        # self.lista.sort()
        renglones = self.generar_conjunto_de_renglones(self.lista)
        print(renglones)
        return renglones


    def agregar_renglon(self):
        self.count +=1
        data = self.data_renglon.get()
        if data !="":
            self.lista.append(data)

            self.tree.write_rows(self.lista)
            self.entrada.focus()
            self.data_renglon.set("")
            print(f"agregar renglon {data}", self.count)
        else:
            print("")
    
    def borrar_renglon(self):
        multiple = self.tree.element_clicked()
        self.lista.remove(multiple[0])
        self.tree.reset_tree()
        self.tree.write_rows(self.lista)
        # print("borrar renglon")

    
    def generar_conjunto_de_renglones(self,lista):
        """genera una parte del texto para escribir un conjunto de renglones
        ej: 'para los renglones 1, 2 ,3, 4 y 5'"""
        cantidad_renglones = len(lista)
        # lista.sort()

        txt = ""
        count_cantidad = 0
        #si la lista solo tiene mas de un item
        if cantidad_renglones >1:
            for renglon in lista: 
                count_cantidad +=1
                if count_cantidad == cantidad_renglones:                
                    txt +=  "y "+str(renglon)
                elif count_cantidad == cantidad_renglones-1:
                    txt +=  str(renglon)+" "
                else:
                    txt +=  str(renglon)+", "

        #si la lista solo tiene un item        
        elif cantidad_renglones == 1:
            
            txt +=  "para el renglón "+str(lista[0])+"; "
        # print("texto:",txt)
        return txt


class MainWindow:
    def __init__(self, parent):
        # parameters
        self.parent = parent

        #propierties
        # get current date
        self.date_current = datetime.datetime.now()
        self.current_year = self.date_current.year
        self.parametros = widgets.open_json("bd/parametros.json")

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill = "x")
        
        self.info = widgets.InfoFrame(self.frame)        
        
        self.title_frame = widgets.HeadingFrame(self.frame, "Crear Disposición de Ampliación (CME)")

        #frames
        self.frame_sup = tk.Frame(self.frame, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame_sup.pack(side = "top", fill = "x")

        self.main_frame = ttk.Frame(self.frame, padding=10 )
        self.main_frame.pack(fill = "x")

        # widgets
        self.detalle = widgets.TagsAndEntry(self.main_frame,"Detalle",10,0)
        self.detalle.entry.config(width=42)
        self.detalle.entry.grid(columnspan = 99 )

        self.ex_electronico = widgets.DocumentoSade(self.main_frame,"N° Expediente","EX",15,0)
        self.ex_electronico.sub_frame.grid(columnspan = 99 )

        self.proceso_numero = widgets.NumeroBac(self.main_frame, "N° de Proceso","CME",20,0)
        self.proceso_numero.sub_frame.grid(columnspan = 99 )

        self.dispo_adjudicacion = widgets.DocumentoSade(self.main_frame,"N° Dispo. Adjudicacion","DISFC",25,0)
        self.dispo_adjudicacion.entry.config(width = 7)
        self.dispo_adjudicacion.sub_frame.grid(columnspan = 99 )

        self.oc_numero = widgets.NumeroBac(self.main_frame, "N° orden de compra","OC",30,0)
        self.oc_numero.sub_frame.grid(columnspan = 99 )

        self.fecha_perfeccionamiento = widgets.FechaDividido(self.main_frame, "fecha perfeccionamiento", 35,0)
        self.fecha_perfeccionamiento.frame_main.grid(sticky="w", columnspan =99)


        self.empresa = widgets.TagsAndEntry(self.main_frame,"Nombre Empresa",40,0)        
        self.cuit_empresa = widgets.TagsAndEntry(self.main_frame,"CUIT\n(sin guiones)",40,2)

        self.primer_precio = widgets.TagsAndEntry(self.main_frame,"Precio Original",50,0)
        self.primer_precio.entry.grid(columnspan = 99 )
        self.primer_precio.entry.config(width = 13)

        self.precio_a_letras = widgets.TagsAndEntryWithLink(self.main_frame,"en letras",50,2,
                                                            "https://www.letrasnumeros.com/")

        self.precio_ampliacion = widgets.TagsAndEntry(self.main_frame,"Precio ampliación",60,0)
        self.precio_ampliacion.entry.config(width = 13)
        self.precio_ampliacion_letras = widgets.TagsAndEntryWithLink(self.main_frame,"en letras",60,2,"https://www.letrasnumeros.com/")
        self.porcentaje_ampliacion  = widgets.TagsAndEntry(self.main_frame,"Porcentaje ampliación",70,0)
        self.porcentaje_ampliacion.entry.config(width = 7)

        self.renglones_frame = tk.Frame(self.main_frame)
        self.renglones_frame.grid(row = 80, column = 0, columnspan = 4, sticky="we")
        self.renglones = Renglones(self.renglones_frame) 

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

        self.context = None
        self.set_widgets()


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
                
                self.generate_file()
                self.info.success(f"se ingreso correctamente")
            except Exception as e:
                self.info.warning(f"hay un error: {e}")
                print(f"{e}")

    def get_data(self):        
        parametros = widgets.open_json("bd/parametros.json")
        fecha_perfec = self.fecha_perfeccionamiento.get()
        cuit = f"{self.cuit_empresa.get()[0:2]}-{self.cuit_empresa.get()[2:-1]}-{self.cuit_empresa.get()[-1]}"
        context = {
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

            "numero_proceso":self.proceso_numero.get(),
            "dis_adjudicacion":self.dispo_adjudicacion.get(),
            "orden_compra":self.oc_numero.get(),

            "nombre_empresa":self.empresa.get().upper(),
            "cuit_empresa":cuit,
            "precio_original":xl.agregar_comas_precio(float(self.primer_precio.get())),
            "precio_original_letras":self.precio_a_letras.get().upper(),

            "renglones":self.renglones.get_values(),

            "precio_ampliacion":xl.agregar_comas_precio(float(self.precio_ampliacion.get())),
            "precio_ampliacion_letras":self.precio_ampliacion_letras.get().upper(),
            "porcentaje_ampliacion":self.porcentaje_ampliacion.get(),

            # {dia} de {mes} del {año}
            "fecha_perfeccionamiento":f"{fecha_perfec[0]} de {fecha_perfec[1]} del {fecha_perfec[2]}",
            }

        return context

    def abrir_plantilla(self):
        os.startfile(f"templates\DISPOAMPLIACION_CME.docx")

    def generate_file(self):
        try: 
            context = self.get_data()
            document = DocxTemplate("templates/DISPOAMPLIACION_CME.docx")
            document.render(context)            
            name_path = f"{widgets.open_parameter('path_output')}"
            name_document = f"DISPOAMPLIACION{context['numero_proceso']}.docx"
            document.save(f"{name_document}")
            #abrir el documento automaticamente
            os.startfile(f"{name_document}")
            self.info.success(f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}")

            
            messagebox.showinfo(message=f"El documento '{name_document}' fue creado con exito\nen la carpeta {name_path}", title="Documento Creado")
        except Exception as e: 
            self.info.warning(f"Error: Hubo un Error al intentar crear el archivo\n{e}")

    def limpiar(self):
        print("limpiar entradas")
        self.detalle.limpiar()
        self.ex_electronico.limpiar()
        self.proceso_numero.limpiar()
        self.dispo_adjudicacion.limpiar()
        self.oc_numero.limpiar()
        self.fecha_perfeccionamiento.limpiar()
        self.primer_precio.limpiar()
        self.precio_a_letras.limpiar()
        self.empresa.limpiar()
        self.cuit_empresa.limpiar()
        self.precio_ampliacion.limpiar()
        self.precio_ampliacion_letras.limpiar()
        self.porcentaje_ampliacion.limpiar()
        self.renglones.limpiar()

        self.set_widgets()

    def set_widgets(self):
        parametros = widgets.open_json("bd/parametros.json")

        self.ex_electronico.data_reparticion.set(parametros["reparticion_siglas"])
        self.ex_electronico.data_anio.set(parametros["anio"])

        self.proceso_numero.data_anio.set(parametros["anio"][2:])
        self.proceso_numero.data_num_reparticion.set(parametros["reparticion_num"])

        self.oc_numero.data_anio.set(parametros["anio"][2:])
        self.oc_numero.data_num_reparticion.set(parametros["reparticion_num"])

        self.dispo_adjudicacion.data_anio.set(parametros["anio"])
        self.dispo_adjudicacion.data_reparticion.set(parametros["reparticion_siglas"])

        self.fecha_perfeccionamiento.data_year.set(parametros["anio"])

if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
