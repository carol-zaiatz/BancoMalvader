from util.conexao import obter_conexao as conectar

def listar_contas_ativas(id_usuario, tipo_usuario):
    conn = conectar()
    if not conn:
        print("[ERRO] no DAO: Não foi possível conectar ao banco de dados")
        return []

    cursor = conn.cursor(dictionary=True)

    if tipo_usuario == 'FUNCIONARIO':
        query = """
            SELECT c.id_conta, c.numero_conta, c.tipo_conta, c.saldo
            FROM conta c
            WHERE c.status = 'ATIVA'
        """
        cursor.execute(query)
    else:
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
        conn = conectar()
        if not conn:
            print("[ERRO] no DAO: Não foi possível conectar ao banco de dados")
            return False, "Erro na conexão com o banco."

        cursor = conn.cursor()
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

        cursor.execute("UPDATE conta SET status = 'ENCERRADA' WHERE id_conta = %s", (id_conta,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Conta encerrada com sucesso."
    except Exception as e:
        return False, f"Erro ao encerrar conta: {str(e)}"
