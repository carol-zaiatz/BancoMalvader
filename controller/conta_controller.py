from util.conexao import obter_conexao as conectar
from dao.conta_dao import inserir_cliente_e_conta
from hashlib import md5

def salvar_nova_conta(dados):
    try:
        dados["senha_hash"] = md5(dados["senha"].encode()).hexdigest()
        sucesso = inserir_cliente_e_conta(dados)
        if sucesso:
            return "Conta criada com sucesso!", True
        else:
            return "Não foi possível criar a conta. Verifique os dados.", False
    except Exception as e:
        print(f"[ERRO] no controller: {e}")
        return f"Erro ao criar conta: {str(e)}", False

def obter_conta_por_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*
        FROM conta c
        JOIN cliente cl ON c.id_cliente = cl.id_cliente
        JOIN usuario u ON cl.id_usuario = u.id_usuario
        WHERE u.id_usuario = %s AND c.status = 'ATIVA'
        LIMIT 1
    """, (id_usuario,))
    conta = cursor.fetchone()
    cursor.close()
    conn.close()
    return conta

def obter_saldo_e_rendimento(id_conta):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT saldo FROM conta WHERE id_conta = %s", (id_conta,))
    saldo = cursor.fetchone()["saldo"]
    cursor.execute("SELECT taxa_rendimento FROM conta_poupanca WHERE id_conta = %s", (id_conta,))
    poupanca = cursor.fetchone()
    rendimento = (float(saldo) * float(poupanca["taxa_rendimento"]) / 100) if poupanca else 0.00
    cursor.close()
    conn.close()
    return saldo, rendimento

def realizar_transferencia(id_conta_origem, numero_conta_destino, valor, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_conta FROM conta WHERE numero_conta = %s AND status = 'ATIVA'", (numero_conta_destino,))
    destino = cursor.fetchone()
    if not destino:
        conn.close()
        return False, "Conta destino não encontrada ou inativa."
    id_conta_destino = destino[0]
    cursor.execute("""
        INSERT INTO transacao (id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao)
        VALUES (%s, %s, 'TRANSFERENCIA', %s, %s)
    """, (id_conta_origem, id_conta_destino, valor, descricao))
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Transferência realizada com sucesso."

def obter_transacoes(id_conta):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tipo_transacao, valor, data_hora, descricao
        FROM transacao
        WHERE id_conta_origem = %s OR id_conta_destino = %s
        ORDER BY data_hora DESC
        LIMIT 50
    """, (id_conta, id_conta))
    transacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return transacoes
