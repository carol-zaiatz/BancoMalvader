from dao.relatorios_dao import buscar_relatorios

class RelatoriosController:
    def __init__(self, usuario):
        self.usuario = usuario

    def obter_relatorios(self, tipo_relatorio, data_inicio, data_fim):
        tipo = tipo_relatorio if tipo_relatorio else None
        return buscar_relatorios(tipo, data_inicio, data_fim)
    