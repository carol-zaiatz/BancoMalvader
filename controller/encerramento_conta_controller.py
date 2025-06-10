from dao.encerramento_conta_dao import listar_contas_ativas, encerrar_conta_por_id

class EncerramentoContaController:
    def __init__(self, usuario):
        self.usuario = usuario

    def get_contas_ativas(self):
        return listar_contas_ativas(self.usuario.id_usuario)

    def encerrar_conta(self, id_conta):
        return encerrar_conta_por_id(id_conta)
