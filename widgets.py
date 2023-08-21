import tkinter as tk
from tkinter import Button, Frame, ttk, Canvas,Scrollbar,filedialog
from functools import partial
import json, webbrowser
# import nav_vertical_right as nvr
import datetime 
import pyperclip

NORMAL_FONT = "Calibri 12"
TITLE_FONT = "Calibri 18 bold"
parameters_file = "bd/parametros.json"

numero_letras = ["cero","una", "dos","tres","cuatro","cinco","seis","siete","ocho","nueve","diez",
                "once","doce","trece","catorce","quince","dieciséis","diecisiete", "dieciocho", "diecinueve",
                "veinte","veintiún","veintidós","veintitrés","veinticuatro","veinticinco","veintiséis","veintisiete","veintiocho","veintinueve",
                "treinta","treinta y un", "treinta y dos","treinta y tres", "treinta y cuatro", "treinta y cinco", "treinta y seis", "treinta y siete" ,"treinta y ocho", "treinta y nueve",
                "cuarenta", "cuarenta y un", "cuarenta y dos","cuarenta y tres", "cuarenta y cuatro", "cuarenta y cinco", "cuarenta y seis", "cuarenta y siete", "cuarenta y ocho", "cuarenta y nueve",
                "cincuenta", "cincuenta y un", "cincuenta y dos", "cincuenta y tres", "cincuenta y cuatro", "cincuenta y cinco", "cincuenta y seis", "cincuenta y siete", "cincuenta y ocho", "cincuenta y nueve",

                 ]


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def open_json(file):
    """abre los archivos json para su lectura"""
    with open(file,encoding='utf-8') as json_file: #ABRIR EL ARCHIVO	
        main_objeto = json.load(json_file ) #LA VARIABLE 'datos' ABRE EL OBJETO JSON DEL ARCHIVO 'json_file'
        return main_objeto
    
def open_parameter( parameter):
    return open_json("bd/parametros.json")[f'{parameter}']

def save_json(file,parametro, valor): #1er. ARG: EL NOMBRE DE ARCHIVO, 2do ARG: EL DATO QUE ABRE EL OBJETO PARA AGREGAR DATOS
    """escribe datos en el archivo json que se le asigne."""
    data = open_json(file)
    data[f"{parametro}"] = valor
    with open(file, "w") as outfile:
        json.dump(data, outfile, sort_keys = False, indent = 4)
        # outfile["parametros"][f"{parametro}"]

def numero_a_letras(numero):
    try:
        letra = numero_letras[int(numero)]
        print(letra)
        return letra
    except:
        print("agregar este numero a la lista de 'numero_letras' en widgets")

def convert_primera_letra_mayusc(texto):
    """convierte en mayuscula la primera letra de una palabra larga,
    excepto si la palabra es una de 'palabras_recurrentes'"""
    palabras_recurrentes = ["de", "del","y","e","a","al",
                            "para","su","sus","la", "las",
                            "en","con","el","los", ]
    palabras_recurrentes_cant = len(palabras_recurrentes)

    texto.lower()
    texto = texto.split(" ")
    txt = [""]


    for palabra in texto:
        print(palabra)
        count = 0
        for palabra_rec in palabras_recurrentes:
            count += 1
            print("\t",palabra_rec)
            if palabra ==palabra_rec:
                txt.append(palabra.lower())
                print(palabra.lower())
                break
            elif count == palabras_recurrentes_cant:                
                txt.append(palabra.capitalize())
                print(palabra.capitalize())
    txt = " ".join(txt)
    print(txt[1:])


def verify_all_entries(self, context, query):
    valid = 0
    for data in context:
        # print(f"{context[data]}")
        if context[data] == "":
            valid += 1

    if valid > 0:
        self.info.warning(f"error se deben llenar todas las entradas")
        print("error se deben llenar todas las entradas")
        return False
    else:
        try:
            self.info.success(f"se ingreso correctamente")
            set_data = query(context)
            self.clean()
            return True
        except Exception as e:
            self.info.warning(f"hay un error: {e}")
            print(f"{e}")
            return False


