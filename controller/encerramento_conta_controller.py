from dao.usuario_dao import buscar_contas_ativas_por_usuario, encerrar_conta

class EncerramentoContaController:
    def __init__(self, usuario):
        self.usuario = usuario

    def get_contas_ativas(self):
        return buscar_contas_ativas_por_usuario(self.usuario.cpf)

    def encerrar_conta(self, id_conta):
        return encerrar_conta(id_conta)