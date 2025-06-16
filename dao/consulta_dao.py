# dao/consulta_dao.py
import mysql.connector

def obter_dados_usuario(id_usuario):
    conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                   host='localhost', database='banco_malvader')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nome, cpf, telefone, tipo_usuario FROM usuario WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obter_contas_usuario(id_usuario):
    conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                   host='localhost', database='banco_malvader')
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT c.numero_conta, c.tipo_conta, c.saldo, c.status
        FROM conta c
        JOIN cliente cl ON c.id_cliente = cl.id_cliente
        WHERE cl.id_usuario = %s AND c.status = 'ATIVA'
    """
    cursor.execute(query, (id_usuario,))
    contas = cursor.fetchall()
    cursor.close()
    conn.close()
    return contas
