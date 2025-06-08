from dao.conexao import conectar
from model.usuario import Usuario

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
