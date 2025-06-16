# controller/consulta_controller.py
from dao.consulta_dao import obter_dados_usuario, obter_contas_usuario

class ConsultaController:
    def __init__(self, usuario):
        self.usuario = usuario

    def get_dados_usuario(self):
        return obter_dados_usuario(self.usuario.id_usuario)

    def get_contas(self):
        return obter_contas_usuario(self.usuario.id_usuario)
