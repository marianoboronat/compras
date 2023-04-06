import tkinter as tk
from tkinter import Button, ttk
from tkinter.constants import NO

# import settings
import widgets
# import objects_db as db


class TreeviewData():
    def __init__(self, parent):
        self.parent = parent 
        # Definicion de frames
        self.frame = ttk.Frame(self.parent)
        self.frame.pack( expand=1,fill = tk.BOTH)
        
        #Frame del Arbol
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(expand=1,fill = tk.BOTH)

        
        self.tree.bind('<<TreeviewSelect>>', lambda x : self.element_clicked()) 

    def element_clicked(self):
        item = self.tree.focus()
        print(self.tree.item(item, "values"))
        return self.tree.item(item, "values")


    def head(self, list_head):
        """genera una cabecera para el arbol"""
        #Definicion de columnas

        if type(list_head) == list:
            self.tree["columns"] = list_head
            self.tree.column("#0",width = 0, stretch = tk.NO) #Omitir la columna fantasma.

            #loop for create the heading with lists
            count = 0
            for item in list_head:
                count +=1
                #Agregar las columnas
                self.tree.column(f"#{count}")
                #Agregar el nombre de los encabezados
                self.tree.heading(f"{item}", text=f"{item}")

        elif type(list_head) == dict:
            list_heading = list(list_head.keys())
            list_propierties = list(list_head.values())

            print("keys: ", list_heading,"values", list_propierties)

            self.tree["columns"] = list_heading
            self.tree.column("#0",width = 0, stretch = tk.NO) #Omitir la columna fantasma.

            print(list_heading)
            #loop for create the heading with dict
            count = 0
            for item in list_heading:
                count +=1
                #Agregar las columnas
                # if exists the column width number 
                if "width" in list_head[item].keys(): 
                    self.tree.column(f"#{count}", width =list_head[item]["width"])
                else:
                    self.tree.column(f"#{count}", width = 100)

                # if exists the column anchor number 
                if "anchor" in list_head[item].keys():                     
                    self.tree.column(f"#{count}", anchor =list_head[item]["anchor"] )
                else:
                    self.tree.column(f"#{count}", anchor ="center" )

                #Agregar el nombre de los encabezados
                self.tree.heading(f"{item}", text=f"{item}")
            
    
    def write_rows(self, list_values):
        """Iterar datos para filas"""
        try:
            self.reset_tree()
            count = -1    
            for row in list_values:
                count += 1
                # print("fila: ",count, row)
                main_item = self.tree.insert(parent = "", index = tk.END, iid = count, values = row )
        except:
            print("Hubo un error en la escritura de filas.")

    def reset_tree(self):
        """cleaning all rows of the treeview"""
        for i in self.tree.get_children():
            self.tree.delete(i)

    def delete_row(self,list_values):
        try:
            focus = int(self.tree.focus())
            item = list_values.pop(focus)
            self.tree.write_rows(list_values)
            print(focus, list_values)
        except:
            print("ERROR: tree.py/FormFrame/delete_row():\nocurrio un problema")


heading = ["number", "title", "year"]
fake_data = [
                        ["112", 'fifa world cup: germany 2006', "2006"],
                        ["111", "high school musical 3: senior year dance!","2008"],
                        ["110","Van Helsing","2004"],
                        ["109","Silent Hill 2", "2001"],
                        ["108", "Ace Combat 5: The Unsung War","2004"]
                        ]

class FormFrame:
    def __init__(self, parent,tree, list_values, list_heading):
        #parameters
        self.parent = parent
        self.tree = tree
        self.list_values = list_values
        self.list_heading =list_heading
        # frames
        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        self.number = widgets.TagsAndEntry(self.frame, "Numero", 0, 0)
        self.title = widgets.TagsAndEntry(self.frame, "titulo", 1,0)
        self.launch_year = widgets.TagsAndEntry(self.frame, "año", 2, 0)

        self.label_info = tk.Label(self.frame, text = "")
        self.label_info.grid(row = 99, column = 0, columnspan=2)

        self.boton = tk.Button(self.frame, width = 25, text = "Submit", command = lambda: self.add_data(self.list_values , self.get_data()))
        self.boton.grid(row = 3, column = 0, columnspan=2, pady = 5, padx = 5)

        self.boton_delete = tk.Button(self.frame, width = 25, text = "Delete",
                                    command = lambda: self.delete_row(self.list_values))
                                    # command = self.tree.reset_tree)
        self.boton_delete.grid(row = 4, column = 0, columnspan=2, pady = 5, padx = 5)


        self.tree.head(self.list_heading)
        self.tree.write_rows(self.list_values)
        

    
    def cleaner(self):
        self.number.data.set("")
        self.title.data.set("")
        self.launch_year.data.set("")

    def get_data(self):
        data = [
        self.number.data.get(),
        self.title.data.get(),
        self.launch_year.data.get()
        ]
        return data

    def add_data(self, list_values, data):
        try:
            count = 0
            for item in data:
                if item != "":
                    count += 1

            if count == len(data):
                self.cleaner()
                print(data)
                list_values.append(data)
                self.tree.write_rows(list_values)                
                self.tree.element_clicked(event=None)
                return data

            else:
                print("Todos los datos deben ser cagados")
        except:
            print("tree.py/FormFrame/get_info(): \nocurrio un problema ")
    

    def delete_row(self,list_values):
        try:
            focus = int(self.tree.tree.focus())
            item = list_values.pop(focus)
            self.tree.write_rows(list_values)
            print(focus, list_values)
        except:
            print("ERROR: tree.py/FormFrame/delete_row():\nocurrio un problema")


def verificar_key():
    heading = {
        "id":{"width":100,
        },
        "name":{"width":400,
                    "anchor":"w"
        },
        "lastname":{"width":400,
                    "anchor":"w"
        }
    }
    keys = list(heading.keys())
    print(keys.index("name"))
    if "id" in keys:
        print("id existe en esta lista.")
    else:
        print("id no existe en esta lista")

if __name__ == "__main__":
    verificar_key()
    root = tk.Tk()
    root.mainloop()