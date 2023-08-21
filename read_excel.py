import openpyxl
import time
import admin_json
import json
import tkinter as tk

recomendaciones = {
    "3276" : "PROCESOS PARA TESTEAR//3276//3276.xlsx",
    "3276_detalles" : "PROCESOS PARA TESTEAR//3276//Detalle-producto.xlsx",
    
    "2243" : "PROCESOS PARA TESTEAR//2243//2243.xlsx",
    "2243_detalles" : "PROCESOS PARA TESTEAR//2243//renglones.xlsx",
    
    "0893":"PROCESOS PARA TESTEAR//0893//1.xlsx",
    "0893_detalles":"PROCESOS PARA TESTEAR//0893//renglones.xlsx",

    "0798": "PROCESOS PARA TESTEAR//0798//0798.xlsx",
    "0798_detalles" : "PROCESOS PARA TESTEAR//0798//renglones.xlsx",
    
    "2874": "PROCESOS PARA TESTEAR//2874//2874.xlsx",
    "2874_detalles" : "PROCESOS PARA TESTEAR//2874//renglones.xlsx"
}

class LeerExcel:
    """una clase para leer los exceles de 'recomendacion' y 'renglones'
    y extraer sus datos para el json"""
    def __init__(self,xl_recomendacion,xl_renglones ):
        self.xl_recomendacion = self.open_excel(xl_recomendacion)
        self.xl_renglones = self.open_excel(xl_renglones)

    def open_excel(self, path):
        try:
            workbook = openpyxl.load_workbook(path)
            sheet = workbook.active
            list_values = list(sheet.values)
            return list_values
        except Exception as e:
            print(e, "se debe cargar un excel")
            return "False"        

    def lista_empresas(self):
        """devuelve una lista con los nombre de las empresas presentadas"""
        try:
            lista_empresas = [nombre_empresa.upper() for nombre_empresa in self.xl_recomendacion[3][3:] if nombre_empresa != None]
            return lista_empresas
        except Exception as e:
            print(e)

    def lista_empresas_cuit(self):
        """devuelve una lista con los nombre de las empresas y sus cuit"""
        listado_empresas = self.lista_empresas()
        lista = []
        count = 0        
        for empresa in listado_empresas:
            count += 1
            cuit = self.xl_recomendacion[4][count*3:3+count*3][0]
            lista.append({empresa : cuit})

        return lista

    def leer_precio_renglon_por_empresa(self,fila, indice_empresa):
        """calcula el precio de un solo renglon de una empresa"""
        numero_renglon = str(self.xl_recomendacion[fila-4:][3][0])+"."+str(self.xl_recomendacion[fila-4:][3][1])
        precio_y_cantidad = self.xl_recomendacion[fila-4:][3][ 3*indice_empresa: 3*indice_empresa+3]

        return numero_renglon, precio_y_cantidad
    
    def leer_renglon_por_empresa(self, fila, indice_empresa):
        """calcula el precio de un solo renglon de una empresa"""
        numero_renglon =  self.xl_recomendacion[fila-1][indice_empresa*3:3+indice_empresa*3]
        return numero_renglon
    
    def renglones_ofertadas(self):
        """cargar excel de recomendaciones
        devuelve una lista con la totalidad de renglones ofertadas por todas las empresas"""
        lista_renglones_ofertadas = [str(renglon[0])+"."+str(renglon[1])  for renglon in self.xl_recomendacion[6:] if type(renglon[0]) == int] 

        return lista_renglones_ofertadas
    
    def precio_total_x_empresa(self, indice_empresa):
        """devuelve el precio total que se le adjudico a la empresa seleccionada"""
        numero_de_renglones = len(self.renglones_ofertadas())
        count = 0
        for fila in self.xl_recomendacion:
            count += 1
            if count == numero_de_renglones+1:
                # print(numero_de_renglones)
                precio_total = self.convertir_a_numero(self.leer_renglon_por_empresa(numero_de_renglones+7,indice_empresa)[0])
                break

        return precio_total

    def renglones_ofrecidos_por_empresa(self, indice_empresa):
        """devuelve un diccionario con los renglones que presento la empresa
        seleccionada. el 1er valor del diccionario es 'adjudicados'
        y el 2do es el 'desestimados'"""
        
        adjudicados = []
        desestimados = []
        
        #cantidad de ofertas totales
        ofertas = self.renglones_ofertadas()
        for oferta in range(len(ofertas)):
            # print(oferta)
            #xl_recomendacion,fila, indice_empresa
            fila = self.leer_precio_renglon_por_empresa(oferta+7,indice_empresa)
            renglon = fila[0]
            precio_total = fila[1][2]
            # print(fila, renglon)
            
            if fila[1] != ('', '', ''):
                """si la empresa oferto"""
                datos_renglon = [renglon, precio_total]
                
                # desestimados:
                if precio_total == "ARS":
                    if renglon.split(".")[1] == "1":
                        print("renglon desestimado", renglon)
                        desestimados.append(int(renglon.split(".")[0]))
                    else:
                        print("renglon desestimado", renglon)
                        desestimados.append(float(f"{renglon.split('.')[0]}.{renglon.split('.')[1]}"))
                    # print(renglon,"desestimado")
                
                # adjudicados:
                elif precio_total != "ARS":

                    # si el renglon es primera opcion que solo aparezca el numero
                    if renglon.split(".")[1] == "1":
                        print("renglon adjudicado", renglon)
                        adjudicados.append(int(renglon.split(".")[0]))
                    else:
                        print("renglon adjudicado", renglon)
                        adjudicados.append(float(renglon))

                    # print(renglon,"adjudicado")
        
        return {"adjudicados":adjudicados, "desestimados":desestimados}

    def monto_estimado(self):
        """devuelve el monto estimado """
        estimado = self.xl_renglones[-1][-1].split(" ")[1]
        estimado = estimado.replace(".","")
        estimado = self.convertir_a_numero("ARS "+estimado.replace(",","."))

        return estimado
    
    def cantidad_renglones_solicitadas(self):
        """cargar excel de 'detalle de renglones',
        devuelve la lista completa de renglones solicitada por compras"""
        lista_renglones = [renglon[0]  for renglon in self.xl_renglones if type(renglon[0]) == int] 

        return lista_renglones 
    
    def renglones_desiertos(self):
        """devuelve una lista de renglones desiertas: POR NO TENER OFERTAS.
        compara la lista de la funcion 'cantidad_renglones_solicitadas'
        y 'renglones_ofertadas'"""
        renglones_pedidos = self.cantidad_renglones_solicitadas()
        lista_ofertas = self.renglones_ofertados_sin_opciones(self.renglones_ofertadas())
        lista_desiertos = [] #
        # print(renglones_pedidos, lista_ofertas)

        for pedidos in renglones_pedidos:
            # time.sleep(0.1)
            try:
                lista_ofertas.index(pedidos)
            except:
                lista_desiertos.append(pedidos)

        print(lista_desiertos)
        return lista_desiertos
    
    def renglones_ofertados_sin_opciones(self,lista_renglones):
        """devuelve una lista de renglones ofertadas por todas las empresas
        sin las opciones."""
        lista = {}
        for renglon in lista_renglones:
            if type(renglon)== int or type(renglon)== float:
                lista[int(renglon)]=True
            elif type(renglon) != int:
                lista[int(renglon.split(".")[0])] = True

        return list(lista.keys())

    # GENERAR PROCESO PARA EL JSON #
    def datos_contratacion(self):
        """toma datos basico de la contratacion del excel de recomendacion
        y del excel de renglones"""
        values = self.xl_recomendacion
        
        numero_contratacion = values[1][3].split(" ")[-1]        
        ee_tipo_documento  = values[1][0].split(" ")[4].split("-")[0]
        ee_anio = values[1][0].split(" ")[4].split("-")[1]
        ee_num = values[1][0].split(" ")[4].split("-")[2]
        ee_reparticion = values[1][0].split("-")[6]
        numero_expediente = f'{ee_tipo_documento}-{ee_anio}-{ee_num}-GCABA-{ee_reparticion}'

        dia_apertura = values[1][9].split("/")[0].split(" ")[1]
        mes_apertura = values[1][9].split("/")[1]
        anio_apertura = values[1][9].split("/")[2]
        precio_estimado = self.monto_estimado()
        
        datos = {
            "n_proceso":f"{numero_contratacion}",
            "expediente":f"{numero_expediente}",
            "fecha_apertura_dia":f"{dia_apertura}",
            "fecha_apertura_mes":f"{mes_apertura}",
            "fecha_apertura_anio":f"{anio_apertura}",
            "monto_estimado":f"{precio_estimado}"
            }

        return datos
    
    def crear_plantillas_empresas(self):
        """crea una lista de empresas de la contratacion y sus 
        propiedades para el json"""

        list_empresas = self.lista_empresas_cuit()
        list_json  = []
        count = 0

        for empresa in list_empresas:
            nombre_empresa = list(empresa.keys())[0]
            print(nombre_empresa)        
            count += 1 

            renglones = self.renglones_ofrecidos_por_empresa(count)
            adjudicados = renglones["adjudicados"]
            desestimados = renglones["desestimados"]

            precio_total = self.precio_total_x_empresa(count )


            dict_empresa = {
                    "empresa":nombre_empresa,
                    "cuit": "",#cargan a mano
                    "doc_complementaria": False,#cargan a mano
                    "renglones_adjudicados":adjudicados,
                    "renglones_desestimados":{
                        "administrativo":[],
                        "tecnicamente":[],
                        "economicamente":desestimados
                        },
                    "precio_total": precio_total,
                    "precio_total_letras": "",#cargan a mano
                    "monto_anterior":"",
                    "monto_anterior_letras":""
                    
                }
            list_json.append(dict_empresa)

        return list_json

    def crear_proceso(self):
        """guarda los datos basicos  de la contratacion en el json
        usando funciones del modulo 'read_excel'"""
        
        cantidad_empresas = len(self.lista_empresas())
        datos_basicos = self.datos_contratacion()
        datos_empresas = self.crear_plantillas_empresas()
        desiertas = self.renglones_desiertos()
        precio_estimado = self.monto_estimado()

        plantilla_contratacion = {
            f'{datos_basicos["n_proceso"]}':{
            "detalle":"",
            "expediente":datos_basicos["expediente"],
            "num_dispo":"",
            "informe_grafico":"",
            "num_dispo_adj":"",
            "fecha_publicacion":{"dia":"",
                            "mes":"",
                            "anio":""
                            },
            "monto_estimado":precio_estimado,
            "monto_estimado_letras":"",
            "monto_adjudicado":"",
            "monto_adjudicado_letras":"",
            "fecha_apertura":{"dia":datos_basicos["fecha_apertura_dia"],
                            "mes":datos_basicos["fecha_apertura_mes"],
                            "anio":datos_basicos["fecha_apertura_anio"]
                            },
            "fecha_final_consultas":{"dia":"",
                            "mes":"",
                            "anio":""
                            },
            "hora_apertura":{
                "horas":"10",
                "minutos":"00"
                },
            "firmas_interesadas":0,
            "firmas_confirmadas":cantidad_empresas,
            "desiertos":desiertas,
            "fracasados":"",
            "lista_empresas":datos_empresas
        }}
        return plantilla_contratacion

    # funciones para conversion de precios
    def convertir_a_numero(self,celda):
        """convierte una celda de texto (ARS 1000.00) a numero"""
        precio_i = celda.split(" ")[-1].split(".")[0]
        precio_f = celda.split(" ")[-1].split(".")[-1]
        if precio_i != "ARS":
            if precio_f == "00":
                precio_f=0.0
            precio_final = float(precio_i)+0.01*float(precio_f)      
        return precio_final

    def agregar_puntos_precio(self, precio):
        """agregarle puntos a los enteros, y comas a los decimales y 2 cifras
        ejemplo: 12345 >>> 12.345"""
        precio_int = str(precio).split(".")[0]
        count = 0
        pre_final = ""
        for x in precio_int:
            count -=1
            resto = count % 3 
            pre_final += precio_int[count]
            if resto ==0:
                pre_final += "."
            # print(precio_int,precio_int[count],count,  resto)

        final = ""
        count = 0
        for letra in pre_final:        
            count -=1
            final += pre_final[count]
        if final[0] ==".":
            final = final[1:]

        return final

    def agregar_comas_precio(self,precio):
        precio_int =  str(agregar_puntos_precio(precio))
        precio_float = ","+str("%.2f"%precio).split(".")[1]
        return precio_int+precio_float    



