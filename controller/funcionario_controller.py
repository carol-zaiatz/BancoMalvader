from dao.funcionario_dao import inserir_funcionario_completo

class FuncionarioController:
    def __init__(self, usuario_logado):
        self.usuario_logado = usuario_logado

    def salvar_funcionario(self, dados):
        if self.usuario_logado.cargo != "GERENTE":
            return "Apenas gerentes podem cadastrar novos funcionários.", False

        try:
            sucesso = inserir_funcionario_completo(dados)
            if sucesso:
                return "Funcionário cadastrado com sucesso!", True
            else:
                return "Erro ao cadastrar funcionário. Verifique os dados.", False
        except Exception as e:
            return f"Erro no cadastro: {str(e)}", False
