# dao/usuario_dao.py
from dao.conexao import conectar
from model.usuario import Usuario
import mysql.connector
import hashlib

def buscar_scores_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nome, score FROM cliente")
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    return scores

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

def cadastrar_funcionario(cpf, nome, senha, cargo):
    senha_md5 = hashlib.md5(senha.encode()).hexdigest()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("CALL cadastrar_funcionario(%s, %s, %s, %s)", (cpf, nome, senha_md5, cargo))
    conexao.commit()
    cursor.close()
    conexao.close()

def alterar_dados_usuario(id_usuario, telefone=None, senha_hash=None):
    try:
        conn = conectar()
        cursor = conn.cursor()

        if telefone:
            cursor.execute("UPDATE usuario SET telefone = %s WHERE id_usuario = %s", (telefone, id_usuario))

        if senha_hash:
            cursor.execute("UPDATE usuario SET senha_hash = %s WHERE id_usuario = %s", (senha_hash, id_usuario))

        conn.commit()
        return True, "Dados atualizados com sucesso."
    
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao atualizar dados: {e}"
    
    finally:
        cursor.close()
        conn.close()

def consultar_cliente(cpf):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE cpf = %s", (cpf,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

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
        contas = cursor.fetchall()
        return contas
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
        
        # Atualiza o status da conta para encerrado
        cursor.execute("""
            UPDATE conta
            SET status = 'ENCERRADA'
            WHERE id_conta = %s
        """, (id_conta,))
        
        # Opcional: insere no log de auditoria
        cursor.execute("CALL registrar_auditoria_conta(%s, 'Conta encerrada')", (id_conta,))
        
        conn.commit()
        return True, "Conta encerrada com sucesso."
    
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao encerrar conta: {str(e)}"
    
    finally:
        cursor.close()
        conn.close()

def abrir_conta(cpf, tipo_conta, saldo_inicial):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("CALL abrir_conta(%s, %s, %s)", (cpf, tipo_conta, saldo_inicial))
        conexao.commit()
    except Exception as e:
        print("Erro ao abrir conta:", e)
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()

def consultar_limite(cpf):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
    SELECT cc.limite
    FROM conta_corrente cc
    JOIN conta c ON cc.id_conta = c.id_conta
    JOIN cliente cl ON c.id_cliente = cl.id_cliente
    JOIN usuario u ON cl.id_usuario = u.id_usuario
    WHERE u.cpf = %s
""", (cpf,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()
        return resultado[0] if resultado else 0.0
    except Exception as e:
        print("Erro ao consultar limite:", e)
        return 0.0
    
def buscar_saldo_por_cpf(cpf):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
            SELECT tipo_conta, saldo
            FROM vw_resumo_contas
            WHERE cpf = %s
        """
        cursor.execute(query, (cpf,))
        resultados = cursor.fetchall()
        return resultados

    except mysql.connector.Error as err:
        print("Erro ao buscar saldo:", err)
        return None

    finally:
        cursor.close()
        conn.close()
    

def transferir_valor(cpf_origem, cpf_destino, valor):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Buscar ID das contas
        cursor.execute("SELECT id, saldo FROM conta WHERE cliente_id = (SELECT id FROM cliente WHERE cpf = %s)", (cpf_origem,))
        origem = cursor.fetchone()
        if not origem:
            return "Conta de origem não encontrada."

        id_origem, saldo_origem = origem

        cursor.execute("SELECT id FROM conta WHERE cliente_id = (SELECT id FROM cliente WHERE cpf = %s)", (cpf_destino,))
        destino = cursor.fetchone()
        if not destino:
            return "Conta de destino não encontrada."

        id_destino = destino[0]

        if saldo_origem < valor:
            return "Saldo insuficiente."

        # Inserir transações
        cursor.execute("""
            INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
            VALUES (%s, 'TRANSFERENCIA', %s, 'Transferência enviada')
        """, (id_origem, valor))

        cursor.execute("""
            INSERT INTO transacao (id_conta_destino, tipo_transacao, valor, descricao)
            VALUES (%s, 'TRANSFERENCIA', %s, 'Transferência recebida')
        """, (id_destino, valor))

        # Chamar procedure de auditoria
        cursor.execute("CALL registrar_auditoria(%s, %s)", (cpf_origem, "Transferência realizada"))

        conexao.commit()
        return "Transferência realizada com sucesso."

    except Exception as e:
        conexao.rollback()
        return f"Erro na transferência: {e}"

    finally:
        cursor.close()
        conexao.close()
        

def buscar_usuario_por_cpf(cpf):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE cpf = %s", (cpf,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return Usuario(**row)
    return None

def buscar_usuario_por_cpf_e_senha(cpf, senha_hash):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM usuario WHERE cpf = %s AND senha_hash = %s"
    cursor.execute(sql, (cpf, senha_hash))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return Usuario(**row)
    return None

def buscar_usuario_por_cpf_e_senha_e_otp(cpf, senha_hash, otp):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT * FROM usuario
        WHERE cpf = %s AND senha_hash = %s
          AND otp_ativo = %s
          AND otp_expiracao > NOW()
    """
    cursor.execute(sql, (cpf, senha_hash, otp))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return Usuario(**row)
    return None

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

def limpar_otp(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuario SET otp_ativo = NULL, otp_expiracao = NULL WHERE id_usuario = %s", (id_usuario,))
    conn.commit()
    cursor.close()
    conn.close()
    
    
    