# ______________________________________________________



def open_excel(path):
    try:
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)
        return list_values
    except Exception as e:
        print(e, "se debe cargar un excel")
        return "False"


#EN DESARROLLO
def verificar_excel_recomendacion(xl_recomendacion):
    """verifica si el excel de recomendacion cargado es el correcto
    si es correcto, devuelve 'true' si no 'false'"""
    values = open_excel(xl_recomendacion)[0:3][1]
    
    return values 




def lista_empresas(xl_recomendacion):
    """devuelve una lista con los nombre de las empresas presentadas"""
    try:
        list_values = open_excel(xl_recomendacion)
        lista_empresas = [nombre_empresa.upper() for nombre_empresa in list_values[3][3:] if nombre_empresa != None]
        count = 0
        return lista_empresas
    except Exception as e:
        print(e)

def lista_empresas_cuit(xl_recomendacion):
    """devuelve una lista con los nombre de las empresas y sus cuit"""
    list_values = open_excel(xl_recomendacion)
    listado_empresas = lista_empresas(xl_recomendacion)
    lista = []

    count = 0
    
    for empresa in listado_empresas:
        count += 1
        cuit = list_values[4][count*3:3+count*3][0]
        lista.append({empresa : cuit})

    return lista

def leer_precio_renglon_por_empresa(xl_recomendacion,fila, indice_empresa):
    """calcula el precio de un solo renglon de una empresa"""
    lista_values = open_excel(xl_recomendacion)
    numero_renglon = str(lista_values[fila-4:][3][0])+"."+str(lista_values[fila-4:][3][1])
    precio_y_cantidad = lista_values[fila-4:][3][ 3*indice_empresa: 3*indice_empresa+3]

    return numero_renglon, precio_y_cantidad

