import json
import read_excel as xl

import time

file = "bd/contrataciones.json"



plantilla_contratacion = {
    "detalle":"",
    "expediente":"",
    "num_dispo":"",
    "monto_estimado":"",
    "monto_estimado_letras":"",
    "monto_adjudicado":"",
    "monto_adjudicado_letras":"",
    "fecha_apertura":{"dia":"","mes":"","anio":""},    
    "fecha_final_consultas":{"dia":"","mes":"","anio":""},
    "firmas_interesadas":0,
    "firmas_confirmadas":0,
    "desiertos":[],
    "fracasados":[],
    "lista_empresas":[]
}

# renglon = ["numero", partida, cantidad, precio_u]
renglon = {
    "numero" :1,
    "opcion":1,
    "cantidad":1,
    "unidades":"unidad",
    "precio_unitario":1560
}

# dentro de la plantilla contratacion en lista empresas
plantilla_empresas = {
    "empresa":{
        "cuit": "",#cargan a mano
        "doc_complementaria": False,#cargan a mano
        "renglones_adjudicados":[],
        "renglones_desestimados":None,
        "precio_total": None,
        "precio_total_letras": None#cargan a mano
        }
    }

#dentro de la plantilla de empresas, en 'desestimados'
desestimados = {
    "administrativo":[],
    "tecnicamente":[],
    "economicamente":[]
    }