class SelectorFile:
    def __init__(self, parent, texto ,fila, columna):
        # parametros
        self.parent = parent
        self.texto = texto
        self.fila = fila
        self.columna = columna


        #frame
        self.frame = tk.Frame(self.parent, pady = 3)
        self.frame.grid(row = self.fila, column = self.columna, sticky="we")

        # widgets
        #widgets para la carga de exceles
        self.label = tk.Label(self.frame, text =self.texto, font = "Calibri 12" )
        self.label.grid(row = 0, column = 0)

        self.path_data = tk.StringVar()
        self.path = ttk.Entry(self.frame, textvariable=self.path_data,width=47, font = "Calibri 12" )
        self.path.grid(row = 0, column = 0+1)

        self.path_button = ttk.Button(self.frame, cursor = "hand2",width=6, text ="Abrir", command = self.open_file)
        self.path_button.grid(row = 0, column = 0+2)
    

    def open_file(self):
        self.directory = filedialog.askopenfile(title=f"{self.texto}")
        self.path_data.set(self.directory.name)

    def get(self):
        data = self.path_data.get()
        return data
        
class SubVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title = ""
        self.grab_set()

class NumeroBac:    
    def __init__(self, parent, texto, values, _row, _column ):
        """Genera un widget para objetos del BAC"""

        self.parent = parent
        self.texto = texto
        self.values = values
        self._row = _row
        self._column = _column

        # data
        self.data = tk.StringVar()
        self.data_num_reparticion = tk.StringVar()
        self.tipo_document = tk.StringVar()
        self.data_anio = tk.StringVar()

        # widgets

        self.label = ttk.Label(self.parent, cursor="hand2", text =self.texto+":", font = NORMAL_FONT)
        self.label.grid(row = self._row, column=self._column, sticky="e")
        self.label.bind("<Button-1>", lambda x: self.focus_entry())

        self.sub_frame = ttk.Frame(self.parent)
        self.sub_frame.grid(row = self._row, column=self._column+1, sticky="w", pady = 3, padx = 5)

        self.num_reparticion = ttk.Entry(self.sub_frame,width=6, textvariable = self.data_num_reparticion, font = NORMAL_FONT)
        self.num_reparticion.grid(row = 0, column=0)
        self.num_reparticion.bind('<Return>', self.button_tab )
        self.num_reparticion.bind('<Down>', self.button_tab )
        self.num_reparticion.bind('<Up>', self.button_previous_tab )  

        self.label_guion_1 = ttk.Label(self.sub_frame, text ="-", font = NORMAL_FONT)
        self.label_guion_1.grid(row = 0, column=1)

        self.entry = ttk.Entry(self.sub_frame,width=6, textvariable = self.data, font = NORMAL_FONT)
        self.entry.grid(row = 0, column=2)
        self.entry.bind('<Return>', self.button_tab )
        self.entry.bind('<Down>', self.button_tab )
        self.entry.bind('<Up>', self.button_previous_tab )  

        self.label_guion_2 = ttk.Label(self.sub_frame, text ="-", font = NORMAL_FONT)
        self.label_guion_2.grid(row = 0, column=3)

        self.siglas_tipo = ttk.Combobox(self.sub_frame,
                                    values = self.values, 
                                    textvariable=self.tipo_document,
                                    state="readonly",
                                    width = 7,
                                    font = NORMAL_FONT)
        self.siglas_tipo.grid(row = 0, column=4)

        self.anio = ttk.Entry(self.sub_frame,width=3, textvariable = self.data_anio, font = NORMAL_FONT)
        self.anio.grid(row = 0, column=5, padx = 5)
        self.anio.bind('<Return>', self.button_tab )
        self.anio.bind('<Down>', self.button_tab )
        self.anio.bind('<Up>', self.button_previous_tab )  


    def focus_entry(self):
        try:
            pyperclip.copy(f"{self.get()}")
            self.entry.focus()
        except:
            print("La entrada de texto fue destruida")

    def button_previous_tab(self, event):    
        self.parent.event_generate('<Shift-Tab>')

    def button_tab(self, event):    
        self.parent.event_generate('<Tab>')

    def get(self):
        """obtiene los datos de las 3 entradas"""
        data = self.data.get()
        reparticion = self.data_num_reparticion.get()
        anio = self.data_anio.get()
        tipo_document = self.tipo_document.get()
        result = f"{reparticion}-{data}-{tipo_document}{anio}"
        print(result)
        return result

    def limpiar(self):
        self.data.set("")
        self.data_num_reparticion.set("")
        self.data_anio.set("")


    def disabled(self):
        self.label.config(state="disabled")
        self.num_reparticion.config(state="disabled")
        self.label_guion_1.config(state="disabled")
        self.entry.config(state="disabled")
        self.label_guion_2.config(state="disabled")
        self.siglas_tipo.config(state="disabled")
        self.anio.config(state="disabled")
    def item_default(self, item_lista):
        pass