def leer_renglon_por_empresa(xl_recomendacion,fila, indice_empresa):
    """calcula el precio de un solo renglon de una empresa"""
    lista_values = open_excel(xl_recomendacion)
    numero_renglon =  lista_values[fila-1][indice_empresa*3:3+indice_empresa*3]
    return numero_renglon

def renglones_ofertadas(xl_recomendacion):
    """cargar excel de recomendaciones
    devuelve una lista con la totalidad de renglones ofertadas por todas las empresas"""
    lista_values = open_excel(xl_recomendacion)
    lista_renglones_ofertadas = [str(renglon[0])+"."+str(renglon[1])  for renglon in lista_values[6:] if type(renglon[0]) == int] 

    for renglon in lista_values[6:]:
        renglon

    return lista_renglones_ofertadas

def precio_total_x_empresa(xl_recomendacion, indice_empresa):
    """devuelve el precio total que se le adjudico a la empresa seleccionada"""
    valores =open_excel(xl_recomendacion)
    numero_de_renglones = len(renglones_ofertadas(xl_recomendacion))
    count = 0
    for fila in valores:
        count += 1
        if count == numero_de_renglones+1:
            # print(numero_de_renglones)
            precio_total = convertir_a_numero(leer_renglon_por_empresa(xl_recomendacion,numero_de_renglones+7,indice_empresa)[0])
            break

    return precio_total

