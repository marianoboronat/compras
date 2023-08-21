import tkinter as tk
from tkinter import ttk

import read_excel, widgets, admin_json, json
from docxtpl import DocxTemplate
import os, time
import datetime

def fecha_actual():
    fecha_hoy = datetime.datetime.now()
    dia = fecha_hoy.strftime("%d")
    mes =fecha_hoy.strftime("%m")
    anio = fecha_hoy.strftime("%y")

    return dia, mes, anio

# construccion de texto
def generar_conjunto_de_renglones(lista):
    """genera una parte del texto para escribir un conjunto de renglones
    ej: 'para los renglones 1, 2 ,3, 4 y 5'"""
    cantidad_renglones = len(lista)
    lista.sort()

    txt = ""

    # print("cantidad de renglones",cantidad_renglones)
    count_cantidad = 0

    #si la lista solo tiene mas de un item
    if cantidad_renglones >1:
        txt +=  "para los renglones "
        # time.sleep(0.5)
        for renglon in lista: 
            count_cantidad +=1
            if len(str(renglon).split("."))>1:
                renglon_int = str(renglon).split(".")[0]
                renglon_float = str(renglon).split(".")[1]
                if count_cantidad == cantidad_renglones:                
                    txt +=  f"y {renglon_int} opción {renglon_float}; "
                elif count_cantidad == cantidad_renglones-1:
                    txt +=  f"{renglon_int} opción {renglon_float} "
                else:
                    txt +=  f"{renglon_int} opción {renglon_float}, "
            else:
                if count_cantidad == cantidad_renglones:                
                    txt +=  "y "+str(renglon)+"; "
                elif count_cantidad == cantidad_renglones-1:
                    txt +=  str(renglon)+" "
                else:
                    txt +=  str(renglon)+", "

            # print(renglon)           

    #si la lista solo tiene un item        
    elif cantidad_renglones == 1:
        
        txt +=  "para el renglón "+str(lista[0])+"; "
    # print("texto:",txt)
    return txt


