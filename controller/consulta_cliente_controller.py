# controller/consulta_cliente_controller.py
from dao.usuario_dao import consultar_cliente, buscar_contas_ativas_por_usuario


class ConsultaClienteController:
    def get_dados_cliente(self, cpf):
        dados = consultar_cliente(cpf)
        if dados:
            return {
                "nome": dados[1],           # supondo que 0 = id, 1 = nome, 2 = telefone, 3 = id_usuario, etc
                "telefone": dados[2],
                "tipo_usuario": "Cliente"
            }
        return None

    def get_contas_ativas(self, cpf):
        return buscar_contas_ativas_por_usuario(cpf)