from dao.conexao import conectar
from model.usuario import Usuario
import hashlib

# ====================
# CLIENTES E CONTAS
# ====================

def buscar_scores_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT cl.id_cliente, u.nome, cl.score_credito
        FROM cliente cl
        JOIN usuario u ON cl.id_usuario = u.id_usuario
    """)
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    return scores

def buscar_id_cliente_por_id_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente FROM cliente WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else None

def buscar_saldo_por_cpf(cpf):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.tipo_conta, c.saldo,
                   COALESCE(cp.taxa_rendimento, ci.taxa_rendimento_base, 0) AS rendimento
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            LEFT JOIN conta_poupanca cp ON c.id_conta = cp.id_conta
            LEFT JOIN conta_investimento ci ON c.id_conta = ci.id_conta
            WHERE u.cpf = %s AND c.status = 'ATIVA'
        """
        cursor.execute(query, (cpf,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print("Erro ao buscar saldo:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def buscar_contas_ativas_por_usuario(cpf):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.id_conta, c.numero_conta, c.tipo_conta, c.saldo
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            WHERE u.cpf = %s AND c.status = 'ATIVA'
        """
        cursor.execute(query, (cpf,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao buscar contas ativas:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def encerrar_conta(id_conta):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE conta SET status = 'ENCERRADA' WHERE id_conta = %s", (id_conta,))
        cursor.execute("CALL registrar_auditoria_conta(%s, 'Conta encerrada')", (id_conta,))
        conn.commit()
        return True, "Conta encerrada com sucesso."
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao encerrar conta: {e}"
    finally:
        cursor.close()
        conn.close()

def abrir_conta(cpf, tipo_conta, saldo_inicial):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("CALL abrir_conta(%s, %s, %s)", (cpf, tipo_conta, saldo_inicial))
        conn.commit()
    except Exception as e:
        print("Erro ao abrir conta:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# ====================
# FUNCIONÁRIOS
# ====================

def cadastrar_funcionario(cpf, nome, senha, cargo):
    senha_md5 = hashlib.md5(senha.encode()).hexdigest()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("CALL cadastrar_funcionario(%s, %s, %s, %s)", (cpf, nome, senha_md5, cargo))
    conn.commit()
    cursor.close()
    conn.close()

# ====================
# RELATÓRIOS
# ====================

def gerar_relatorios():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vw_resumo_contas")
    contas = cursor.fetchall()
    cursor.execute("SELECT * FROM vw_movimentacoes_recentes")
    movimentacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return contas, movimentacoes

# ====================
# LOGIN / USUÁRIO
# ====================

def buscar_usuario_por_cpf(cpf):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE cpf = %s", (cpf,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Usuario.from_dict(row) if row else None

def buscar_usuario_por_cpf_e_senha(cpf, senha_hash):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE cpf = %s AND senha_hash = %s", (cpf, senha_hash))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Usuario.from_dict(row) if row else None

def buscar_usuario_por_cpf_e_senha_e_otp(cpf, senha_hash, otp):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM usuario
        WHERE cpf = %s AND senha_hash = %s
          AND otp_ativo = %s AND otp_expiracao > NOW()
    """, (cpf, senha_hash, otp))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Usuario.from_dict(row) if row else None

def atualizar_telefone_senha(id_usuario, telefone=None, senha=None):
    try:
        conn = conectar()
        cursor = conn.cursor()
        if telefone:
            cursor.execute("UPDATE usuario SET telefone = %s WHERE id_usuario = %s", (telefone, id_usuario))
        if senha:
            senha_hash = hashlib.md5(senha.encode()).hexdigest()
            cursor.execute("UPDATE usuario SET senha_hash = %s WHERE id_usuario = %s", (senha_hash, id_usuario))
        conn.commit()
        return True, "Dados atualizados com sucesso."
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao atualizar dados: {e}"
    finally:
        cursor.close()
        conn.close()

def limpar_otp(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuario SET otp_ativo = NULL, otp_expiracao = NULL WHERE id_usuario = %s", (id_usuario,))
    conn.commit()
    cursor.close()
    conn.close()

def chamar_procedure_gerar_otp(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.callproc("gerar_otp", (id_usuario,))
    for result in cursor.stored_results():
        otp = result.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return otp

# ====================
# OUTROS
# ====================

def consultar_limite(cpf):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cc.limite
            FROM conta_corrente cc
            JOIN conta c ON cc.id_conta = c.id_conta
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            WHERE u.cpf = %s
        """, (cpf,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0.0
    except Exception as e:
        print("Erro ao consultar limite:", e)
        return 0.0
    finally:
        cursor.close()
        conn.close()

def consultar_cliente(cpf):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT cl.*, u.nome, u.telefone
        FROM cliente cl
        JOIN usuario u ON cl.id_usuario = u.id_usuario
        WHERE u.cpf = %s
    """, (cpf,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def realizar_deposito(cpf, valor):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Buscar id_conta do cliente
        cursor.execute("""
            SELECT c.id_conta
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            WHERE u.cpf = %s AND c.status = 'ATIVA'
            LIMIT 1
        """, (cpf,))
        conta = cursor.fetchone()
        if not conta:
            return False, "Conta ativa não encontrada."

        id_conta = conta[0]

        cursor.execute("""
            INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
            VALUES (%s, 'DEPOSITO', %s, 'Depósito realizado pelo cliente')
        """, (id_conta, valor))

        conn.commit()
        return True, "Depósito realizado com sucesso."
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao realizar depósito: {e}"
    finally:
        cursor.close()
        conn.close()

def realizar_saque(cpf, valor):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id_conta, c.tipo_conta, c.saldo,
                   COALESCE(cc.limite, 0) AS limite
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            LEFT JOIN conta_corrente cc ON cc.id_conta = c.id_conta
            WHERE u.cpf = %s AND c.status = 'ATIVA'
            LIMIT 1
        """, (cpf,))
        conta = cursor.fetchone()
        if not conta:
            return False, "Conta ativa não encontrada."

        id_conta, tipo_conta, saldo, limite = conta
        saldo_disponivel = saldo + (limite if tipo_conta == 'CORRENTE' else 0)

        if valor > saldo_disponivel:
            return False, "Saldo insuficiente."

        cursor.execute("""
            INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
            VALUES (%s, 'SAQUE', %s, 'Saque realizado pelo cliente')
        """, (id_conta, valor))

        cursor.execute("CALL registrar_auditoria(%s, 'Saque realizado')", (cpf,))

        conn.commit()
        return True, "Saque realizado com sucesso."
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao realizar saque: {e}"
    finally:
        cursor.close()
        conn.close()


def transferir_valor(cpf_origem, cpf_destino, valor):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id_conta, c.saldo
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            WHERE u.cpf = %s AND c.status = 'ATIVA'
            LIMIT 1
        """, (cpf_origem,))
        origem = cursor.fetchone()
        if not origem:
            return "Conta de origem não encontrada."
        id_origem, saldo_origem = origem

        cursor.execute("""
            SELECT c.id_conta
            FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            WHERE u.cpf = %s AND c.status = 'ATIVA'
            LIMIT 1
        """, (cpf_destino,))
        destino = cursor.fetchone()
        if not destino:
            return "Conta de destino não encontrada."
        id_destino = destino[0]

        if saldo_origem < valor:
            return "Saldo insuficiente."

        cursor.execute("""
            INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
            VALUES (%s, 'TRANSFERENCIA', %s, 'Transferência enviada')
        """, (id_origem, valor))
        cursor.execute("""
            INSERT INTO transacao (id_conta_destino, tipo_transacao, valor, descricao)
            VALUES (%s, 'TRANSFERENCIA', %s, 'Transferência recebida')
        """, (id_destino, valor))

        cursor.execute("CALL registrar_auditoria(%s, %s)", (cpf_origem, "Transferência realizada"))

        conn.commit()
        return "Transferência realizada com sucesso."
    except Exception as e:
        conn.rollback()
        return f"Erro na transferência: {e}"
    finally:
        cursor.close()
        conn.close()
