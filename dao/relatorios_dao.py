import mysql.connector

def buscar_relatorios(tipo_relatorio, data_inicio, data_fim):
    conn = mysql.connector.connect(user='seu_user', password='sua_senha',
                                   host='localhost', database='banco_malvader')
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id_relatorio, tipo_relatorio, data_geracao, conteudo
        FROM relatorio
        WHERE data_geracao BETWEEN %s AND %s
    """
    params = [data_inicio, data_fim]

    if tipo_relatorio:
        query += " AND tipo_relatorio = %s"
        params.append(tipo_relatorio)

    query += " ORDER BY data_geracao DESC"

    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados
