from util.conexao import obter_conexao
from hashlib import md5

def inserir_funcionario_completo(dados):
    conn = obter_conexao()
    try:
        with conn.cursor() as cursor:
            senha_hash = md5(dados["senha"].encode()).hexdigest()

            # 1. Inserir usuário
            cursor.execute("""
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
                VALUES (%s, %s, %s, %s, 'FUNCIONARIO', %s)
            """, (dados["nome"], dados["cpf"], dados["data_nascimento"], dados["telefone"], senha_hash))

            id_usuario = cursor.lastrowid

            # 2. Inserir endereço (opcional, com campos simulados ou reais)
            if "cep" in dados:  # Só insere se dados de endereço forem fornecidos
                cursor.execute("""
                    INSERT INTO endereco (id_usuario, cep, local, numero_casa, bairro, cidade, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (id_usuario, dados["cep"], dados["local"], dados["numero_casa"],
                      dados["bairro"], dados["cidade"], dados["estado"]))

            # 3. Gerar código de funcionário
            codigo_funcionario = f"FUNC-{id_usuario:05d}"

            # 4. Inserir funcionário
            cursor.execute("""
                INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, id_supervisor)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, codigo_funcionario, dados["cargo"], dados["id_supervisor"]))

            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
