# dao/funcionario_dao.py
from util.conexao import obter_conexao
from hashlib import md5

def inserir_funcionario_completo(dados):
    conn = obter_conexao()
    try:
        with conn.cursor() as cursor:
            senha_hash = md5(dados["senha"].encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
                VALUES (%s, %s, %s, %s, 'FUNCIONARIO', %s)
            """, (dados["nome"], dados["cpf"], dados["data_nascimento"], dados["telefone"], senha_hash))

            id_usuario = cursor.lastrowid

            cursor.execute("""
                INSERT INTO endereco (id_usuario, cep, local, numero_casa, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, dados["cep"], dados["local"], dados["numero_casa"],
                  dados["bairro"], dados["cidade"], dados["estado"]))

            cursor.execute("""
                INSERT INTO funcionario (id_usuario, cargo, id_supervisor)
                VALUES (%s, %s, %s)
            """, (id_usuario, dados["cargo"], dados["id_supervisor"]))

            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
