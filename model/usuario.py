class Usuario:
    def __init__(self, id_usuario, nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, otp_ativo=None, otp_expiracao=None):
        self.id = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.tipo_usuario = tipo_usuario
        self.senha_hash = senha_hash
        self.otp_ativo = otp_ativo
        self.otp_expiracao = otp_expiracao
