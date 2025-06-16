from util.conexao import obter_conexao

class TransacaoDAO:
    def transferir(self, id_cliente, conta_origem_num, conta_destino_num, valor):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
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

            cursor.execute("SELECT id_conta FROM conta WHERE numero_conta = %s", (conta_destino_num,))
            conta_destino = cursor.fetchone()
            if not conta_destino:
                return False, "Conta destino não encontrada"

            if conta_origem[1] < valor:
                return False, "Saldo insuficiente"

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

    def obter_transacoes_30_dias(self, id_cliente):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT t.data_hora, t.tipo_transacao, t.valor,
                       t.id_conta_origem, t.id_conta_destino
                FROM transacao t
                JOIN conta c ON t.id_conta_origem = c.id_conta
                WHERE c.id_cliente = %s
                  AND t.data_hora >= NOW() - INTERVAL 30 DAY
                ORDER BY t.data_hora DESC
            """
            cursor.execute(query, (id_cliente,))
            return cursor.fetchall()
        except Exception as e:
            print("Erro ao buscar transações:", e)
            return []
        finally:
            cursor.close()
            conn.close()