class NumeroContratacion(NumeroBac):
    def __init__(self):
        super().__init__(parent, texto, tipo_document, _row, _column )
        self.label_guion_2 = ttk.Combobox(self.parent, "")

class DocumentoSade:
    def __init__(self, parent, texto, tipo_document, _row, _column ):

        """GENERA UN WIDGET PARA OBJETOS DEL SADE
        texto: el texto que ira en el label
        tipo_document: el tipo de Documento SADE """

        # parametros
        self.parent = parent 
        self.texto = texto 
        self.tipo_document = tipo_document 
        self._row = _row 
        self._column = _column 

        # data
        self.data = tk.StringVar()
        self.data_anio = tk.StringVar()
        self.data_reparticion = tk.StringVar()

        # widgets
        self.label = tk.Label(self.parent,cursor="hand2", text =self.texto+":", font = NORMAL_FONT)
        self.label.grid(row = self._row, column=self._column, sticky="e")        
        self.label.bind("<Button-1>", lambda x: self.focus_entry())

        self.sub_frame = tk.Frame(self.parent)
        self.sub_frame.grid(row = self._row, column=self._column+1, sticky="w", pady = 3, padx = 5)

        self.label_document = tk.Label(self.sub_frame, text =self.tipo_document+"-", font = NORMAL_FONT)
        self.label_document.grid(row = 0, column=0)

        self.anio = ttk.Entry(self.sub_frame,width=6, textvariable=self.data_anio, font = NORMAL_FONT)
        self.anio.grid(row = 0, column=1)
        self.anio.bind('<Return>', self.button_tab )
        self.anio.bind('<Down>', self.button_tab )
        self.anio.bind('<Up>', self.button_previous_tab )  

        self.label_guion_1 = tk.Label(self.sub_frame, text ="-", font = NORMAL_FONT)
        self.label_guion_1.grid(row = 0, column=2)

        self.entry = ttk.Entry(self.sub_frame, width=14, textvariable = self.data, font = NORMAL_FONT)
        self.entry.grid(row = 0, column=3)
        self.entry.bind('<Return>', self.button_tab )
        self.entry.bind('<Down>', self.button_tab )
        self.entry.bind('<Up>', self.button_previous_tab )  

        self.label_guion_2 = tk.Label(self.sub_frame, text ="-GCABA-", font = NORMAL_FONT)
        self.label_guion_2.grid(row = 0, column=4)

        self.reparticion_id = ttk.Entry(self.sub_frame, width=7, textvariable = self.data_reparticion, font = NORMAL_FONT)
        self.reparticion_id.grid(row = 0, column=5)
        self.reparticion_id.bind('<Return>', self.button_tab )
        self.reparticion_id.bind('<Down>', self.button_tab )
        self.reparticion_id.bind('<Up>', self.button_previous_tab )  


    # event
    def focus_entry(self):
        try:
            pyperclip.copy(f"{self.get()}")
            self.entry.focus()
        except:
            print("La entrada de texto fue destruida")


    def button_previous_tab(self, event):    
        self.parent.event_generate('<Shift-Tab>')

    def button_tab(self, event):    
        self.parent.event_generate('<Tab>')

    # methods
    def limpiar(self):
        self.data.set("")
        self.data_anio.set("")
        self.data_reparticion.set("")

    def get(self):
        """obtiene los datos de las 3 entradas"""
        data = self.data.get()
        reparticion = self.data_reparticion.get()
        anio = self.data_anio.get()
        return f"{self.tipo_document}-{anio}-{data}-GCABA-{reparticion}"
   


    def disabled(self):
        self.label.config(state="disabled")
        self.label_document.config(state="disabled")
        self.anio.config(state="disabled")
        self.label_guion_1.config(state="disabled")
        self.entry.config(state="disabled")
        self.label_guion_2.config(state="disabled")
        self.reparticion_id.config(state="disabled")

    def enabled(self):
        self.label.config(state="normal")
        self.label_document.config(state="normal")
        self.anio.config(state="normal")
        self.label_guion_1.config(state="normal")
        self.entry.config(state="normal")
        self.label_guion_2.config(state="normal")
        self.reparticion_id.config(state="normal")

