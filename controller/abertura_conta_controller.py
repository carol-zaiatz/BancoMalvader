from dao.abertura_conta_dao import listar_clientes, inserir_conta

class AberturaContaController:
    def __init__(self, usuario):
        self.usuario = usuario

    def get_clientes(self):
        return listar_clientes()

    def criar_conta(self, id_cliente, tipo_conta, numero_conta):
        return inserir_conta(id_cliente, tipo_conta, numero_conta)