class Considerando:
    def __init__(self, contratacion):
        """genera texto de la parte del considerando"""
        #parameters
        self.contratacion = contratacion
        self.parameters = widgets.open_json("bd/parametros.json")

        #datos basicos de la contratacion
        self.datos_basicos = admin_json.datos_basicos_contratacion(self.contratacion)
        self.datos_x_empresa = admin_json.lista_empresas_con_datos_completos(self.contratacion)

        #propiedades de la contratacion
        self.doc_complementaria = admin_json.cantidad_documentacion_complementaria(self.contratacion)  
        self.desestimacion_admin = admin_json.cantidad_desestimaciones_admin(self.contratacion)    
        self.renglones_fracasados = admin_json.renglones_fracasados(self.contratacion)

    def empresas_presentadas(self):
        """genera texto para el parrafo de la presentacion de empresas
        para la parte de considerando"""
        
        dia_publicacion = self.datos_basicos["fecha_apertura"]["dia"]
        mes_publicacion = widgets.MESES[int(self.datos_basicos["fecha_apertura"]["mes"])-1]
        anio_publicacion = self.datos_basicos["fecha_apertura"]["anio"]


        txt_final = f"Que el día {dia_publicacion} de {mes_publicacion} de {anio_publicacion} a las 10:00 horas, operó la apertura de ofertas, habiendo presentado propuestas "
        
        lista_completa = admin_json.lista_empresas_con_datos_completos(self.contratacion)
        cantidad = len(lista_completa)
        count = 0

        if cantidad > 1:
            txt_final += "las firmas "
            for renglon in lista_completa:
                count += 1
                cuit = renglon["cuit"][:2]+"-"+renglon["cuit"][2:-1]+"-"+renglon["cuit"][-1]
                if count == cantidad:
                    txt_final +=  f'y {renglon["empresa"].upper()} (CUIT N° {cuit})' 
                elif count == cantidad-1:
                    txt_final +=  f'{renglon["empresa"].upper()} (CUIT N° {cuit}) ' 
                else:                
                    txt_final +=  f'{renglon["empresa"].upper()} (CUIT N° {cuit}), '
        
        elif cantidad ==1:
            txt_final += f' la firma {lista_completa[0]["empresa"].upper()} (CUIT N° {lista_completa[0]["cuit"][:2]+lista_completa[0]["cuit"][2:-1]+lista_completa[0]["cuit"][-1]}) ' 
        
        txt_final +=  " habiéndose generado el Acto de Apertura correspondiente, en cumplimiento de la normativa vigente;"
        print(txt_final)
        return txt_final    

    def documentacion_complementaria(self):
        """genera texto para el parrafo de la documentacion complementaria
        para la parte de considerando"""
        txt_final = ""    
        
        # datos
        lista_completa = self.doc_complementaria  
        cantidad = len(lista_completa)

        # si hay mas de una empresa qu ese le solicito doc complementaria
        if cantidad > 1:
            txt_final += "Que se solicitó documentación complementaria administrativa y/o técnica a las firmas "
            count = 0
            for renglon in lista_completa:
                empresa = list(renglon.keys())[0]                
                cuit = renglon[empresa][:2]+"-"+renglon[empresa][2:-1]+"-"+renglon[empresa][-1]

                print("renglon: ",empresa,cuit)
                count += 1
                if count == cantidad:
                    txt_final +=  f'y {empresa.upper()} (CUIT N° {cuit})' 
                elif count == cantidad-1:
                    txt_final +=  f'{empresa.upper()} (CUIT N° {cuit}) ' 
                else:                
                    txt_final +=  f'{empresa.upper()} (CUIT N° {cuit}), '
            txt_final+=";"

            print(txt_final)
            return txt_final  
        # si hay solo una empresa a la que se le solicito doc complementaria
        elif cantidad ==1:
            
            empresa = list(lista_completa[0].keys())[0]     
            cuit = lista_completa[0][empresa]  
            txt_final += f"Que se solicitó documentación complementaria administrativa y/o técnica a la firma {empresa} (CUIT N° {cuit[:2]+'-'+cuit[2:-1]+'-'+cuit[-1]});"
            print(txt_final)
            return txt_final    
        else:
            return None

    def desestimar_admin(self):
        """genera texto para el parrafo de la documentacion complementaria
        para la parte de considerando"""
        txt_final = ""    
        
        # datos
        lista_completa = self.desestimacion_admin 
        cantidad = len(lista_completa)

        # si hay mas de una empresa qu ese le solicito doc complementaria
        if cantidad > 1:
            txt_final += "Que corresponde desestimar las propuestas por razones administrativas a las firmas "
            count = 0
            for renglon in lista_completa:
                empresa = list(renglon.keys())[0]
                cuit = renglon[empresa][:2]+"-"+renglon[empresa][2:-1]+"-"+renglon[empresa][-1]
                # print(empresa,cuit)
                count += 1
                if count == cantidad:
                    txt_final +=  f'y {empresa.upper()} (CUIT N° {cuit})' 
                elif count == cantidad-1:
                    txt_final +=  f'{empresa.upper()} (CUIT N° {cuit}) ' 
                else:                
                    txt_final +=  f'{empresa.upper()} (CUIT N° {cuit}), '
            txt_final+=" para la totalidad de los renglones;"

            print(txt_final)
            return txt_final  
        # si hay solo una empresa a la que se le solicito doc complementaria
        elif cantidad ==1:
            
            empresa = list(lista_completa[0].keys())[0]     
            cuit = lista_completa[0][empresa]  
            txt_final += f"Que corresponde desestimar las propuestas por razones administrativas a la firma {empresa} (CUIT N° {cuit[:2]+'-'+cuit[2:-1]+'-'+cuit[-1]}) para la totalidad de los renglones;"
            print(txt_final)
            return txt_final    
        else:
            return None

    def desestimar_tecnicamente(self):
        """genera el texto para los renglones desestimados tecnicamente"""
        txt = "Que corresponde desestimar las ofertas, por no cumplir técnicamente con lo solicitado, de las firmas de "
        empresas = self.datos_x_empresa

        # calcula la cantidad de empresas desestimadas tecnicamente
        cantidad_empresas_deses_tec = len([x for x in empresas if len(x["renglones_desestimados"]["tecnicamente"])>0])
        
        if cantidad_empresas_deses_tec > 1:
            # print("desestimar tecnicamente multiples empresas")

            # itera todas las empresas
            for em in empresas:
                # print(em)
                # seleccionar solo las empresas que tengan 1 o mas 
                # renglones desestimados tecnicamente
                if len(em["renglones_desestimados"]["tecnicamente"]) >0:
                    # print(em)
                    empresa_nombre = em["empresa"]                    
                    empresa_cuit = em["cuit"][:2]+"-"+em["cuit"][2:-1]+"-"+em["cuit"][-1]     

                    renglones_desestimados= em["renglones_desestimados"]["tecnicamente"]
                    cantidad_desestimados = len(renglones_desestimados)
                    renglones_desestimados.sort()
                    txt += f"{empresa_nombre} (CUIT N° {empresa_cuit}), {generar_conjunto_de_renglones(renglones_desestimados)}"

                    
                    # print(empresa_nombre,empresa_cuit,renglones_desestimados, cantidad_desestimados)
            print(txt)
            return txt
        
        elif cantidad_empresas_deses_tec ==1:
            # print("desestimar tecnicamente solo uno")

            for em in empresas:
                # print(em)
                # seleccionar solo las empresas que tengan 1 o mas 
                # renglones desestimados tecnicamente
                if len(em["renglones_desestimados"]["tecnicamente"]) >0:
                    # print(em)
                    empresa_nombre = em["empresa"]
                    empresa_cuit = em["cuit"][:2]+"-"+em["cuit"][2:-1]+"-"+em["cuit"][-1]                
                    renglones_desestimados= em["renglones_desestimados"]["tecnicamente"]
                    cantidad_desestimados = len(renglones_desestimados)
                    renglones_desestimados.sort()
                    txt += f"{empresa_nombre} (CUIT N° {empresa_cuit}), {generar_conjunto_de_renglones(renglones_desestimados)}"
                    # print(empresa_nombre,empresa_cuit,renglones_desestimados, cantidad_desestimados)
            
            print(txt)
            return txt
        else:
            return None

    def desestimar_economicamente(self):
        """genera el texto para los renglones desestimados economicamente"""
        txt = ""
        empresas = self.datos_x_empresa

        # calcula la cantidad de empresas desestimadas economicamente
        cantidad_empresas_deses_tec = len([x for x in empresas if len(x["renglones_desestimados"]["economicamente"])>0])
        
        if cantidad_empresas_deses_tec > 1:
            txt += "Que corresponde desestimar las ofertas, por no cumplir económicamente con lo solicitado, de las firmas de "
            # print("desestimar economicamente multiples empresas")

            # itera todas las empresas
            for em in empresas:
                # print(em)
                # seleccionar solo las empresas que tengan 1 o mas 
                # renglones desestimados economicamente
                if len(em["renglones_desestimados"]["economicamente"]) >0:
                    # print(em)
                    empresa_nombre = em["empresa"]
                    empresa_cuit = em["cuit"][:2]+"-"+em["cuit"][2:-1]+"-"+em["cuit"][-1]             
                    renglones_desestimados= em["renglones_desestimados"]["economicamente"]
                    cantidad_desestimados = len(renglones_desestimados)
                    renglones_desestimados.sort()
                    txt += f"{empresa_nombre} (CUIT N° {empresa_cuit}), {generar_conjunto_de_renglones(renglones_desestimados)}"

                    
                    # print(empresa_nombre,empresa_cuit,renglones_desestimados, cantidad_desestimados)
            print(txt)
            return txt
        elif cantidad_empresas_deses_tec ==1:
            # print("desestimar economicamente solo uno")
            txt += "Que corresponde desestimar las ofertas, por no cumplir económicamente con lo solicitado, de la firma de "

            for em in empresas:
                # print(em)
                # seleccionar solo las empresas que tengan 1 o mas 
                # renglones desestimados economicamente
                if len(em["renglones_desestimados"]["economicamente"]) >0:
                    # print(em)
                    empresa_nombre = em["empresa"]
                    empresa_cuit = em["cuit"][:2]+"-"+em["cuit"][2:-1]+"-"+em["cuit"][-1]            
                    renglones_desestimados= em["renglones_desestimados"]["economicamente"]
                    cantidad_desestimados = len(renglones_desestimados)
                    renglones_desestimados.sort()
                    txt += f"{empresa_nombre} (CUIT N° {empresa_cuit}), {generar_conjunto_de_renglones(renglones_desestimados)}"
            
            print(txt)
            return txt
        else:
            return None
                    
                    # print(empresa_nombre,empresa_cuit,renglones_desestimados, cantidad_desestimados)

    def desiertas(self):
        """genera texto para el parrafo de los renglones desiertos
        para la parte de considerando"""
        txt_final = ""    
        
        # datos
        lista_completa = self.datos_basicos["desiertos"]
        cantidad = len(lista_completa)

        if cantidad > 1:
            txt_final += "Que corresponde declarar desiertos los renglones "
            count = 0
            for renglon in lista_completa:
                # print(renglon)
                count += 1
                if count == cantidad:
                    txt_final +=  f' y {renglon};' 
                elif count == cantidad-1:
                    txt_final +=  f'{renglon}' 
                else:                
                    txt_final +=  f'{renglon}, '
            
            print(txt_final)
            return txt_final
        elif cantidad ==1:
            txt_final += f"Que corresponde declarar desierto el renglón {lista_completa[0]}"
            print(txt_final)
            return txt_final
        else:
            #si no hay renglones fracasados que devuelva nada
            return None

    def fracasado(self):
        """genera texto para el parrafo de los renglones fracasados
        para la parte de considerando"""
        txt_final = ""    
        
                # datos["fracasados"] = renglones_fracasados(contratacion)
        # datos
        lista_completa = self.renglones_fracasados
        cantidad = len(lista_completa)

        if cantidad > 1:
            txt_final += "Que corresponde declarar fracasados los renglones "
            count = 0
            for renglon in lista_completa:
                # print(renglon)
                count += 1
                if count == cantidad:
                    txt_final +=  f' y {renglon}' 
                elif count == cantidad-1:
                    txt_final +=  f'{renglon}' 
                else:                
                    txt_final +=  f'{renglon}, '
            txt_final+=";"

            print(txt_final)
            return txt_final 
        elif cantidad ==1:
            txt_final += f"Que corresponde declarar fracasado el renglón {lista_completa[0]};"

            print(txt_final)
            return txt_final 
        else:
            #si no hay renglones fracasados que devuelva nada
            return None

    def adjudicaciones(self):
        """crea el parrafo de las adjudicaciones"""
        informe_grafico = self.datos_basicos["informe_grafico"]
        empresas = self.datos_x_empresa
        # print(empresas)
        txt= f"Que se emitió la recomendación en base al informe técnico {informe_grafico}, por el cual se recomendó la adjudicación "

        for empresa in empresas:
            # print(empresa)
            #se toman las empresas que tienen adjudicaciones
            if len(empresa["renglones_adjudicados"])>0:
                nombre_em = empresa["empresa"].upper()
                cuit = empresa["cuit"][:2]+"-"+empresa["cuit"][2:-1]+"-"+empresa["cuit"][-1]    

                precio_total = read_excel.agregar_comas_precio(empresa["precio_total"])
                precio_total_letras = empresa["precio_total_letras"].upper()
                renglones_adjudicados = empresa["renglones_adjudicados"]
                renglones_adjudicados.sort()
                cantidad_adjudicados = len(renglones_adjudicados)

                
                txt += f"para la firma {nombre_em} (CUIT N° {cuit}) "

                #si existe MAS DE un renglon
                if cantidad_adjudicados>1:
                    txt +="para los renglones "

                    count_renglon = 0
                    txt += " ".join(generar_conjunto_de_renglones(renglones_adjudicados).split(" ")[3:])

                elif cantidad_adjudicados==1:
                    txt +="para el renglón "

                    count_renglon = 0
                    #se iteran los renglones adjudicados y se agregan al txt
                    for renglon in renglones_adjudicados:
                        txt += f"{renglon} "
                        

                txt += f"por la suma de PESOS {precio_total_letras} (${precio_total}); "

            
        txt += f"""por ajustarse a los pliegos que rigen la contratación y ser las ofertas más convenientes, al amparo de lo establecido en el Artículo {self.parameters['art_seleccion_ofertas']}-Criterio de selección de las Ofertas- de la Ley N° 2.095 (texto consolidado por Ley N° {self.parameters['ley']});"""
        print(txt)
        return txt

    def texto(self):
        """genera el texto de considerando"""
        txt = ""
        lista = [
        self.empresas_presentadas(),
        self.documentacion_complementaria(),
        self.desestimar_admin(),
        self.desestimar_tecnicamente(),
        self.desestimar_economicamente(),
        self.desiertas(),
        self.fracasado(),
        self.adjudicaciones()
        ]

        for textos in lista:
            if textos != None:
                txt += f"\n\n{textos}"

        # print(txt)
        return txt