def renglones_ofrecidos_por_empresa(xl_recomendacion, indice_empresa):
    """devuelve un diccionario con los renglones que presento la empresa
    seleccionada. el 1er valor del diccionario es 'adjudicados'
    y el 2do es el 'desestimados'"""
    
    adjudicados = []
    desestimados = []
    
    #cantidad de ofertas totales
    ofertas = renglones_ofertadas(xl_recomendacion)
    for oferta in range(len(ofertas)):
        # print(oferta)
        #xl_recomendacion,fila, indice_empresa
        fila = leer_precio_renglon_por_empresa(xl_recomendacion, oferta+7,indice_empresa)
        renglon = fila[0]
        precio_total = fila[1][2]
        # print(fila, renglon)
        
        if fila[1] != ('', '', ''):
            """si la empresa oferto"""
            datos_renglon = [renglon, precio_total]
            
            # desestimados:
            if precio_total == "ARS":
                if renglon.split(".")[1] == "1":
                    print("renglon desestimado", renglon)
                    desestimados.append(int(renglon.split(".")[0]))
                else:
                    print("renglon desestimado", renglon)
                    desestimados.append(float(f"{renglon.split('.')[0]}.{renglon.split('.')[1]}"))
                # print(renglon,"desestimado")
            
            # adjudicados:
            elif precio_total != "ARS":

                # si el renglon es primera opcion que solo aparezca el numero
                if renglon.split(".")[1] == "1":
                    print("renglon adjudicado", renglon)
                    adjudicados.append(int(renglon.split(".")[0]))
                else:
                    print("renglon adjudicado", renglon)
                    adjudicados.append(float(renglon))

                # print(renglon,"adjudicado")
    
    return {"adjudicados":adjudicados, "desestimados":desestimados}

