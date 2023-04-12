import tkinter as tk
from tkinter import Button, Frame, ttk, Canvas,Scrollbar,filedialog
from functools import partial
import json
# import nav_vertical_right as nvr
import datetime 

NORMAL_FONT = "Calibri 14"

def open_json(file):
    """abre los archivos json para su lectura"""
    with open(file) as json_file: #ABRIR EL ARCHIVO	
        main_objeto = json.load(json_file) #LA VARIABLE 'datos' ABRE EL OBJETO JSON DEL ARCHIVO 'json_file'
        return main_objeto
def open_parameter( parameter):
    return open_json("parametros.json")["parametros"][f"{parameter}"]

def save_json(file,parametro, valor): #1er. ARG: EL NOMBRE DE ARCHIVO, 2do ARG: EL DATO QUE ABRE EL OBJETO PARA AGREGAR DATOS
    """escribe datos en el archivo json que se le asigne."""
    data = open_json(file)
    data["parametros"][f"{parametro}"] = valor
    with open(file, "w") as outfile:
        json.dump(data, outfile, sort_keys = False, indent = 4)
        # outfile["parametros"][f"{parametro}"]

class InfoFrame:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="x")

        self.label = tk.Label(self.parent,font = "Calibri 10", text ="")
        self.label.pack(fill = "x")

    def warning(self, texto):
        print(f"Peligro: {texto}")
        self.frame.config(bg = "#CA6161")
        self.label.config(bg = "#CA6161", fg= "white", text =texto)
    def success (self, texto):
        print("")        
        self.frame.config(bg = "#44C190")
        self.label.config(bg = "#44C190", fg= "white", text =texto)
    def info(self, texto):
        print(f"Info: {texto}")
        self.frame.config(bg = "#CDCDCD")
        self.label.config(bg = "#CDCDCD", fg= "black", text =texto)

class ConfigFrame:
    def __init__(self, parent):
        #parameters
        self.parent = parent

        self.frame = ttk.LabelFrame(self.parent, text ="Config ", padding = 10)
        self.frame.pack(fill = "x", padx = 5, pady = 5)

        # self.file_template = PathSelector(self.frame, "Plantilla", 10, 0, "file_template")
        self.file_output = PathSelector(self.frame, "Destino del archivo", 20, 0, "path_output")

class FechaDividido:
    def __init__(self, parent, texto, _row, _column ):
        
        # parameters
        self.parent = parent
        self.texto = texto
        self._row = _row
        self._column = _column

        self.data_day = tk.StringVar()
        self.data_month = tk.StringVar()
        self.data_year = tk.StringVar()

        self.frame_main = tk.Frame(self.parent)
        self.frame_main.grid(row = self._row, column = self._column)
        self.fecha_consulta_label = tk.Label(self.frame_main,cursor="hand2", text = self.texto, font = NORMAL_FONT)
        self.fecha_consulta_label.pack(side = "left", pady = 5, padx = 5)        
        self.fecha_consulta_label.bind("<Button-1>", self.focus_entry)

        self.dia_consultas = ttk.Entry(self.frame_main, width=3, font = NORMAL_FONT, textvariable=self.data_day)
        self.dia_consultas.pack(side = "left", pady = 5, padx = 5)
        self.dia_consultas.bind('<Return>', self.button_tab )
        self.delimitador_1 = tk.Label(self.frame_main, text = "/", font = NORMAL_FONT)
        self.delimitador_1.pack(side = "left", pady = 5, padx = 5)
        self.mes_consultas = ttk.Entry(self.frame_main, width=10, font = NORMAL_FONT, textvariable=self.data_month)
        self.mes_consultas.pack(side = "left", pady = 5, padx = 5)
        self.mes_consultas.bind('<Return>', self.button_tab )
        self.delimitador_2 = tk.Label(self.frame_main, text = "/", font = NORMAL_FONT)
        self.delimitador_2.pack(side = "left", pady = 5, padx = 5)
        self.anio_consultas = ttk.Entry(self.frame_main, width=6, font = NORMAL_FONT, textvariable=self.data_year)
        self.anio_consultas.pack(side = "left", pady = 5, padx = 5)
        self.anio_consultas.bind('<Return>', self.button_tab )
    
    # events
    def focus_entry(self,event):
        self.dia_consultas.focus()

    # methods
    def button_tab(self, event):    
        self.parent.event_generate('<Tab>')
    
    def get(self):
        get_day = self.data_day.get()
        get_month = self.data_month.get()
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
    def __init__(self,parent, text_):
        # parameters
        self.parent = parent
        self.text_ = text_

        #textVariable
        self.data = tk.StringVar()

        # widgets
        self.label = tk.Label(self.parent, text = text_)
        self.label.pack

        self.textarea = tk.Text(self.parent , width = 30, height = 5,
                                bd =2,relief ="groove",
                                        font= "Calibri 14")
        self.textarea.pack(fill = "x")
        self.textarea.bind("<Control-BackSpace>", self.clean)

    def get(self):
        self.textarea.get("1.0",'end-1c')

    def clean(self, event):
        # permite limpiar la entry de texto presionando control-suprimir
        self.textarea.delete(1.0, tk.END)

    def deshabilitar(self):
        self.entry.config(state = "disabled")

