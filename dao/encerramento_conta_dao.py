import mysql.connector

def listar_contas_ativas(id_usuario):
    conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                   host='localhost', database='banco_malvader')
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT c.id_conta, c.numero_conta, c.tipo_conta, c.saldo
        FROM conta c
        JOIN cliente cl ON c.id_cliente = cl.id_cliente
        WHERE cl.id_usuario = %s AND c.status = 'ATIVA'
    """
    cursor.execute(query, (id_usuario,))
    contas = cursor.fetchall()
    cursor.close()
    conn.close()
    return contas

def encerrar_conta_por_id(id_conta):
    try:
        conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                       host='localhost', database='banco_malvader')
        cursor = conn.cursor()

        # Verifica saldo da conta
        cursor.execute("SELECT saldo FROM conta WHERE id_conta = %s AND status = 'ATIVA'", (id_conta,))
        resultado = cursor.fetchone()
        if not resultado:
            cursor.close()
            conn.close()
            return False, "Conta não encontrada ou já encerrada."

        saldo = resultado[0]
        if saldo != 0:
            cursor.close()
            conn.close()
            return False, "Conta não pode ser encerrada com saldo diferente de zero."

        # Atualiza status da conta para ENCERRADA
        cursor.execute("UPDATE conta SET status = 'ENCERRADA' WHERE id_conta = %s", (id_conta,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Conta encerrada com sucesso."
    except Exception as e:
        return False, f"Erro ao encerrar conta: {str(e)}"
