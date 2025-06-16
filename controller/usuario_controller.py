# controller/usuario_controller.py

from dao.usuario_dao import cadastrar_funcionario

class UsuarioController:
    def cadastrar_funcionario(self, nome, cpf, data_nascimento, telefone, cargo, senha):
        # Aqui você pode validar dados adicionais e depois chamar DAO
        
        # Exemplo: validar data de nascimento e telefone (pode melhorar)
        # Para simplificar, vamos direto ao cadastro, assumindo dados ok.

        try:
            cadastrar_funcionario(cpf, nome, senha, cargo)
            return True, "Funcionário cadastrado com sucesso."
        except Exception as e:
            return False, str(e)