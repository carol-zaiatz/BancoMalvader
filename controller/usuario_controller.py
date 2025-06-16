from dao.usuario_dao import atualizar_telefone_senha
from dao.funcionario_dao import inserir_funcionario_completo

class UsuarioController:
    def atualizar_usuario(self, id_usuario, telefone=None, senha=None):
        if not telefone and not senha:
            return False, "Nada para atualizar."
        return atualizar_telefone_senha(id_usuario, telefone, senha)

    def cadastrar_funcionario(self, nome, cpf, data_nascimento, telefone, cargo, senha):
        try:
            dados = {
                "nome": nome,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
                "telefone": telefone,
                "cargo": cargo,
                "senha": senha,
                "cep": "00000-000",
                "local": "Rua Padrão",
                "numero_casa": 123,
                "bairro": "Bairro Padrão",
                "cidade": "Cidade",
                "estado": "DF",
                "id_supervisor": None
            }
            sucesso = inserir_funcionario_completo(dados)
            if sucesso:
                return True, "Funcionário cadastrado com sucesso."
            else:
                return False, "Erro ao cadastrar funcionário."
        except Exception as e:
            return False, f"Erro no cadastro: {e}"
