import mysql.connector

def listar_clientes():
    conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                   host='localhost', database='banco_malvader')
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT c.id_cliente, u.nome
        FROM cliente c
        JOIN usuario u ON c.id_usuario = u.id_usuario
    """
    cursor.execute(query)
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return clientes

def inserir_conta(id_cliente, tipo_conta, numero_conta):
    try:
        conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                       host='localhost', database='banco_malvader')
        cursor = conn.cursor()

        # Verifica se número da conta já existe
        cursor.execute("SELECT id_conta FROM conta WHERE numero_conta = %s", (numero_conta,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Número de conta já existe."

        # Inserir nova conta
        cursor.execute("""
            INSERT INTO conta (numero_conta, tipo_conta, id_cliente, saldo, status)
            VALUES (%s, %s, %s, 0, 'ATIVA')
        """, (numero_conta, tipo_conta, id_cliente))

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Conta aberta com sucesso."
    except Exception as e:
        return False, f"Erro ao abrir conta: {str(e)}"