class JsonAdmin:
    def __init__(self, xl_recomendacion, xl_renglones):
        """una clase que gestiona el json"""
        self.xl_recomendacion = xl_recomendacion
        self.xl_renglones = xl_renglones

        self.excel = xl.LeerExcel(self.xl_recomendacion, self.xl_renglones)
        self.file = "bd/contrataciones.json"
        self.values = self.open_json(self.file)

        # el numero de contratacion es tomado desde el objeto 'self.excel'
        self.contratacion = self.excel.datos_contratacion()["n_proceso"]

    def open_json(self,file):
        """abre los archivos json para su lectura"""
        with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
            main_objeto = json.load(json_file) #LA VARIABLE 'datos' ABRE EL OBJETO JSON DEL ARCHIVO 'json_file'
            return main_objeto

    def save_json_values(self,file, values):
        # data = open_json(file)
        with open(file, "w", encoding='utf8') as outfile:
            json.dump(values, outfile, sort_keys = False, indent = 2, ensure_ascii=False)
        
        self.values = self.open_json(self.file)


    def modificar_datos_empresa(self, empresa, data):
        with open(self.file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
            values = json.load(json_file)
        # print(values)

        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["empresa"] = data["empresa"]
                        values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["cuit"] = data["cuit"]
                        values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["doc_complementaria"] = data["doc_complementaria"]
                        values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["precio_total_letras"] = data["precio_total_letras"]

                        # saving
                        with open(self.file, "w", encoding='utf8') as outfile:
                            json.dump(values, outfile, sort_keys = False,
                                    indent = 2, ensure_ascii=False)
                    
                    count_empresa +=1
            count_contrataciones+=1

    def cantidad_documentacion_complementaria(self):
        """ devuelve las empresas a las que se les solicito
        documentacion complementaria.
        devuelve una lista de dictionarios, cuyas keys son 
        el nombre de la empresa y su valor el n° de cuit
        ej: [{'empresa':'12-12345678-1'}, ...]"""
        final = [] 

        for x in self.values:
            if list(x.keys())[0] == contratacion:
                lista_empresas = x[contratacion]["lista_empresas"]
                count_em = 0
                for y in lista_empresas:
                    count_em+=1
                    if y["doc_complementaria"] == True:
                        final.append({y["empresa"]:y["cuit"]})
                # print(lista_empresas)

        # print(final)
        return final

    def cantidad_desestimaciones_admin(self):
        """ devuelve las empresas que se desestimaron administrativamente.
        devuelve una lista de dictionarios, cuyas keys son 
        el nombre de la empresa y su valor el n° de cuit
        ej: [{'empresa':'12-12345678-1'}, ...]"""
        final = []
        for x in self.values:
            if list(x.keys())[0] == self.contratacion:
                lista_empresas = x[self.contratacion]["lista_empresas"]
                count_em = 0
                for y in lista_empresas:
                    count_em+=1
                    if len(y["renglones_desestimados"]["administrativo"]) > 0:
                        final.append({y["empresa"]:y["cuit"]})
                # print(lista_empresas)

        # print(final)
        return final

    def documentacion_complementaria(self,  empresa, complementaria):
        """ FALTA DESCRIPCION
        empresa -> (str) nombre empresa
        complementaria -> (str) True/false"""

        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == contratacion:
                list_empresas = contrataciones[contratacion]["lista_empresas"]
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                for item_empresa in list_empresas:                
                    nombre_empresa = item_empresa["empresa"]
                    if nombre_empresa == empresa:
                        doc_complementaria = self.values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["doc_complementaria"]

                        #para luego pasar a administrativo
                        self.values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["doc_complementaria"] = complementaria

                        # saving
                        self.save_json_values(self.file, self.values)
                    
                    count_empresa +=1
            count_contrataciones+=1

    # Desestimaciones
    def desestimar_administrativamente(self, empresa):
        """junta todos los renglones desestimados tecnicas y economicamente
        y los pasa a administrativos"""

        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        # pass

                        lista_desestimados = []          
                        administrativo = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"]
                        economicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                        tecnicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                        
                        # se juntan todas las desestimaciones en economicos
                        lista_desestimados.extend(administrativo)
                        lista_desestimados.extend(economicos) 
                        lista_desestimados.extend(tecnicos) 

                        #para luego pasar a administrativo
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"] = lista_desestimados
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = []
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = []
                        # print(values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"])

                        # saving
                        self.save_json_values(self.file,self.values)
                        # print(administrativo)
                    
                    count_empresa +=1
            count_contrataciones+=1
    
    def desestimar_economicamente(self,empresa):
        """junta todos los renglones desestimados tecnicas y administrativa
        y los pasa a economicos"""
        

        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        # pass

                        lista_desestimados = []          
                        administrativo = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"]
                        economicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                        tecnicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                        
                        # se juntan todas las desestimaciones en economicos
                        lista_desestimados.extend(administrativo)
                        lista_desestimados.extend(economicos) 
                        lista_desestimados.extend(tecnicos) 

                        #para luego pasar a administrativo
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = lista_desestimados
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"] = []
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = []
                        # print(values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"])

                        # saving
                        self.save_json_values(self.file, self.values)
                        # print(administrativo)
                    
                    count_empresa +=1
            count_contrataciones+=1

    # eliminar renglones de economicos y tecnicos
    def eliminar_renglones_economicos(self, empresa, lista_renglones):
        """elimina items especificados en la 'lista de renglones'
        de la lista de economicos"""
        
        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                # para buscar la empresa seleccionada
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        economicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                        
                        #iterara la lista de renglones seleccionados
                        for item in lista_renglones:
                            print("eliminando renglon de economico",type(item),item)
                            try:
                                if len(item.split(".")) == 1:
                                    economicos.remove(int(item))
                                else:                                
                                    economicos.remove(float(item))
                            except Exception as e:
                                print(e,"no existen estos items en la lista de economicos")

                        print(empresa,economicos)
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = economicos
                        # saving

                        self.save_json_values(self.file,self.values )
                    
                    count_empresa +=1
            count_contrataciones+=1

    def eliminar_renglones_tecnicos(self, empresa, lista_renglones):
        """elimina items especificados en la 'lista de renglones'
        de la lista de tecnicos"""
        
        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                # para buscar la empresa seleccionada
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        tecnicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                        
                        #iterara la lista de renglones seleccionados
                        for item in lista_renglones:
                            print(item)
                            try:
                                if len(item.split(".")) == 1:
                                    tecnicos.remove(int(item))
                                else:                                
                                    tecnicos.remove(float(item)) 
                            except Exception as e:
                                print(e,"no existen estos items en la lista de 'tecnicos'")

                        print(empresa,tecnicos)
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = tecnicos
                        # saving
                        self.save_json_values(self.file,self.values)
                    
                    count_empresa +=1
            count_contrataciones+=1

    def agregar_renglones_economicos(self, empresa, lista_renglones):
        """agrega a la lista de desestimaciones economicas renglones
        especificados en la lista_renglones"""

        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                # para buscar la empresa seleccionada
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        economicos = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                        
                        #iterara la lista de renglones seleccionados
                        for item in lista_renglones:
                            print(item)
                            try:
                                if len(item.split(".")) == 1:
                                    economicos.append(int(item))
                                else:                                
                                    economicos.append(float(item)) 
                            except Exception as e:
                                print(e,"no existen estos items en la lista de economicos")

                        print(empresa,economicos)
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = economicos
                        # saving
                        self.save_json_values(self.file, self.values)
                    
                    count_empresa +=1
            count_contrataciones+=1

    def agregar_renglones_tecnicas(self, empresa, lista_renglones):
        """agrega a la lista de desestimaciones economicas renglones
        especificados en la lista_renglones"""


        # se iteran todas la contrataciones cargadas
        count_contrataciones = 0
        for contrataciones in self.values:
            # print(contrataciones)
            # se busca con el condicional seleccionar solo la contratacion buscada
            if  list(contrataciones.keys())[0] == self.contratacion:
                list_empresas = contrataciones[self.contratacion]["lista_empresas"]
                # print(list_empresas)
                count_empresa = 0 # para calcular el indice donde se ubica la empresa

                # se iteran todos los items de la propiedad 'lista_empresas'
                # para buscar la empresa seleccionada
                for item_empresa in list_empresas:                
                    # print(item_empresa)
                    nombre_empresa = item_empresa["empresa"]
                    # print(des_economicos,nombre_empresa)
                    if nombre_empresa == empresa:
                        tecnicas = self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                        
                        #iterara la lista de renglones seleccionados
                        for item in lista_renglones:
                            print("agregando a tecnicos",type(item),item)
                            try:
                                # agregar renglones a la lista de 'tecnicos'
                                if len(item.split(".")) == 1:
                                    tecnicas.append(int(item))
                                else:                                
                                    tecnicas.append(float(item)) 
                            except Exception as e:
                                print(e,"no existen estos items en la lista de economicos")

                        print(empresa,tecnicas)
                        self.values[count_contrataciones][self.contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = tecnicas
                        # saving
                        self.save_json_values(self.file, self.values)
                    
                    count_empresa +=1
            count_contrataciones+=1

    def monto_total_adjudicado(self):
        """suma todos los precios totales de las empresas"""
        values = self.lista_empresas_con_datos_completos()
        
        precio_total = 0.0
        for precio in values:
            precio_total+=precio["precio_total"]
            
        return precio_total
    
    def renglones_total_adjudicados(self):
        """devuelve una lista con todos los renglones adjudicados"""

        renglones_ad = []
        for contrataciones_ in self.values:
            if list(contrataciones_.keys())[0] == self.contratacion:
                for empresa  in contrataciones_[self.contratacion]["lista_empresas"]:
                    renglones_ad += empresa["renglones_adjudicados"]

        renglones_ad.sort()
        return renglones_ad

    def renglones_totales_desestimados(self):
        """devuelve una lista con todos los renglones desestimados(en cualquier forma)
        de todas las empresas de la contratacion"""
        lista_empresas = self.lista_empresas_con_datos_completos()
        lista_desestimados = {}

        # obtiene los renglones desestimados de la empresa
        for empresa in lista_empresas:
            # print(empresa["renglones_desestimados"])
            # obtiene cada tipo de desestimacion(ad, tec, eco)
            for tipo_desestimacion in empresa["renglones_desestimados"]:
                renglones = empresa["renglones_desestimados"][tipo_desestimacion]
                # print("\t",tipo_desestimacion,renglones)
                for renglon in renglones:
                    # print("\t",renglon)
                    lista_desestimados[renglon] = True
        
        # print(lista_desestimados, len(lista_desestimados))
        return list(lista_desestimados.keys())

    def renglones_fracasados(self):
        """devuelve una lista con los renglones fracasados
        compara una lista """

        # renglones desestimados
        lista_desestimados_totales = self.excel.renglones_ofertados_sin_opciones(self.renglones_totales_desestimados())
        lista_desestimados_totales.sort()

        # renglones adjudicados
        lista_adjudicados_totales = self.excel.renglones_ofertados_sin_opciones(self.renglones_total_adjudicados())
        lista_adjudicados_totales.sort()
        
        lista = []

        for desestimados in lista_desestimados_totales:
            print(desestimados)
            try:
                lista_adjudicados_totales.index(desestimados)
            except:
                lista.append(desestimados)


        print(lista,lista_desestimados_totales, lista_adjudicados_totales)
        return lista

    def verificar_proceso_existente(self):
        """verifica si en el archivo json ya existe el numero
        de contratacion que se quiere 
        crear o modificar
            si es False no existe
            si es True ya existe"""
        existe = False
        # print(self.values)
        
        count = 0
        for value in self.values:
            n_proceso = list(value.keys())[0]            
            # print(n_proceso)
            if self.contratacion == n_proceso:
                count +=1

        if count == 0:
            existe = False
            print(f"La contratación {self.contratacion} fue creada con éxito.")
            return existe
        
        elif count > 0:
            existe = True
            print(f"La contratacion {self.contratacion} ya existe.")
            return existe

    def empresas_con_adjudicacion(self):
        """devuelve una lista de empresas a los que no se
        les adjudico ningun renglon de la contratacion.
        sirve para desestimar administrativamente mas facil."""
        lista_empresas_con_adjudicar = {}
        for x in self.values:
            if self.contratacion == list(x.keys())[0]:
                listado_empresas = x[self.contratacion]["lista_empresas"]
                
                for empresas in listado_empresas:
                    nombre_empresa = str(empresas["empresa"])
                    cuit = str(empresas["cuit"])
                    renglones_adjudicados = empresas["renglones_adjudicados"]
                    if len(renglones_adjudicados) > 0:
                        lista_empresas_con_adjudicar[nombre_empresa]=cuit
                        
        # print(lista_empresas_con_adjudicar)
        return lista_empresas_con_adjudicar

    def empresas_sin_adjudicacion(self):
        """devuelve una lista de empresas a los que no se
        les adjudico ningun renglon de la contratacion.
        sirve para desestimar administrativamente mas facil."""
        lista_empresas_sin_adjudicar = []
        for x in self.values:
            if self.contratacion == list(x.keys())[0]:
                listado_empresas = x[self.contratacion]["lista_empresas"]
                cantidad_empresas = x[self.contratacion]["firmas_confirmadas"]
                
                for empresas in listado_empresas:
                    nombre_empresa = str(empresas["empresa"])
                    renglones_adjudicados = empresas["renglones_adjudicados"]
                    if renglones_adjudicados == []:
                        print(nombre_empresa)
                        lista_empresas_sin_adjudicar.append(nombre_empresa)
                        
        print("empresas con 0 renglones: ",lista_empresas_sin_adjudicar)
        return lista_empresas_sin_adjudicar

    def agregar_proceso(self):
        """agrega el proceso de compra al json. 
        primero verifica si ya existe, si no, lo agrega"""
        verificacion = self.verificar_proceso_existente()

        if verificacion == True:
            msj = f"La contratación {self.contratacion} ya existe"
            # print(msj)
        else:        
            msj = f"Guardando la contratación {self.contratacion}"
            # print(msj)        

            valores = self.excel.crear_proceso()
            data = self.open_json(self.file)
            data.append(valores)
            self.save_json_values(self.file, data )
        
        return self.contratacion

    def eliminar_contratacion(self):
        """elimina el diccionario de una contratacion"""
        values = self.values

        indice = 0
        for diccionario in values:
            print(list(diccionario.keys())[0])
            if list(diccionario.keys())[0] == self.contratacion:
                values.pop(indice)                
            indice +=1

        self.save_json_values(self.file,values)

    def actualizar_dato_contratacion(self, propiedad, valor):
        """permite actualizar dato en el archivo json
        solo de una propiedad de la contratacion"""

        count = 0
        for empresas in self.values:
            contratacion_json = list(empresas.keys())[0]
            print(contratacion_json)
            if contratacion_json == self.contratacion:
                self.values[count][self.contratacion][propiedad]= valor
                self.save_json_values(self.file, self.values)
            else:                
                print("no encontrado")

            count += 1

    def datos_empresa(self,empresa):
        """devuelve los datos de una sola empresa ESPECIFICADA"""
        datos = self.lista_empresas_con_datos_completos()
        value = None
        for em in datos:
            # print(em)
            if em["empresa"] == empresa:
                value = em
                
        return value

    def lista_empresas_con_datos_completos(self):
        """toma la key entera de 'lista_empresas' de la contratacion
        con todos sus datos"""
        for contratacion in self.values:
            # busca la contratacion en la lista del json
            nombre_contratacion = list(contratacion.keys())[0]

            if nombre_contratacion == self.contratacion:
                #cuando encuentra el nombre de la contratacion
                # que obtenga la key 'lista_empresas'
                valores_contratacion = contratacion[self.contratacion]
                valores_empresas =valores_contratacion["lista_empresas"]

                return valores_empresas    

    def datos_basicos_contratacion(self):
        """obtiene todos los datos basicos de la contratacion
        desde el json"""
        values = self.values
        datos = {}

        for contratacion_numero in values:
            # print(contratacion)
            if list(contratacion_numero.keys())[0] == self.contratacion:
                data = list(contratacion_numero.values())[0]
                datos = data

        return datos

    def renglones_totales_desestimados_x_empresa(self, empresa):
        """devuelve una lista total de los renglones desestimados en cualquiera de
        sus formas (ya sea admin, tec o eco) x empresa.
        sirve principalmente para la desestimacion en el 'dispone'"""
        values = self.lista_empresas_con_datos_completos()
        lista_final = []
        for emp in values:
            if emp["empresa"] == empresa:
                for deses in emp["renglones_desestimados"]:
                    lista_deses  = emp["renglones_desestimados"][deses]
                    lista_final.extend(lista_deses)

        lista_final.sort()
        # print(lista_final)
        return lista_final

    def cant_empresas_totales_con_desestimaciones(self):
        lista_empresas = self.lista_empresas_con_datos_completos()

        lista=  []
        for empresa in lista_empresas:
            nombre_empresa = empresa["empresa"]
            renglones_deses = self.renglones_totales_desestimados_x_empresa(nombre_empresa)
            if len(renglones_deses) >0:
                lista.append(renglones_deses)

        return len(lista)



#______________________________________________________________________________________________



def open_json(file):
    """abre los archivos json para su lectura"""
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        main_objeto = json.load(json_file) #LA VARIABLE 'datos' ABRE EL OBJETO JSON DEL ARCHIVO 'json_file'
        return main_objeto

def save_json_values(file, values):
    # data = open_json(file)
    with open(file, "w", encoding='utf8') as outfile:
        json.dump(values, outfile, sort_keys = False, indent = 2, ensure_ascii=False)

def modificar_datos_empresa(contratacion, empresa, data):
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["empresa"] = data["empresa"]
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["cuit"] = data["cuit"]
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["doc_complementaria"] = data["doc_complementaria"]
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["precio_total_letras"] = data["precio_total_letras"]

                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                
                count_empresa +=1
        count_contrataciones+=1

def cantidad_documentacion_complementaria(contratacion):
    """ devuelve las empresas a las que se les solicito
    documentacion complementaria.
    devuelve una lista de dictionarios, cuyas keys son 
    el nombre de la empresa y su valor el n° de cuit
    ej: [{'empresa':'12-12345678-1'}, ...]"""
    values = open_json(file)
    final = [] 

    for x in values:
        if list(x.keys())[0] == contratacion:
            lista_empresas = x[contratacion]["lista_empresas"]
            count_em = 0
            for y in lista_empresas:
                count_em+=1
                if y["doc_complementaria"] == True:
                    final.append({y["empresa"]:y["cuit"]})
            # print(lista_empresas)

    # print(final)
    return final

def cantidad_desestimaciones_admin(contratacion):
    """ devuelve las empresas que se desestimaron administrativamente.
    devuelve una lista de dictionarios, cuyas keys son 
    el nombre de la empresa y su valor el n° de cuit
    ej: [{'empresa':'12-12345678-1'}, ...]"""
    values = open_json(file)
    final = [] 

    for x in values:
        if list(x.keys())[0] == contratacion:
            lista_empresas = x[contratacion]["lista_empresas"]
            count_em = 0
            for y in lista_empresas:
                count_em+=1
                if len(y["renglones_desestimados"]["administrativo"]) > 0:
                    final.append({y["empresa"]:y["cuit"]})
            # print(lista_empresas)

    # print(final)
    return final

def documentacion_complementaria(contratacion, empresa, complementaria):
    """junta todos los renglones desestimados tecnicas y economicamente
    y los pasa a administrativos
    contratacion-> (str) n° contratacion
    empresa -> (str) nombre empresa
    complementaria -> (str) True/false"""

    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            for item_empresa in list_empresas:                
                nombre_empresa = item_empresa["empresa"]
                if nombre_empresa == empresa:
                    doc_complementaria = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["doc_complementaria"]

                    #para luego pasar a administrativo
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["doc_complementaria"] = complementaria

                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                
                count_empresa +=1
        count_contrataciones+=1

# desestimar
def desestimar_administrativamente(contratacion, empresa):
    """junta todos los renglones desestimados tecnicas y economicamente
    y los pasa a administrativos"""
    # values = open_json(file)

    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    # pass

                    lista_desestimados = []          
                    administrativo = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"]
                    economicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                    tecnicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                    
                    # se juntan todas las desestimaciones en economicos
                    lista_desestimados.extend(administrativo)
                    lista_desestimados.extend(economicos) 
                    lista_desestimados.extend(tecnicos) 

                    #para luego pasar a administrativo
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"] = lista_desestimados
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = []
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = []
                    # print(values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"])

                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                    # print(administrativo)
                
                count_empresa +=1
        count_contrataciones+=1

def desestimar_economicamente(contratacion, empresa):
    """junta todos los renglones desestimados tecnicas y administrativa
    y los pasa a economicos"""
    # values = open_json(file)

    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    # pass

                    lista_desestimados = []          
                    administrativo = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"]
                    economicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                    tecnicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                    
                    # se juntan todas las desestimaciones en economicos
                    lista_desestimados.extend(administrativo)
                    lista_desestimados.extend(economicos) 
                    lista_desestimados.extend(tecnicos) 

                    #para luego pasar a administrativo
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = lista_desestimados
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["administrativo"] = []
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = []
                    # print(values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"])

                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                    # print(administrativo)
                
                count_empresa +=1
        count_contrataciones+=1

# eliminar renglones de economicos y tecnicos
def eliminar_renglones_economicos(contratacion, empresa, lista_renglones):
    """elimina items especificados en la 'lista de renglones'
    de la lista de economicos"""
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            # para buscar la empresa seleccionada
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    economicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                    
                    #iterara la lista de renglones seleccionados
                    for item in lista_renglones:
                        print("eliminando renglon de economico",type(item),item)
                        try:
                            if len(item.split(".")) == 1:
                                economicos.remove(int(item))
                            else:                                
                                economicos.remove(float(item))
                        except Exception as e:
                            print(e,"no existen estos items en la lista de economicos")

                    print(empresa,economicos)
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = economicos
                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                
                count_empresa +=1
        count_contrataciones+=1

def eliminar_renglones_tecnicos(contratacion, empresa, lista_renglones):
    """elimina items especificados en la 'lista de renglones'
    de la lista de tecnicos"""
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            # para buscar la empresa seleccionada
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    tecnicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                    
                    #iterara la lista de renglones seleccionados
                    for item in lista_renglones:
                        print(item)
                        try:
                            if len(item.split(".")) == 1:
                                tecnicos.remove(int(item))
                            else:                                
                                tecnicos.remove(float(item)) 
                        except Exception as e:
                            print(e,"no existen estos items en la lista de 'tecnicos'")

                    print(empresa,tecnicos)
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = tecnicos
                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                
                count_empresa +=1
        count_contrataciones+=1

def agregar_renglones_economicos(contratacion, empresa, lista_renglones):
    """agrega a la lista de desestimaciones economicas renglones
    especificados en la lista_renglones"""
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            # para buscar la empresa seleccionada
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    economicos = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"]
                    
                    #iterara la lista de renglones seleccionados
                    for item in lista_renglones:
                        print(item)
                        try:
                            if len(item.split(".")) == 1:
                                economicos.append(int(item))
                            else:                                
                                economicos.append(float(item)) 
                        except Exception as e:
                            print(e,"no existen estos items en la lista de economicos")

                    print(empresa,economicos)
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["economicamente"] = economicos
                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                
                count_empresa +=1
        count_contrataciones+=1

def agregar_renglones_tecnicas(contratacion, empresa, lista_renglones):
    """agrega a la lista de desestimaciones economicas renglones
    especificados en la lista_renglones"""
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        values = json.load(json_file)
    # print(values)

    # se iteran todas la contrataciones cargadas
    count_contrataciones = 0
    for contrataciones in values:
        # print(contrataciones)
        # se busca con el condicional seleccionar solo la contratacion buscada
        if  list(contrataciones.keys())[0] == contratacion:
            list_empresas = contrataciones[contratacion]["lista_empresas"]
            # print(list_empresas)
            count_empresa = 0 # para calcular el indice donde se ubica la empresa

            # se iteran todos los items de la propiedad 'lista_empresas'
            # para buscar la empresa seleccionada
            for item_empresa in list_empresas:                
                # print(item_empresa)
                nombre_empresa = item_empresa["empresa"]
                # print(des_economicos,nombre_empresa)
                if nombre_empresa == empresa:
                    tecnicas = values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"]
                    
                    #iterara la lista de renglones seleccionados
                    for item in lista_renglones:
                        print("agregando a tecnicos",type(item),item)
                        try:
                            # agregar renglones a la lista de 'tecnicos'
                            if len(item.split(".")) == 1:
                                tecnicas.append(int(item))
                            else:                                
                                tecnicas.append(float(item)) 
                        except Exception as e:
                            print(e,"no existen estos items en la lista de economicos")

                    print(empresa,tecnicas)
                    values[count_contrataciones][contratacion]["lista_empresas"][count_empresa]["renglones_desestimados"]["tecnicamente"] = tecnicas
                    # saving
                    with open(file, "w", encoding='utf8') as outfile:
                        json.dump(values, outfile, sort_keys = False,
                                indent = 2, ensure_ascii=False)
                
                count_empresa +=1
        count_contrataciones+=1

def monto_total_adjudicado(contratacion):
    """suma todos los precios totales de las empresas"""
    values = lista_empresas_con_datos_completos(contratacion)
    
    precio_total = 0.0
    for precio in values:
        precio_total+=precio["precio_total"]
        
    return precio_total

def renglones_total_adjudicados(contratacion):
    """devuelve una lista con todos los renglones adjudicados"""

    datos_contratacion = datos_basicos_contratacion(contratacion)
    
    values = open_json(file)

    renglones_ad = []

    for contrataciones_ in values:
        if list(contrataciones_.keys())[0] == contratacion:
            for empresa  in contrataciones_[contratacion]["lista_empresas"]:
                renglones_ad += empresa["renglones_adjudicados"]

    renglones_ad.sort()
    return renglones_ad

def renglones_totales_desestimados(contratacion):
    """devuelve una lista con todos los renglones desestimados(en cualquier forma)
    de todas las empresas de la contratacion"""
    lista_empresas = lista_empresas_con_datos_completos(contratacion)
    lista_desestimados = {}

    # obtiene los renglones desestimados de la empresa
    for empresa in lista_empresas:
        # print(empresa["renglones_desestimados"])
        # obtiene cada tipo de desestimacion(ad, tec, eco)
        for tipo_desestimacion in empresa["renglones_desestimados"]:
            renglones = empresa["renglones_desestimados"][tipo_desestimacion]
            # print("\t",tipo_desestimacion,renglones)
            for renglon in renglones:
                # print("\t",renglon)
                lista_desestimados[renglon] = True
    
    # print(lista_desestimados, len(lista_desestimados))
    return list(lista_desestimados.keys())

def renglones_fracasados(contratacion):
    """devuelve una lista con los renglones fracasados
    compara una lista """

    # renglones desestimados
    lista_desestimados_totales = xl.renglones_ofertados_sin_opciones(renglones_totales_desestimados(contratacion))
    lista_desestimados_totales.sort()

    # renglones adjudicados
    lista_adjudicados_totales = xl.renglones_ofertados_sin_opciones(renglones_total_adjudicados(contratacion))
    lista_adjudicados_totales.sort()
    
    lista = []

    for desestimados in lista_desestimados_totales:
        print(desestimados)
        try:
            lista_adjudicados_totales.index(desestimados)
        except:
            lista.append(desestimados)


    print(lista,lista_desestimados_totales, lista_adjudicados_totales)
    return lista

def verificar_proceso_existente(n_proceso):
    """verifica si en el archivo json ya existe el numero
    de contratacion que se quiere 
    crear o modificar
        si es False no existe
        si es True ya existe"""
    values = open_json(file)
    existe = False
    print(values)
    
    count = 0
    for value in values:
        proceso = list(value.keys())[0]
        
        print(proceso)
        if n_proceso == proceso:
            count +=1

    if count == 0:
        existe = False
        return existe
    elif count > 0:
        existe = True
        return existe

def empresas_con_adjudicacion(contratacion):
    """devuelve una lista de empresas a los que no se
    les adjudico ningun renglon de la contratacion.
    sirve para desestimar administrativamente mas facil."""
    values = open_json(file)
    lista_empresas_con_adjudicar = {}
    for x in values:
        if contratacion == list(x.keys())[0]:
            listado_empresas = x[contratacion]["lista_empresas"]
            
            for empresas in listado_empresas:
                nombre_empresa = str(empresas["empresa"])
                cuit = str(empresas["cuit"])
                renglones_adjudicados = empresas["renglones_adjudicados"]
                if len(renglones_adjudicados) > 0:
                    lista_empresas_con_adjudicar[nombre_empresa]=cuit
                    
    # print(lista_empresas_con_adjudicar)
    return lista_empresas_con_adjudicar

def empresas_sin_adjudicacion(contratacion):
    """devuelve una lista de empresas a los que no se
    les adjudico ningun renglon de la contratacion.
    sirve para desestimar administrativamente mas facil."""
    values = open_json(file)
    lista_empresas_sin_adjudicar = []
    for x in values:
        if contratacion == list(x.keys())[0]:
            listado_empresas = x[contratacion]["lista_empresas"]
            cantidad_empresas = x[contratacion]["firmas_confirmadas"]
            
            for empresas in listado_empresas:
                nombre_empresa = str(empresas["empresa"])
                renglones_adjudicados = empresas["renglones_adjudicados"]
                if renglones_adjudicados == []:
                    print(nombre_empresa)
                    lista_empresas_sin_adjudicar.append(nombre_empresa)
                    
    print("empresas con 0 renglones: ",lista_empresas_sin_adjudicar)
    return lista_empresas_sin_adjudicar

def agregar_proceso(xl_recomendacion, xl_renglones):
    """agrega el proceso de compra al json. 
    primero verifica si ya existe, si no, lo agrega"""
    numero_contratacion = xl.datos_contratacion(xl_recomendacion, xl_renglones)["n_proceso"]
    verificacion = verificar_proceso_existente(numero_contratacion)

    if verificacion == True:
        msj = f"La contratación {numero_contratacion} ya existe"
        # print(msj)
    else:        
        msj = f"Guardando la contratación {numero_contratacion}"
        # print(msj)        

        valores = xl.crear_proceso(xl_recomendacion, xl_renglones)
        data = open_json(file)
        data.append(valores)
        with open(file, "w", encoding='utf8') as outfile:
            json.dump(data, outfile, sort_keys = False, indent = 2, ensure_ascii=False)
    
    return numero_contratacion

def eliminar_contratacion(contratacion):
    """elimina el diccionario de una contratacion"""
    main_list = open_json(file)

    indice = 0
    for diccionario in main_list:
        print(list(diccionario.keys())[0])
        if list(diccionario.keys())[0] == contratacion:
            main_list.pop(indice)


        indice +=1
    save_json_values(file,main_list)

def actualizar_dato_contratacion(contratacion, propiedad, valor):
    """permite actualizar dato en el archivo json
    solo de una propiedad de la contratacion"""
    with open(file, encoding='utf8') as json_file: #ABRIR EL ARCHIVO	
        data = json.load(json_file)
    
    count = 0
    for empresas in data:
        contratacion_json = list(empresas.keys())[0]
        print(contratacion_json)
        if contratacion_json == contratacion:
            data[count][contratacion][propiedad]= valor

            with open(file, "w", encoding='utf8') as outfile:
                json.dump(data, outfile, sort_keys = False,
                        indent = 2, ensure_ascii=False)
        else:
            
            print("no encontrado")

        count += 1

def datos_empresa(num_contratacion,empresa):
    """devuelve los datos de una sola empresa ESPECIFICADA"""
    datos = lista_empresas_con_datos_completos(num_contratacion)
    value = None
    for em in datos:
        # print(em)
        if em["empresa"] == empresa:
            value = em
            
    return value

def lista_empresas_con_datos_completos( num_contratacion):
    """toma la key entera de 'lista_empresas' de la contratacion
    con todos sus datos"""
    values =open_json(file) 
    for contratacion in values:
        # busca la contratacion en la lista del json
        nombre_contratacion = list(contratacion.keys())[0]

        if nombre_contratacion == num_contratacion:
            #cuando encuentra el nombre de la contratacion
            # que obtenga la key 'lista_empresas'
            valores_contratacion = contratacion[num_contratacion]
            valores_empresas =valores_contratacion["lista_empresas"]

            return valores_empresas

def datos_basicos_contratacion(contratacion):
    """obtiene todos los datos basicos de la contratacion
    desde el json"""
    values = open_json(file)
    datos = {}

    for contratacion_numero in values:
        # print(contratacion)
        if list(contratacion_numero.keys())[0] == contratacion:
            data = list(contratacion_numero.values())[0]
            datos = data

    return datos

def renglones_totales_desestimados_x_empresa(contratacion, empresa):
    """devuelve una lista total de los renglones desestimados en cualquiera de
    sus formas (ya sea admin, tec o eco) x empresa.
    sirve principalmente para la desestimacion en el 'dispone'"""
    values = lista_empresas_con_datos_completos(contratacion)
    lista_final = []
    for emp in values:
        if emp["empresa"] == empresa:
            for deses in emp["renglones_desestimados"]:
                lista_deses  = emp["renglones_desestimados"][deses]
                lista_final.extend(lista_deses)

    lista_final.sort()
    # print(lista_final)
    return lista_final

def cant_empresas_totales_con_desestimaciones(contratacion):
    lista_empresas = lista_empresas_con_datos_completos(contratacion)

    lista=  []
    for empresa in lista_empresas:
        nombre_empresa = empresa["empresa"]
        renglones_deses = renglones_totales_desestimados_x_empresa(contratacion, nombre_empresa)
        if len(renglones_deses) >0:
            lista.append(renglones_deses)

    return len(lista)

if __name__== "__main__":
    contratacion = "455-3276-CME21"
    empresa = "BIODIAGNOSTICO S.A."  
    # renglones_fracasados(contratacion)
    xl1= "PROCESOS/2243/2243.xlsx"
    xl2= "PROCESOS/2243/renglones.xlsx"

    json_ = JsonAdmin(xl1,xl2)
    print(json_.datos_basicos_contratacion())