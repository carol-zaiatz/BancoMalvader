from dao.conta_dao import inserir_cliente_e_conta # Vamos criar este arquivo e função a seguir
from hashlib import md5

def salvar_nova_conta(dados):
    """
    Controller para orquestrar a criação de um novo cliente e sua conta.
    Recebe os dados da view, prepara e envia para o DAO.
    """
    try:
        # 1. Validar se o funcionário está logado (já é feito na view)
        # 2. Preparar os dados (ex: criptografar a senha)
        dados["senha_hash"] = md5(dados["senha"].encode()).hexdigest()

        # 3. Chamar o DAO para inserir no banco de dados
        sucesso = inserir_cliente_e_conta(dados)
        
        if sucesso:
            return "Conta criada com sucesso!", True
        else:
            # Esta condição pode não ser atingida se o DAO levantar uma exceção,
            # mas é uma boa prática mantê-la.
            return "Não foi possível criar a conta. Verifique os dados.", False
            
    except Exception as e:
        # Captura qualquer erro vindo do DAO (ex: CPF duplicado)
        print(f"[ERRO] no controller: {e}")
        return f"Erro ao criar conta: {str(e)}", False