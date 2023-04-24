import sqlite3
from sqlite3 import OperationalError

import tkinter as tk
from tkinter import ttk


data_base = "bd/compras.db"


def run_query(db,query):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query)
        conn.commit()
    return result

def get_data(query):
    """devuelve una lista de listas con los datos"""
    result = []    
    db_row = run_query(data_base,query)
    for row in db_row:
        result.append(row)
    return result


def get_empresa_from_cuit(cuit):
    if cuit =="":
        query = f"""
        SELECT * FROM empresa 
        """
    else:        
        query = f"""
        SELECT * FROM empresa 
        WHERE cuit = '{cuit}'
        """
    result = get_data(query)
    return result

def add_empresa(cuit, nombre):
    query = f"""
        INSERT INTO empresa ('cuit', 'nombre')
        VALUES ('{cuit}', '{nombre}')
    """
    run_query(data_base,query)

def add_proceso(lista):
    query = f"""
    INSERT INTO proceso (numero_proceso, nombre_proceso, expediente, monto_sugerido,
    monto_sugerido_en_letras, fecha_limite_dia, fecha_limite_mes, fecha_limite_anio,
    cantidad_firmas_revisadas, anio) 

    VALUES ('{lista["numero_proceso"]}', '{lista["nombre_proceso"]}', '{lista["expediente"]}',
    '{lista["monto_sugerido"]}', '{lista["monto_sugerido_en_letras"]}', '{lista["fecha_limite_dia"]}',
    '{lista["fecha_limite_mes"]}','{lista["fecha_limite_anio"]}','{lista["cantidad_firmas_revisadas"]}','{lista["anio"]}')   

    """
    run_query(data_base,query)



if __name__ == "__main__":
    # add_empresa("124124", "qoiwhfqiow")
    print(get_empresa_from_cuit("124124"))