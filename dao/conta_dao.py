from util.conexao import obter_conexao
import random

def inserir_cliente_e_conta(dados):
    conn = obter_conexao()
    if not conn:
        raise Exception("Não foi possível conectar ao banco de dados")

    try:
        with conn.cursor() as cursor:
            conn.start_transaction()

            sql_usuario = """
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
                VALUES (%s, %s, %s, %s, 'CLIENTE', %s)
            """
            cursor.execute(sql_usuario, (
                dados["nome"], dados["cpf"], dados["data_nascimento"],
                dados["telefone"], dados["senha_hash"]
            ))
            id_usuario = cursor.lastrowid

            sql_endereco = """
                INSERT INTO endereco (id_usuario, cep, local, numero_casa, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_endereco, (
                id_usuario, dados["cep"], dados["local"], dados["numero_casa"],
                dados["bairro"], dados["cidade"], dados["estado"]
            ))

            sql_cliente = "INSERT INTO cliente (id_usuario, score_credito) VALUES (%s, %s)"
            cursor.execute(sql_cliente, (id_usuario, 50.0))
            id_cliente = cursor.lastrowid

            numero_conta = f"{random.randint(10000, 99999)}-{random.randint(0,9)}"
            id_agencia_padrao = 1
            sql_conta = """
                INSERT INTO conta (numero_conta, id_agencia, tipo_conta, id_cliente)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_conta, (
                numero_conta, id_agencia_padrao, dados["tipo_conta"], id_cliente
            ))
            id_conta = cursor.lastrowid

            tipo_conta = dados["tipo_conta"]
            if tipo_conta == 'POUPANCA':
                sql_especifica = "INSERT INTO conta_poupanca (id_conta, taxa_rendimento) VALUES (%s, %s)"
                cursor.execute(sql_especifica, (id_conta, dados["taxa_rendimento"]))

            elif tipo_conta == 'CORRENTE':
                sql_especifica = """
                    INSERT INTO conta_corrente (id_conta, limite, data_vencimento, taxa_manutencao) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_especifica, (
                    id_conta, dados["limite"], dados["data_vencimento"], dados["taxa_manutencao"]
                ))

            elif tipo_conta == 'INVESTIMENTO':
                sql_especifica = """
                    INSERT INTO conta_investimento (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_especifica, (
                    id_conta, dados["perfil_risco"], dados["valor_minimo"], dados["taxa_rendimento_base"]
                ))

            conn.commit()
            return True

    except Exception as e:
        conn.rollback()
        print(f"[ERRO] no DAO: {e}")
        raise e

    finally:
        conn.close()
