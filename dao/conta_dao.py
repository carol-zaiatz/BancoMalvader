# dao/conta_dao.py
from util.conexao import obter_conexao  # Linha 1: Importa a função correta
import random

def inserir_cliente_e_conta(dados):
    """
    Insere um novo cliente e sua respectiva conta no banco de dados
    usando uma transação para garantir a integridade dos dados.
    """
    conn = obter_conexao()  # Linha 2: Usa a função correta para obter a conexão
    if not conn:
        raise Exception("Não foi possível conectar ao banco de dados")

    try:
        # Linha 3: Todo o resto do código que você já tinha, que está perfeito, vem aqui dentro
        with conn.cursor() as cursor:
            # Inicia a transação
            conn.start_transaction()

            # --- Passo 1: Inserir na tabela `usuario` ---
            sql_usuario = """
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
                VALUES (%s, %s, %s, %s, 'CLIENTE', %s)
            """
            cursor.execute(sql_usuario, (
                dados["nome"], dados["cpf"], dados["data_nascimento"], 
                dados["telefone"], dados["senha_hash"]
            ))
            id_usuario = cursor.lastrowid

            # --- Passo 2: Inserir na tabela `endereco` ---
            sql_endereco = """
                INSERT INTO endereco (id_usuario, cep, local, numero_casa, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_endereco, (
                id_usuario, dados["cep"], dados["local"], dados["numero_casa"],
                dados["bairro"], dados["cidade"], dados["estado"]
            ))

            # --- Passo 3: Inserir na tabela `cliente` ---
            sql_cliente = "INSERT INTO cliente (id_usuario, score_credito) VALUES (%s, %s)"
            cursor.execute(sql_cliente, (id_usuario, 50.0))
            id_cliente = cursor.lastrowid

            # --- Passo 4: Inserir na tabela `conta` ---
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

            # --- Passo 5: Inserir na tabela específica da conta ---
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

            # Se tudo deu certo, confirma a transação
            conn.commit()
            return True

    except Exception as e:
        conn.rollback()
        print(f"[ERRO] no DAO: {e}")
        raise e
    
    finally:
        conn.close()