class Dispone:
    def __init__(self, contratacion):
        
        """genera texto de la parte del dispone"""
        self.contratacion = contratacion
        self.datos = admin_json.datos_basicos_contratacion(contratacion)        
        self.list_empresas = admin_json.lista_empresas_con_datos_completos(contratacion)
        self.parameters = widgets.open_json("bd/parametros.json")


        self.renglones_fracasados = admin_json.renglones_fracasados(self.contratacion)

        self.articulo = 0

    def primer_parrafo(self):
        """Escribir el articulo 1 del dispone"""

        txt = f'Apruébese la Contratación Menor Nº {self.contratacion}, realizada al amparo de lo establecido en el artículo {self.parameters["art_cme"]} de la Ley Nº 2.095 (Texto consolidado por Ley N° {self.parameters["ley"]}) y el Decreto Reglamentario Nº {self.parameters["decreto_reglamentario"]} gestionada bajo el Sistema Buenos Aires Compras (BAC), en el marco de lo dispuesto por el artículo {self.parameters["art_informatizacion_contrataciones"]} –Informatización de las Contrataciones- “{self.datos["detalle"]} para el Hospital General de Agudos Dra. Cecilia Grierson” dependiente del Ministerio de Salud del Gobierno de la Ciudad Autónoma de Buenos Aires.'
        return txt

    def desestimaciones(self):    
        """Escribir el articulo 2 del dispone: DESESTIMACIONES"""
        txt= ""

        #calcula la cantidad de empresas que tienen desestimaciones
        cantidad_desestimadas = admin_json.cant_empresas_totales_con_desestimaciones(self.contratacion)
        
        if cantidad_desestimadas != 0:
            if cantidad_desestimadas > 1:
                txt += "Desestímese las ofertas de las firmas "
            elif cantidad_desestimadas == 1:
                txt += "Desestímese las ofertas de la firma "

            for empresa in self.list_empresas:
                nombre_empresa = empresa["empresa"]
                cuit = empresa["cuit"][:2]+"-"+empresa["cuit"][2:-1]+"-"+empresa["cuit"][-1] 
                lista_deses = admin_json.renglones_totales_desestimados_x_empresa(self.contratacion,nombre_empresa)
                cantidad_deses = len(lista_deses)

                if cantidad_deses > 1:
                # print(empresas,lista_deses, cantidad_deses)
                    txt += f"{nombre_empresa} (CUIT N° {cuit}) {generar_conjunto_de_renglones(lista_deses)}"

                elif cantidad_deses ==1:
                    txt += f"{nombre_empresa} (CUIT N° {cuit}) {generar_conjunto_de_renglones(lista_deses)}"

            # print(txt)
            txt +=" por las razones expuestas en el considerando;"
            return txt
        else:
            # print("no hay empresas con desestimaciones")
            return None

    def desiertos(self):
        """parrafo de renglones desiertos"""
        """genera texto para el parrafo de los renglones desiertos
        para la parte de dispone"""
        txt_final = ""    
        
        # datos
        lista_completa = self.datos["desiertos"]
        lista_completa.sort()
        cantidad = len(lista_completa)

        if cantidad > 1:
            txt_final += "Declárese desiertos los renglones "
            count = 0
            for renglon in lista_completa:
                # print(renglon)
                count += 1
                if count == cantidad:
                    txt_final +=  f' y {renglon};' 
                elif count == cantidad-1:
                    txt_final +=  f'{renglon}' 
                else:                
                    txt_final +=  f'{renglon}, '
            
            print(txt_final)
            return txt_final
        elif cantidad ==1:
            txt_final += f"Declárese desierto el renglón {lista_completa[0]}"
            print(txt_final)
            return txt_final
        else:
            #si no hay renglones fracasados que devuelva nada
            return None

    def fracasados(self):
        """genera texto para el parrafo de los renglones fracasados
        para la parte de considerando"""
        txt_final = ""    
        
                # datos["fracasados"] = renglones_fracasados(contratacion)
        # datos
        lista_completa = self.renglones_fracasados
        cantidad = len(lista_completa)

        if cantidad > 1:
            txt_final += "Declárese fracasados los renglones "
            count = 0
            for renglon in lista_completa:
                # print(renglon)
                count += 1
                if count == cantidad:
                    txt_final +=  f' y {renglon}' 
                elif count == cantidad-1:
                    txt_final +=  f'{renglon}' 
                else:                
                    txt_final +=  f'{renglon}, '
            txt_final+=";"

            print(txt_final)
            return txt_final 
        elif cantidad ==1:
            txt_final += f"Declárese fracasado el renglón {lista_completa[0]};"

            print(txt_final)
            return txt_final 
        else:
            #si no hay renglones fracasados que devuelva nada
            return None

    def adjudicaciones(self):
        """Escribir el articulo 5 del dispone: ADJUDICACIONES"""

        txt = f'Adjudicase por un monto total de PESOS {self.datos["monto_adjudicado_letras"].upper()} (${read_excel.agregar_comas_precio(float(self.datos["monto_adjudicado"]))}.-), al amparo de lo establecido en el Artículo {self.parameters["art_seleccion_ofertas"]} –Criterio de selección de las Ofertas- de la Ley Nº 2095 (Texto Consolidado por Ley N° {self.parameters["ley"]}), conforme al siguiente detalle:'
        return txt

    def tabla_adjudicaciones(self):
        """crea la lista de datos para iterar en la tabla
        del dispone"""
        empresas = self.list_empresas
        lista_final = []

        for datos in empresas:
            nombre = datos["empresa"]
            cuit = datos["cuit"][:2]+"-"+datos["cuit"][2:-1]+"-"+datos["cuit"][-1] 
            monto_total_adj = read_excel.agregar_comas_precio(datos["precio_total"])      
            # print(monto_total_adj)

            renglones_adj = datos["renglones_adjudicados"]        
            cantidad_renglones = len(renglones_adj)
            
            if cantidad_renglones >0:
                txt_renglon = ""
                
                if cantidad_renglones == 1:            
                    txt_renglon = f"{renglones_adj[0]}"
                    datos_empresa = [nombre, cuit,txt_renglon, monto_total_adj]
                    lista_final.append(datos_empresa)
                else:            
                    # print(nombre,cuit,monto_total_adj)

                    count_renglon = 0
                    #se iteran los renglones adjudicados y se agregan al txt
                    for renglon in renglones_adj:
                        
                        count_renglon += 1
                        txt_renglon = "".join(" ".join(generar_conjunto_de_renglones(renglones_adj).split(" ")[3:]).split(";"))
                    # print(txt_renglon)
                    
                    datos_empresa = [nombre, cuit,txt_renglon, monto_total_adj]
                    lista_final.append(datos_empresa)
        
        # print(lista_final)
        return lista_final

    def texto_1(self):
        """genera los parrafos del dispone arriba de la tabla"""
        txt= ""
        lista_parrafos = [
            self.primer_parrafo(),
            self.desestimaciones(),
            self.desiertos(),
            self.fracasados(),
            self.adjudicaciones()
        ]
        for textos in lista_parrafos:
            if textos != None:
                self.articulo+=1
                txt += f"\n\nArtículo {self.articulo}°: {textos}"

        # print(txt)
        return txt

    def texto_2(self):
        """genera los parrafos del dispone debajo de la tabla"""
        txt =f"""Artículo {self.articulo+1}°: La erogación que demande la presente gestión será imputada a la correspondiente partida presupuestaria del ejercicio presente.\n
Artículo {self.articulo+2}°: Autorizase al Hospital Gral. De Agudos “Dra. Cecilia Grierson” a emitir las respectivas Órdenes de Compras.\n
Artículo {self.articulo+3}°: Publíquese y, para su conocimiento y demás efectos, pase a la Dirección General Administrativa Contable."""
        return txt

    # generar archivo