class Pagination:
    def __init__(self, parent, frame_list):
        #parameters
        self.parent = parent
        self.frame_list = frame_list

        self.frame = tk.Frame(self.parent, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame.pack(side = "top", fill = "x")

        self.frame_main = tk.Frame(self.parent, bg = "#B6B6B6", padx = 5, pady= 5)
        self.frame.pack(side = "top", fill = "x")

        self.before_button = tk.Button(self.frame, text ="◄ Anterior", cursor = "hand2", command = self.before_frame)
        self.before_button.pack(side ="left")

        self.next_button = tk.Button(self.frame, text ="Siguiente ►", cursor = "hand2", command = self.next_frame)
        self.next_button.pack(side ="left")

        # for frame in self.frame_list:
        #     frame(self.frame)

        self.hide_frame()
        self.numero_frame = 0
        self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)


    def next_frame(self):            
        try:
            self.numero_frame += 1
            if self.numero_frame > len(self.frame_list)-1:
                self.numero_frame =len(self.frame_list)-1
            else:
                self.hide_frame()
                self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)
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
                self.frame_list[self.numero_frame].frame.pack(fill="both", expand =1)
                print("frame anterior", self.numero_frame)
        except Exception as e:
            print(e)

    def hide_frame(self):
        for frame in self.frame_list:
            frame.frame.pack_forget()

class InfoFrame:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="x")

        self.label = tk.Label(self.frame,font = "Calibri 10", text ="")
        self.label.pack(fill = "x")
    
    def thread(self):
        pass


    def warning(self, texto):
        # print(f"Peligro: {texto}")
        self.frame.config(bg = "#CA6161")
        self.label.config(bg = "#CA6161", fg= "white", text =texto)
    def success (self, texto):
        # print("")        
        self.frame.config(bg = "#44C190")
        self.label.config(bg = "#44C190", fg= "black", text =texto)
    def info(self, texto):
        # print(f"ⓘ Info: {texto}")
        self.frame.config(bg = "#CDCDCD")
        self.label.config(bg = "#CDCDCD", fg= "black", text =f"ⓘ Info: {texto}")

class ConfigFrame:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        self.frame = tk.LabelFrame(self.parent, text ="Config ", padx = 5, pady =5)
        self.frame.pack(fill = "x")

        # self.file_template = PathSelector(self.frame, "Plantilla", 10, 0, "file_template")
        self.file_output = PathSelector(self.frame, "Destino del archivo", 20, 0, "path_output")
    
class FechaDividido:
    def __init__(self, parent, texto, _row, _column ):
        
        # parameters
        self.parent = parent
        self.texto = texto
        self._row = _row
        self._column = _column

        self.MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

        self.data_day = tk.StringVar()
        self.data_month = tk.StringVar()
        self.data_year = tk.StringVar()


        self.fecha_consulta_label = tk.Label(self.parent,cursor="hand2", text = f'{self.texto}:', font = NORMAL_FONT)
        self.fecha_consulta_label.grid(row = self._row, column = self._column,padx = 5, sticky="e")      
        self.fecha_consulta_label.bind("<Button-1>", self.focus_entry)

        self.frame_main = tk.Frame(self.parent)
        self.frame_main.grid(row = self._row, column = self._column+1,sticky="w")


        self.dia_consultas = ttk.Entry(self.frame_main, width=3, font = NORMAL_FONT, textvariable=self.data_day)
        self.dia_consultas.grid(column =10 ,row =0 ,padx = 5)
        self.dia_consultas.bind('<Return>', self.button_tab )
        self.dia_consultas.bind('<Down>', self.button_tab )
        self.dia_consultas.bind('<Up>', self.button_previous_tab )

        self.delimitador_1 = tk.Label(self.frame_main, text = "/", font = NORMAL_FONT)
        self.delimitador_1.grid(column = 20,row =0,padx = 5)
        
        self.mes_consultas = TagsAndOptions(self.frame_main,"",0,30,self.MESES) 
        self.mes_consultas.label.config(text = "")
        self.mes_consultas.desplegable.config(width=10)     
        self.mes_consultas.desplegable.bind('<Return>', self.button_tab )
        self.mes_consultas.desplegable.bind('<Down>', self.button_tab )
        self.mes_consultas.desplegable.bind('<Up>', self.button_previous_tab )

        self.delimitador_2 = tk.Label(self.frame_main, text = "/", font = NORMAL_FONT)
        self.delimitador_2.grid(column =40 ,row =0 ,padx = 5)
        self.anio_consultas = ttk.Entry(self.frame_main, width=6, font = NORMAL_FONT, textvariable=self.data_year)
        self.anio_consultas.grid(column =50 ,row =0 ,padx = 5)
        self.anio_consultas.bind('<Return>', self.button_tab )
        self.anio_consultas.bind('<Down>', self.button_tab )
        self.anio_consultas.bind('<Up>', self.button_previous_tab )
        self.anio_consultas.bind('<Right>', self.button_tab )
        self.anio_consultas.bind('<Left>', self.button_previous_tab )
        
        


    # events
    def focus_entry(self,event):
        self.dia_consultas.focus()

    def button_previous_tab(self, event):    
        self.parent.event_generate('<Shift-Tab>')

    def button_tab(self, event):    
        self.parent.event_generate('<Tab>')

    # methods
    def disabled(self):
        self.dia_consultas.config(state = "disabled")
        self.mes_consultas.disabled()
        self.anio_consultas.config(state = "disabled")

    def limpiar(self):
        self.data_day.set("")
        self.mes_consultas.data.set("")
        self.data_year.set("")

    def button_tab(self, event):    
        self.parent.event_generate('<Tab>')
    
    def get_fecha_numeros(self, delimiters):
        get_day = self.data_day.get()
        get_month = self.mes_consultas.get()
        get_year = self.data_year.get()
        try:
            print(self.MESES.index(get_month))
            return f"{get_day}{delimiters}{str(self.MESES.index(get_month)+1)}{delimiters}{get_year}"
        except Exception as e:
            print(e, "ERROR: Mal cargado el mes// widgets.FechaDividido.get_fecha_numeros()")

    def get(self):
        get_day = self.data_day.get()
        get_month = self.mes_consultas.get()
        get_year = self.data_year.get()
        return [get_day, get_month, get_year]