# <CONVERSION DE NUMEROS>

def convertir_a_numero(celda):
    """convierte una celda de texto (ARS 1000.00) a numero"""
    precio_i = celda.split(" ")[-1].split(".")[0]
    precio_f = celda.split(" ")[-1].split(".")[-1]
    if precio_i != "ARS":
        if precio_f == "00":
            precio_f=0.0
        precio_final = float(precio_i)+0.01*float(precio_f)      
    return precio_final

def agregar_puntos_precio(precio):
    """agregarle puntos a los enteros, y comas a los decimales y 2 cifras
    ejemplo: 12345 >>> 12.345"""
    precio_int = str(precio).split(".")[0]
    count = 0
    pre_final = ""
    for x in precio_int:
        count -=1
        resto = count % 3 
        pre_final += precio_int[count]
        if resto ==0:
            pre_final += "."
        # print(precio_int,precio_int[count],count,  resto)

    final = ""
    count = 0
    for letra in pre_final:        
        count -=1
        final += pre_final[count]
    if final[0] ==".":
        final = final[1:]

    return final

def agregar_comas_precio(precio):
    precio_int =  str(agregar_puntos_precio(precio))
    precio_float = ","+str("%.2f"%precio).split(".")[1]
    return precio_int+precio_float
# <CONVERSION DE NUMEROS/>


def monto_estimado(xl_renglones):
    """devuelve el monto estimado """
    lista_values = open_excel(xl_renglones)
    monto_estimado = lista_values[-1][-1].split(" ")[1]
    monto_estimado = monto_estimado.replace(".","")
    monto_estimado = convertir_a_numero("ARS "+monto_estimado.replace(",","."))

    return monto_estimado

def cantidad_renglones_solicitadas(xl_renglones):
    """cargar excel de 'detalle de renglones',
    devuelve la lista completa de renglones solicitada por compras"""
    lista_values = open_excel(xl_renglones)
    lista_renglones = [renglon[0]  for renglon in lista_values if type(renglon[0]) == int] 

    return lista_renglones 

def renglones_desiertos(xl_recomendacion, xl_renglones ):
    """devuelve una lista de renglones desiertas: POR NO TENER OFERTAS.
    compara la lista de la funcion 'cantidad_renglones_solicitadas'
    y 'renglones_ofertadas'"""
    renglones_pedidos = cantidad_renglones_solicitadas(xl_renglones)
    lista_ofertas = renglones_ofertados_sin_opciones(renglones_ofertadas(xl_recomendacion))

    lista_desiertos = [] #
    # print(renglones_pedidos, lista_ofertas)

    for pedidos in renglones_pedidos:
        # time.sleep(0.1)
        try:
            lista_ofertas.index(pedidos)
        except:
            lista_desiertos.append(pedidos)

    print(lista_desiertos)

    return lista_desiertos

def renglones_ofertados_sin_opciones(lista_renglones):
    """devuelve una lista de renglones ofertadas por todas las empresas
    sin las opciones."""
    lista = {}
    for renglon in lista_renglones:
        if type(renglon)== int or type(renglon)== float:
            lista[int(renglon)]=True
        elif type(renglon) != int:
            lista[int(renglon.split(".")[0])] = True

    return list(lista.keys())


