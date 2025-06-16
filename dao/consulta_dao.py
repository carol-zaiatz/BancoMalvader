from util.conexao import obter_conexao as conectar

def obter_dados_usuario(id_usuario):
    conn = conectar()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nome, cpf, telefone, tipo_usuario FROM usuario WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obter_contas_usuario(id_usuario, tipo_usuario=None):
    conn = conectar()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)

    if tipo_usuario == 'FUNCIONARIO':
        query = """
            SELECT c.id_conta, c.numero_conta, c.tipo_conta, c.saldo, c.status
            FROM conta c
            WHERE c.status = 'ATIVA'
        """
        cursor.execute(query)
    else:
        query = """
            SELECT c.id_conta, c.numero_conta, c.tipo_conta, c.saldo, c.status
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            WHERE cl.id_usuario = %s AND c.status = 'ATIVA'
        """
        cursor.execute(query, (id_usuario,))
        
    contas = cursor.fetchall()
    cursor.close()
    conn.close()
    return contas

def obter_score_credito(id_usuario):
    conn = conectar()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT score_credito FROM cliente WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else None

def obter_projecao_rendimentos(id_conta):
    conn = conectar()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ROUND(c.saldo * COALESCE(cp.taxa_rendimento, ci.taxa_rendimento_base, 0), 2)
        FROM conta c
        LEFT JOIN conta_poupanca cp ON c.id_conta = cp.id_conta
        LEFT JOIN conta_investimento ci ON c.id_conta = ci.id_conta
        WHERE c.id_conta = %s
    """, (id_conta,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else 0.0
