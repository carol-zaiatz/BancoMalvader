# dao/conexao.py
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="91190707",  
            database="banco_malvader"
        )
    except Error as err:
        print(f"[ERRO] Falha ao conectar no banco de dados: {err}")
        return None
