import openpyxl
import time
import admin_json
import json
import tkinter as tk
import read_excel


class ExcelReader:
    def __init__(self, xl_comparacion, xl_renglones):
        """una clase que permite leer excel de comparacion"""
        self.xl_comparacion = self.open_excel(xl_comparacion)
        self.xl_renglones = self.open_excel(xl_renglones)

        self.json_file = "bd/comparacion.json"

        #almacenar contratacion en el json
        self.guardar_json()

        
    def open_excel(self, path):
        try:
            workbook = openpyxl.load_workbook(path)
            sheet = workbook.active
            list_values = list(sheet.values)
            return list_values
        except Exception as e:
            print(e, "se debe cargar un excel")
            return "False"

    def datos_contratacion(self):
        """datos basico de la contratacion"""
        contratacion = self.xl_comparacion[1][4]
        detalle = self.xl_comparacion[2][4]
        precio_estimado_total = self.xl_renglones[-1][-1]
        return [contratacion, detalle, precio_estimado_total]
    
    def lista_empresas(self):
        """devuelve una lista de los nombres de empresas"""   
        try:
            values = self.xl_comparacion
            lista_empresas = [nombre_empresa.upper() for nombre_empresa in values[7][6:] if nombre_empresa != None]

            return lista_empresas
        except Exception as e:
            print(e)

    def renglones_pedidos(self):
        """devuelve una lista de tuplas de cada renglon pedido.
        Esto lo extrae del excel de los renglones."""
        lista = [renglon[0:-2] for renglon in self.xl_renglones[1:-4]]    
        return lista

    def leer_ofertas_por_empresa(self, renglon, empresa ):
        """devuelve una lista de listas con la empresa y la oferta"""
        empresas = self.lista_empresas()[empresa-1]
        # print(values)
        lista = []
        for oferta in self.xl_comparacion[9:-1]:
            renglon_ = int(oferta[0])
            opcion = int(oferta[1])
            # print(renglon_)
            if renglon_ == renglon:
                # print(empresa)
                datos_oferta= list(oferta[empresa*6 : 6+empresa*6])
                datos_oferta.append(opcion)
                # print(datos_oferta)
                if datos_oferta[0]!=None:
                    datos_oferta.append(empresas)
                    lista.append(datos_oferta)
        return lista

    def ofertas_x_renglon(self, renglon):
        """obtiene una lista de listas de cada renglon con sus valores"""
        cant_empresas = len(self.lista_empresas())
        lista = []
        count = 0

        for value in range(cant_empresas):        
            count +=1
            ofertas = self.leer_ofertas_por_empresa( renglon, count)
            # print(ofertas)
            if ofertas !=None:
                lista.extend(ofertas)

        lista = self.ordenar_listas(lista)

        # obtener los datos de los renglones
        datos_renglon = [dato_renglon[5] for dato_renglon in self.xl_renglones if str(dato_renglon[0])==str(renglon)][0]

        return {f"{renglon}":{"precio_estimado":datos_renglon,"ofertas":lista}}

    def desiertos(self):
        """devuelve una lista de desiertos"""        
        desiertos = [renglon[0] for renglon in self.renglones_pedidos() if self.ofertas_x_renglon(renglon[0])[f'{renglon[0]}']['ofertas']==[]]
        return desiertos

    def renglon_fracasado(self, renglon):
        """calcula si un renglon quedo fracasado"""
        counter = 0

        precio_est = [precio_est[-2] for precio_est in self.renglones_pedidos() if precio_est[0]==renglon][0]
        precio_est_20 = precio_est*0.2+precio_est

        for num_renglon in self.ofertas_x_renglon(renglon):
            lista_ofertas = self.ofertas_x_renglon(renglon)[num_renglon]["ofertas"]
            # print(lista_ofertas)
            if len(lista_ofertas) == 0 :
                counter += 1
            else:
                for oferta in lista_ofertas:
                    precio_ofertado = oferta[1]
                    # print(precio_ofertado, precio_est_20)
                    if float(precio_ofertado) < float(precio_est_20):
                        counter += 1

        if counter > 0:
            return False
        else:
            print(f"el renglón {renglon} está fracasado.", counter)
            return renglon



    def renglones_fracasados(self):
        """Devuelve una lista de todos los fracasados
         de la contratacion con la función self.renglon_fracasado"""
        lista_fracasados = []

        for renglon in self.renglones_pedidos():
            # print(renglon[0])
            fracasado = self.renglon_fracasado(int(renglon[0]))
            if fracasado != False:
                lista_fracasados.append(fracasado)

        return lista_fracasados


    def todas_ofertas_y_renglones(self):
        """itera todas las empresas con todas las ofertas de la contratacion"""
        ofertas = self.renglones_pedidos()
        count = 0
        lista = []
        for oferta in ofertas:
            count += 1
            # print(oferta)
            ofertas_renglon = self.ofertas_x_renglon(count)
            lista.append(ofertas_renglon)

        return lista

    def ordenar_precios(self, lista):
        ordenamiento = [x[1] for x in lista]
        ordenamiento.sort()
        return ordenamiento

    def ordenar_listas(self, lista):
        """ordena la lista"""
        lista_precios_ordenados = self.ordenar_precios(lista)

        lista_in = lista
        lista_out = []

        for precio in lista_precios_ordenados:
            for item in lista_in:
                if precio == item[1]:
                    lista_out.append(item)
                    lista_in.remove(item)
        return lista_out
    
    def guardar_json(self):
        numero_contratacion = self.xl_comparacion[1][4]
        precio_estimado = float(self.xl_renglones[-1][-1].split(" ")[1].replace(".", "").replace(",", "."))
        # print(precio_estimado,numero_contratacion)
        
    
        context = {
            numero_contratacion:{
                "precio_estimado":precio_estimado,
                "ofertas":self.todas_ofertas_y_renglones()
            }
        }
        values = admin_json.open_json(self.json_file)
        
        # verificar si la contratacion ya existe.
        # almacenamos todas las contrataciones en la lista 'existe'
        existe = [list(x.keys())[0] for x in values]
        
        # a traves del manejo de errores verifica 
        # si ya existe la contratacion en el json
        try:
            existe.index(numero_contratacion)
            print(f"La contratacion {numero_contratacion} ya existe")
        except:
            print(f"{numero_contratacion} fue creada con exito")
            values.append(context)
            admin_json.save_json_values(self.json_file, values)



class ReadJson:
    def __init__(self,contratacion):
        """una clase que permite leer el archivo json"""
        self.contratacion = contratacion
        
        #propierties
        self.file = "bd/comparacion.json"
        self.values = admin_json.open_json(self.file)
    
    def read_file(self):
        for value in self.values:
            print(value)


if __name__ == "__main__":
    xl = "PROCESOS/455-2053-CME20/CuadroComparativo.xlsx"
    xl2= "PROCESOS/455-2053-CME20/Detalle-producto-05072023.xlsx"
    
    leer_excel = ExcelReader(xl, xl2)
    print(leer_excel.renglones_pedidos())

