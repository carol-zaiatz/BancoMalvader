class Usuario:
    def __init__(self, id_usuario, nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, otp_ativo=None, otp_expiracao=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.tipo_usuario = tipo_usuario
        self.senha_hash = senha_hash
        self.otp_ativo = otp_ativo
        self.otp_expiracao = otp_expiracao

    @classmethod
    def from_dict(cls, dados):
        """Permite criar um objeto Usuario diretamente de um dicionário (ex: resultado do cursor)."""
        return cls(
            id_usuario=dados.get("id_usuario"),
            nome=dados.get("nome"),
            cpf=dados.get("cpf"),
            data_nascimento=dados.get("data_nascimento"),
            telefone=dados.get("telefone"),
            tipo_usuario=dados.get("tipo_usuario"),
            senha_hash=dados.get("senha_hash"),
            otp_ativo=dados.get("otp_ativo"),
            otp_expiracao=dados.get("otp_expiracao"),
        )