class BotonesOpciones:
    """botones de opciones para las CRUDs"""
    def __init__(self, parent, texto, comando ):
        # parameters
        self.parent = parent
        self.texto = texto
        self.comando = comando

        #widgets
        self.boton_opciones = tk.Button(parent, font = "Calibri 14",padx=15,
                                         bd = 1,fg = "white" , bg = "gray",
                                        text = texto, command = comando)
        self.boton_opciones.pack(side = "left", padx = 3)

        #events
        self.boton_opciones.bind('<Return>', lambda x: parent.event_generate('<Tab>'))
        self.boton_opciones.bind("<Enter>",self.enter )
        self.boton_opciones.bind("<Leave>",self.leave )
    # eventos
    def enter(self, event):
        self.boton_opciones.config(bg = "#a5a5a5", fg = "black", cursor="hand2")
    def leave(self, event):
        self.boton_opciones.config(bg = "gray", fg ="white")

class OptionFrame:
    """clase para generar una barra superior de opciones para cualquier frame
    ya sea modificar, eliminar, crear, imprimir etcetera."""
    def __init__(self,parent, dict_options):
        # parametros
        self.parent = parent
        self.dict_options = dict_options

        # frames
        self.buttons_frame = tk.Frame(self.parent, bg = "gray",padx = 10, pady = 5)
        self.buttons_frame.pack(side = "top", fill = "x")

        for text in self.dict_options:
            BotonesOpciones(self.buttons_frame,text.capitalize(), self.dict_options[text] )

class Ventana:
    def __init__(self, root):
        self.root = root

        # frames
        self.main_frame = Frame(root)
        self.main_frame.pack()

        self.escrol = ScrollbarFrame(self.main_frame)

        for x in range(100):
            tag = tk.Label(self.escrol.inside_frame,text = f"label {x}")
            tag.pack(fill = "x")

class ScrollbarFrame:
    def __init__(self,parent):
        # paremeters
        self.parent = parent

        # create a canvas
        self.canvas_main = tk.Canvas(self.parent)
        self.canvas_main.pack(side = "left", fill="both", expand=1)

        # create the scrollbar
        self.scrollbar = Scrollbar(self.parent, orient=tk.VERTICAL, command=self.canvas_main.yview)
        self.scrollbar.pack(side = "right", fill="y")

        # configure the canvas
        self.canvas_main.configure(yscrollcommand= self.scrollbar.set)
        self.canvas_main.bind("<Configure>",self.scroll_update)

        self.inside_frame = tk.Frame(self.canvas_main, pady=30, width=300)        
        self.canvas_main.create_window((0,0), window=self.inside_frame, anchor = "nw")

    def scroll_update(self, event):
        self.canvas_main.configure(scrollregion=self.canvas_main.bbox("all"))
        self.canvas_main.yview_moveto('1.0')
        # self.inside_frame.pack(fill="x")