# GENERAR PROCESO PARA EL JSON #
def datos_contratacion(xl_recomendacion, xl_renglones):
    """toma datos basico de la contratacion del excel de recomendacion
    y del excel de renglones"""
    values = open_excel(xl_recomendacion)
    
    numero_contratacion = values[1][3].split(" ")[-1]
    
    ee_tipo_documento  = values[1][0].split(" ")[4].split("-")[0]
    ee_anio = values[1][0].split(" ")[4].split("-")[1]
    ee_num = values[1][0].split(" ")[4].split("-")[2]
    ee_reparticion = values[1][0].split("-")[6]
    numero_expediente = f'{ee_tipo_documento}-{ee_anio}-{ee_num}-GCABA-{ee_reparticion}'

    dia_apertura = values[1][9].split("/")[0].split(" ")[1]
    mes_apertura = values[1][9].split("/")[1]
    anio_apertura = values[1][9].split("/")[2]
    precio_estimado = monto_estimado(xl_renglones)
    
    datos = {
        "n_proceso":f"{numero_contratacion}",
        "expediente":f"{numero_expediente}",
        "fecha_apertura_dia":f"{dia_apertura}",
        "fecha_apertura_mes":f"{mes_apertura}",
        "fecha_apertura_anio":f"{anio_apertura}",
        "monto_estimado":f"{precio_estimado}"
        }

    return datos


def crear_plantillas_empresas(xl_recomendacion):
    """crea una lista de empresas de la contratacion y sus 
    propiedades para el json"""

    list_empresas = lista_empresas_cuit(xl_recomendacion)
    list_json  = []
    count = 0

    for empresa in list_empresas:
        nombre_empresa = list(empresa.keys())[0]
        print(nombre_empresa)        
        count += 1 

        renglones = renglones_ofrecidos_por_empresa(xl_recomendacion,count)
        adjudicados = renglones["adjudicados"]
        desestimados = renglones["desestimados"]

        precio_total = precio_total_x_empresa(xl_recomendacion,count )


        dict_empresa = {
                "empresa":nombre_empresa,
                "cuit": "",#cargan a mano
                "doc_complementaria": False,#cargan a mano
                "renglones_adjudicados":adjudicados,
                "renglones_desestimados":{
                    "administrativo":[],
                    "tecnicamente":[],
                    "economicamente":desestimados
                    },
                "precio_total": precio_total,
                "precio_total_letras": "",#cargan a mano
                "monto_anterior":"",
                "monto_anterior_letras":""
                
            }
        list_json.append(dict_empresa)

    return list_json

def crear_proceso(xl_recomendacion,xl_renglones):
    """guarda los datos basicos  de la contratacion en el json
    usando funciones del modulo 'read_excel'"""
    
    cantidad_empresas = len(lista_empresas(xl_recomendacion))
    datos_basicos = datos_contratacion(xl_recomendacion, xl_renglones)
    datos_empresas = crear_plantillas_empresas(xl_recomendacion)
    desiertas = renglones_desiertos(xl_recomendacion, xl_renglones)
    renglones_ofertadas(xl_recomendacion)
    precio_estimado = monto_estimado(xl_renglones)

    plantilla_contratacion = {
        f'{datos_basicos["n_proceso"]}':{
        "detalle":"",
        "expediente":datos_basicos["expediente"],
        "num_dispo":"",
        "informe_grafico":"",
        "num_dispo_adj":"",
        "fecha_publicacion":{"dia":"",
                        "mes":"",
                        "anio":""
                        },
        "monto_estimado":precio_estimado,
        "monto_estimado_letras":"",
        "monto_adjudicado":"",
        "monto_adjudicado_letras":"",
        "fecha_apertura":{"dia":datos_basicos["fecha_apertura_dia"],
                        "mes":datos_basicos["fecha_apertura_mes"],
                        "anio":datos_basicos["fecha_apertura_anio"]
                        },
        "fecha_final_consultas":{"dia":"",
                        "mes":"",
                        "anio":""
                        },
        "hora_apertura":{
            "horas":"10",
            "minutos":"00"
            },
        "firmas_interesadas":0,
        "firmas_confirmadas":cantidad_empresas,
        "desiertos":desiertas,
        "fracasados":"",
        "lista_empresas":datos_empresas
    }}
    return plantilla_contratacion

xl = recomendaciones["2243"]
xl2 = recomendaciones["2243_detalles"]
if __name__== "__main__":

    # no POO
    # crear_proceso(xl,xl2)


    # POO
    excel = LeerExcel(xl, xl2)
    excel.datos_contratacion()