class TagsAndEntry:
    """etiqueta y entry para cruds"""
    def __init__(self, parent, text_, row_, column_, focus=False):        
        # parameters
        self.parent = parent
        self.text_ = text_
        self.row_ = row_
        self.column_ = column_
        self.focus = focus
        
        # tipos de datos
        self.data = tk.StringVar()

        # widgets
        self.label = ttk.Label(self.parent, text = self.text_.capitalize(),cursor="hand2", font = NORMAL_FONT)
        self.label.grid(row = self.row_, column = self.column_)
        self.label.bind("<Button-1>", self.focus_entry)

        self.entry = ttk.Entry(self.parent, width = 23,font = NORMAL_FONT, textvariable = self.data)
        self.entry.grid(row = self.row_, column = self.column_ + 1, pady = 3)
        self.entry.bind('<Return>', self.button_tab )
        self.entry.bind("<Control-BackSpace>",self.cleaner)
        
        # self.nro_desde_entrada.entry.bind('<Return>', self.get_orden_number )

        if self.focus == True:
            self.entry.focus()    

    # events 
    def focus_entry(self,event):
        self.entry.focus()

    def button_tab(self, event):    
        self.parent.event_generate('<Tab>')

    # metodos
    def cleaner(self, event):
        # permite limpiar la entry de texto presionando control-suprimir
        self.data.set("")

    def get(self):
        data = self.data.get()
        return data 

    def disabled(self):
        self.label.config(state = "disabled")
        self.entry.config(state = "disabled")

    def enable(self):
        self.label.config(state= "enabled")
        self.entry.config(state= "enabled")

class TagsAndEntryBlock(TagsAndEntry):
    def __init__(self, parent, text_, row_, column_ , block = False):
        TagsAndEntry.__init__(self,parent, text_, row_, column_)
        self.block = block
        

        self.block_button = ttk.Button(self.parent, text ="block",cursor="hand2", command=self.block_entry)
        self.block_button.grid(column = column_+2,row = row_)

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

        self.data.set(open_json("parametros.json")["parametros"][self.parametro])
        
        self.entry.config(width=47, font = "Calibri 12")
        self.block_button = tk.Button(self.parent, text ="path", command = lambda: self.path(self.parametro))
        self.block_button.grid(column = column_+2,row = row_, padx = 5)

    def path(self,parametro):
        parametro_valor = open_json("parametros.json")
        print(parametro_valor["parametros"][f"{parametro}"]) 
        self.directory = filedialog.askdirectory(title=f"{self.text_}")#, initialdir=f"{parametro_valor}")
        self.data.set(self.directory)
        save_json("parametros.json",f"{parametro}",f"{self.directory}")
        
        self.data.set(open_json("parametros.json")["parametros"][self.parametro])

class FileSelector(TagsAndEntry):
    def __init__(self, parent, text_, row_, column_, parametro ):
        self.parametro = parametro
        TagsAndEntry.__init__(self,parent, text_, row_, column_)

        self.data.set(open_json("parametros.json")["parametros"][self.parametro])
        
        self.entry.config(width=47, font = "Calibri 12")
        self.block_button = tk.Button(self.parent, text ="path", command = lambda: self.path(self.parametro))
        self.block_button.grid(column = column_+2,row = row_, padx = 5)

    def path(self,parametro):
        parametro_valor = open_json("parametros.json")
        print(parametro_valor["parametros"][f"{parametro}"]) 
        self.directory = filedialog.askopenfilename(title=f"{self.text_}")#, initialdir=f"{parametro_valor}")
        self.data.set(self.directory)
        save_json("parametros.json",f"{parametro}",f"{self.directory}")
        
        self.data.set(open_json("parametros.json")["parametros"][self.parametro])

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
        self.label = ttk.Label(self.parent, text = self.text_.capitalize()+":",cursor = "hand2", font = "Calibri 14")
        self.label.grid(row = self.row_, column = self.column_)
        self.label.bind("<Button-1>", self.focus_entry)
        # widgets
        self.desplegable = ttk.Combobox(self.parent,textvariable = self.data,
                                        width = 23,font = "Calibri 14",
                                        values = self.list_options)
        self.desplegable.grid( row = self.row_, column = self.column_+1, pady = 3)
        self.desplegable.bind('<Return>',self.entry_event)



    def focus_entry(self,event):
        self.desplegable.focus()

    def entry_event(self, event):
        self.get()
        self.parent.event_generate('<Tab>')

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
    """ genera una etiqueta y un combobox para los formularios"""
    def __init__(self, parent, text_, row_, column_, list_options):
        # parameters
        self.parent = parent
        self.text_ = text_
        self.row_ = row_
        self.column_ = column_
        self.list_options = list_options

        # widgets
        self.desplegable = ttk.Checkbutton (self.parent,textvariable = self.data,
                                        width = 23,font = "Calibri 14",
                                        values = self.list_options)
        self.desplegable.grid( row = self.row_, column = self.column_+1, pady = 3)
        self.desplegable.bind('<Return>',self.send)
    

    def send(self, event):
        data = self.data.get()
        self.parent.event_generate('<Tab>')
        print(data)


if __name__ == '__main__':    
    # MAIN VENTANA
    print(open_parameter("file_template"))