class HeadingFrame:
    """cabecera para los todos los frames.
    esta integrado por un label en negrita y un separador."""

    def __init__(self, parent, text):
        #parameters
        self.parent = parent 
        self.text = text 

        #frames
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill = "x",pady = 5, padx = 10)

        # widgets
        self.title = ttk.Label(self.frame, font = "calibri 18 bold", text =f"{self.text}")        
        self.title.pack( anchor = "w" )

        self.separator = ttk.Separator(self.frame,orient= tk.HORIZONTAL)
        self.separator.pack(expand = True, fill = "x")

class TextArea:
    def __init__(self,parent, text_, alto):
        # parameters
        self.parent = parent
        self.text_ = text_
        self.alto = alto

        #textVariable
        self.data = tk.StringVar()

        # widgets
        self.label = tk.Label(self.parent, text = text_)
        self.label.pack()

        self.textarea = tk.Text(self.parent, height = self.alto, bd =2,
                                relief ="groove", font= "Calibri 12")
        self.textarea.pack(fill = "x", pady = 5, padx = 5)
        self.textarea.bind("<Control-BackSpace>",lambda x:  self.clean())

    def set_(self, texto):
        self.textarea.insert(tk.INSERT, texto)

    def get(self):
        self.textarea.get("1.0",'end-1c')

    def clean(self):
        # permite limpiar la entry de texto presionando control-suprimir
        self.textarea.delete(1.0, tk.END)

    def deshabilitar(self):
        self.textarea.config(state = "disabled")

class TagsAndEntry:
    """etiqueta y entry para cruds"""
    def __init__(self, parent, text_, row_, column_, focus=False):        
        # parameters
        self.parent = parent
        self.text_ = text_
        self.row_ = row_
        self.column_ = column_
        self.focus = focus

        # properties
        self.info_text = ""
        self.info_frame = None
        
        # tipos de datos
        self.data = tk.StringVar()

        # widgets
        self.label = ttk.Label(self.parent, text = self.text_+": ",cursor="hand2", font = NORMAL_FONT)
        self.label.grid(row = self.row_, column = self.column_, sticky="e")
        self.label.bind("<Button-1>", lambda x: self.focus_entry())
        self.label.bind("<Enter>", self.label_enter)
        self.label.bind("<Leave>", self.label_leave)

        self.entry = ttk.Entry(self.parent, width = 23,font = NORMAL_FONT, textvariable = self.data)
        self.entry.grid(row = self.row_, column = self.column_ + 1, pady = 3, sticky="w")
        
        self.entry.bind("<Enter>", self.label_enter)
        self.entry.bind("<Leave>", self.label_leave)
        self.entry.bind('<Return>', self.button_tab )
        self.entry.bind('<Down>', self.button_tab )
        self.entry.bind('<Up>', self.button_previous_tab )     
        if self.focus == True:
            self.entry.focus()    

    # events 

    def label_enter(self,e):
        try:
            self.info_frame.info(self.info_text)
        except:
            pass

    def label_leave(self,e):
        try:
            self.info_frame.label.config(text ="")
        except:
            pass


    def focus_entry(self):
        try:
            self.entry.focus()
            pyperclip.copy(f"{self.get()}")
        except:
            print("La entrada de texto fue destruida")

    def button_previous_tab(self, event):
        self.parent.event_generate('<Shift-Tab>')

    def button_tab(self, event):
        self.parent.event_generate('<Tab>')

    # metodos
    def limpiar(self):
        # permite limpiar la entry de texto presionando control-suprimir
        self.data.set("")

    def get(self):
        data = self.data.get()
        return data 

    def disabled(self):
        try:
            self.label.config(state = "disabled")
        except:
            pass
        self.entry.config(state = "disabled")

    def enable(self):
        self.label.config(state= "enabled")
        self.entry.config(state= "enabled")

class TagsAndEntryWithLink(TagsAndEntry):
    def __init__(self,parent, text_, row_,column_, _url):
        super().__init__(parent, text_, row_,column_)
        self.url = _url
        # self.label.config(command = lambda: self.link(self.url))
        self.info_frame = None
        self.info_text = ""

        self.label = tk.Label(self.parent, text = self.text_+": ",cursor="hand2",fg = "blue", font = NORMAL_FONT)
        self.label.grid(row = self.row_, column = self.column_, sticky="e")

        self.label.bind("<Button-1>", self.press)
        self.label.bind("<Enter>", self.label_enter)
        self.label.bind("<Leave>", self.label_leave)

    
    def press(self, e):
        webbrowser.open(self.url)

    def enter(self, e):
        self.label.config(fg = "#A9A9A9")
        # pass

    def leave(self, e):
        self.label.config(fg = "blue")
        # pass

    def disabled(self):
        
        self.label.config(state = "disabled")
        self.entry.config(state = "disabled")

    def enable(self):
        self.label.config(state= "normal")
        self.entry.config(state= "normal")

