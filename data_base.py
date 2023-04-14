import sqlite3
from sqlite3 import OperationalError

import tkinter as tk
from tkinter import ttk


db = "bd/compras.db"


def run_query(query):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query)
        conn.commit()
    return result

def sqlquery_in_a_list(query):
    """devuelve una lista de listas con los datos"""
    result = []    
    db_row = run_query(db, query)
    for row in db_row:
        result.append(row)
        # print(row)
    return result

def get_empresa(columns):
    columns = {}
    

def add_empresa(cuit, nombre):
    query = f"""
        INSERT INTO empresa ('cuit', 'nombre')
        VALUES ('{cuit}', '{nombre}');

    """
    run_query(query)
    # return query 


if __name__ == "__main__":
    pass