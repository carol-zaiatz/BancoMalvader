from conexao import obter_conexao

class TransacaoDAO:
    def transferir(self, id_cliente, conta_origem_num, conta_destino_num, valor):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
            # Verificar se conta origem pertence ao cliente
            query = """
            SELECT c.id_conta, c.saldo FROM conta c
            JOIN cliente cl ON c.id_cliente = cl.id_cliente
            JOIN usuario u ON cl.id_usuario = u.id_usuario
            WHERE c.numero_conta = %s AND cl.id_cliente = %s
            """
            cursor.execute(query, (conta_origem_num, id_cliente))
            conta_origem = cursor.fetchone()
            if not conta_origem:
                return False, "Conta origem inválida ou não pertence ao cliente"

            # Verificar conta destino existe
            cursor.execute("SELECT id_conta FROM conta WHERE numero_conta = %s", (conta_destino_num,))
            conta_destino = cursor.fetchone()
            if not conta_destino:
                return False, "Conta destino não encontrada"

            if conta_origem[1] < valor:
                return False, "Saldo insuficiente"

            # Inserir transação de transferência (usa procedure no banco)
            cursor.execute("""
                INSERT INTO transacao (tipo_transacao, valor, id_conta_origem, id_conta_destino, data_hora)
                VALUES ('TRANSFERENCIA', %s, %s, %s, NOW())
            """, (valor, conta_origem[0], conta_destino[0]))

            conn.commit()
            return True, ""
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()