class GenerateDocument:
    def __init__(self,contratacion):
        # parameters
        self.contratacion = contratacion

        #propiedades del documento
        self.document_name = f"DISPFC{''.join(self.contratacion.split('-'))}.docx"
        self.path = ""
        self.file_template = "templates/DISPOADJUDICACION_CME.docx"

        #datos
        # seccion considerando
        self.considerando = Considerando(self.contratacion)

        # seccion dispone
        self.dispone = Dispone(self.contratacion)

    def cantidad_firmas_txt(self, interesadas, confirmadas ):
        txt = ""
        if int(interesadas) > 1:
            txt += f"{widgets.numero_letras[int(interesadas)]} ({interesadas}) firmas interesadas,"
        elif int(interesadas) ==1:
            txt += f"una (1) firma interesada,"
        
        if int(confirmadas) > 1:
            txt += f" encontrándose confirmadas {widgets.numero_letras[int(confirmadas)]} ({confirmadas}) ofertas en el citado Sistema;"
        elif int(confirmadas) ==1:            
            txt += f" encontrándose confirmada una (1) oferta en el citado Sistema;"
        return txt

    def contexto(self):
        datos_contratacion = admin_json.datos_basicos_contratacion(self.contratacion)
        datos_parametros = widgets.open_json("bd/parametros.json")
        expendiente = datos_contratacion["expediente"].split("-")
        cantidad_firmas = self.cantidad_firmas_txt(datos_contratacion["firmas_interesadas"],datos_contratacion["firmas_confirmadas"])

        contexto = {
            "anio": datos_parametros["anio"],
            "ley": datos_parametros["ley"],
            "decreto_reglamentario": datos_parametros["decreto_reglamentario"],

            "dia_apertura":datos_contratacion["fecha_apertura"]["dia"] ,
            "mes_apertura":widgets.MESES[int(datos_contratacion["fecha_apertura"]["mes"])-1], 
            "anio_apertura":datos_contratacion["fecha_apertura"]["anio"],
            "detalle":datos_contratacion["detalle"],            
            "detalle_mayusc":datos_contratacion["detalle"].upper(),
            "contratacion":self.contratacion,

            "expediente":expendiente[2],
            "ee_anio":expendiente[1],
            "ee_reparticion":expendiente[-1],

            "informe_grafico":datos_contratacion["informe_grafico"],            
            "num_dispo":datos_contratacion["num_dispo"],
            "monto_estimado":read_excel.agregar_comas_precio(datos_contratacion["monto_estimado"]),
            "monto_estimado_letras":datos_contratacion["monto_estimado_letras"].upper(),
            "monto_adjudicado":read_excel.agregar_comas_precio(float(datos_contratacion["monto_adjudicado"])),
            "monto_adjudicado_letras":datos_contratacion["monto_adjudicado_letras"].upper(),

            "cantidad_firmas":cantidad_firmas,
            "considerando":self.considerando.texto(),
            "dispone_1":self.dispone.texto_1(),
            "tabla":self.dispone.tabla_adjudicaciones(),
            "dispone_2":self.dispone.texto_2()
        }

        return contexto

    def create_word_file(self):
        """genera el documento word"""
        document = DocxTemplate(self.file_template)
        document.render(self.contexto())

        document.save(f"{self.path}{self.document_name}")
        #abrir el documento automaticamente
        os.startfile(f"{self.path}{self.document_name}")


if __name__== "__main__":
    contratacion = "455-2053-CME20"


    # considerando = Considerando(contratacion)
    # considerando.documentacion_complementaria()

    documento = GenerateDocument(contratacion)
    print(admin_json.cant_empresas_totales_con_desestimaciones(contratacion))
    documento.create_word_file()

