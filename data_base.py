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



if __name__ == "__main__":
    # add_empresa("124124", "qoiwhfqiow")
    print(get_empresa_from_cuit("124124"))