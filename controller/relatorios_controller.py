# controller/relatorios_controller.py
from dao.usuario_dao import gerar_relatorios, buscar_scores_clientes

class RelatoriosController:
    def __init__(self, usuario):
        self.usuario = usuario

    def obter_dados_relatórios(self):
        contas, movimentacoes = gerar_relatorios()
        scores = buscar_scores_clientes()
        return contas, movimentacoes, scores

    def obter_relatorios_filtrados(self, tipo, data_inicio, data_fim):
        # Por enquanto, retorna dados de teste
        # Idealmente você filtraria aqui com base no tipo e datas
        relatorios = [
            {
                'id': 1,
                'tipo': 'FINANCEIRO',
                'data_geracao': data_inicio,
                'conteudo': 'Relatório financeiro de exemplo'
            },
            {
                'id': 2,
                'tipo': 'OPERACIONAL',
                'data_geracao': data_fim,
                'conteudo': 'Relatório operacional de exemplo'
            }
        ]

        # Filtro de tipo (se especificado)
        if tipo:
            relatorios = [r for r in relatorios if r['tipo'] == tipo]

        return relatorios