class TagsAndEntryBlock(TagsAndEntry):
    def __init__(self, parent, text_, row_, column_ , block = False):
        TagsAndEntry.__init__(self,parent, text_, row_, column_)
        self.block = block
        
        self.block_button = ttk.Button(self.parent, text ="block",cursor="hand2", command=self.block_entry)
        self.block_button.grid(column = column_+2,row = row_, sticky="w")

        self.block_entry()

    def block_entry(self):
        if self.block == False:
            self.enable()
            print("bloqueado")
            self.block = True
        elif self.block == True:
            self.disabled()
            self.block = False
            print("desbloqueado")

class PathSelector(TagsAndEntry):
    def __init__(self, parent, text_, row_, column_, parametro ):
        self.parametro = parametro
        TagsAndEntry.__init__(self,parent, text_, row_, column_)

        self.data.set(open_json("bd/parametros.json")[self.parametro])
        
        self.entry.config(width=47, font = "Calibri 12")
        self.block_button = tk.Button(self.parent, text ="path", command = lambda: self.path(self.parametro))
        self.block_button.grid(column = column_+2,row = row_, padx = 5)


    def path(self,parametro):
        parametro_valor = open_json("bd/parametros.json")
        print(parametro_valor[f"{parametro}"]) 
        self.directory = filedialog.askdirectory(title=f"{self.text_}")#, initialdir=f"{parametro_valor}")
        self.data.set(self.directory)
        save_json("bd/parametros.json",f"{parametro}",f"{self.directory}")
        
        self.data.set(open_json("bd/parametros.json")[self.parametro])

class FileSelector(TagsAndEntry):
    def __init__(self, parent, text_, row_, column_, parametro ):
        self.parametro = parametro
        TagsAndEntry.__init__(self,parent, text_, row_, column_)

        self.data.set(open_json("bd/parametros.json")["parametros"][self.parametro])
        self.entry.config(width=47, font = "Calibri 12")
        self.entry.grid(sticky = "we")
                
        self.block_button = tk.Button(self.parent, text ="path", command = lambda: self.path(self.parametro))
        self.block_button.grid(column = column_+2,row = row_, padx = 5)
    

    def path(self,parametro):
        parametro_valor = open_json("bd/parametros.json")
        print(parametro_valor["parametros"][f"{parametro}"]) 
        self.directory = filedialog.askopenfilename(title=f"{self.text_}")#, initialdir=f"{parametro_valor}")
        self.data.set(self.directory)
        save_json("bd/parametros.json",f"{parametro}",f"{self.directory}")
        
        self.data.set(open_json("bd/parametros.json")["parametros"][self.parametro])

class TagsAndOptions:
    """ genera una etiqueta y un combobox para los formularios"""
    def __init__(self, parent, text_, row_, column_, list_options):
        # parameters
        self.parent = parent
        self.text_ = text_
        self.row_ = row_
        self.column_ = column_
        self.list_options = list_options

        # tipos de datos
        self.data = tk.StringVar()

        # widgets
        self.label = ttk.Label(self.parent, text = self.text_.capitalize()+":",cursor = "hand2", font = NORMAL_FONT)
        self.label.grid(row = self.row_, column = self.column_, sticky="e")
        self.label.bind("<Button-1>", self.focus_entry)
        # widgets
        self.desplegable = ttk.Combobox(self.parent,cursor="hand2",state="readonly",textvariable = self.data,
                                        width = 23,font = NORMAL_FONT,
                                        values = self.list_options)
        self.desplegable.grid( row = self.row_, column = self.column_+1, pady = 3, padx = 3)
        self.desplegable.bind('<Return>',self.entry_event)


    # events
    def focus_entry(self,event):
        self.desplegable.focus()

    def entry_event(self, event):
        self.get()
        self.parent.event_generate('<Tab>')

    # methods
    def disabled(self):
        self.desplegable.config(state="disabled")

    def get(self):
        data = self.data.get()
        return data

class RadialButton:
    def __init__(self, parent,text,row_, column_,list_options, orientation, column_span=1):
        # parameters
        self.parent = parent
        self.text = text
        self.row_ = row_
        self.column_ = column_
        self.list_options = list_options
        self.orientation = orientation.lower()
        self.column_span = column_span
        
        # list of instances objects
        self.objects_list = []
        # data type
        self.data = tk.IntVar()

        self.label_frame = ttk.LabelFrame(self.parent, text = f"{self.text}", padding = 5)
        self.label_frame.grid(row = self.row_, column = self.column_, columnspan=self.column_span,
                                pady = 5, padx = 5)

        self.count = 0
        for i in self.list_options:
            self.count +=1
            self.button = ttk.Radiobutton(self.label_frame,text = i, variable=self.data,cursor= "hand2", value=self.count)

            # add the radial buttons in the list objects
            self.objects_list.append(self.button)
            if self.orientation == "v":
                self.button.grid(row = self.count , column = 0)  
            elif self.orientation == "h":
                self.button.grid(row = 0 , column = self.count)
            else:
                print("la orientación asignada no es correcta")                
                self.button.grid(row = self.count , column = 0)  
        self.data.set(1)
        
        # adding a padding on each radialbutton 
        for x in self.objects_list:
            x["padding"] = 5
    
    def disabled_buttons(self):                
        for button in self.objects_list:
            button.config(state = "disabled",cursor= "" )

    def enabled_buttons(self):                
        for button in self.objects_list:
            button.config(state = "normal",cursor= "hand2" )
    
    def get(self):
        # print(self.data.get() )
        index = self.data.get()-1
        
        return self.data.get(), self.objects_list[index]["text"]

class TagsAndChecks:
    """ genera una etiqueta y un Chekboxes multiples para los formularios"""
    def __init__(self, parent, text_, row_, column_, list_options):
        # parameters
        self.parent = parent
        self.text_ = text_
        self.row_ = row_
        self.column_ = column_
        self.list_options = list_options


        # frame
        self.frame = tk.LabelFrame(self.parent,text = self.text_)
        self.frame.grid(row = self.row_,sticky = "we", column = self.column_,pady = 5, padx = 5)
        
        #se almacenan todas las instancias del objeto CheckBox
        self.lista_checks = []

        #en list_values se almacenan los valores obtenidos
        # con el metodo 'get'
        self.list_values = {}

        # widgets
        self.count = 0
        for check in list_options:
            self.count+=1
            self.checkbox = CheckBox(self.frame,f"{check}", self.count,0)
            self.lista_checks.append(self.checkbox)

        self.uncheck_all()
    
    def get(self):
        """obtiene una lista de todos los buleanos"""
        self.list_values = {}
        for checkbox_button in self.lista_checks:
            value = checkbox_button.data.get()
            self.list_values[checkbox_button.text_] = value
            # print(checkbox_button.text_)
        
        print(self.list_values)
        return self.list_values
        

    def check_all(self):
        for checkbox in self.lista_checks:
            checkbox.check()

    def uncheck_all(self):
        for checkbox in self.lista_checks:
            checkbox.uncheck()

class CheckBox:
    def __init__(self, frame, text_, row_, column_):
        """crea el objeto de check button"""
        #parameters
        self.frame =frame 
        self.text_ = text_
        self.row_ = row_
        self.column_ = column_
        
        # data
        self.data = tk.BooleanVar()

        self.habilitado = True
        
        # check
        self.check_box = tk.Checkbutton(self.frame, font=NORMAL_FONT,cursor = "hand2", text=text_ ,variable = self.data)
        self.check_box.grid( row = self.row_, column = self.column_, pady = 5)

        self.check()
    
    def desabilitar(self):
        self.check_box.config(state = "disabled")
        self.habilitado = False
        return self.habilitado
    
    def habilitar(self):
        self.check_box.config(state = "normal")
        self.habilitado = True
        return self.habilitado

    def checked(self):
        value = self.data.get()
        # print(value)
        return value

    def check(self):
        self.data.set(True)
    
    def uncheck(self):
        self.data.set(False)

if __name__ == '__main__':    
    # # MAIN VENTANA
    root = tk.Tk()
    root.title("hola")
    frame = tk.Frame(root)

    bac = NumeroBac(frame,"text", ["CME", "CDI", "LPU"],0,0  )# parent, texto, tipo_document, _row, _column
    bac.item_default(1)

    submit_button = tk.Button(frame, text ="SUBMIT",command = bac.get)
    submit_button.grid(column = 0,row = 1)

    frame.pack()
    root.mainloop()
