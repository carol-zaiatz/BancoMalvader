from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class AlteracaoView(QWidget):
    def __init__(self, usuario, controller):
        super().__init__()
        self.usuario = usuario
        self.controller = controller
        self.setWindowTitle("Alterar Dados")
        self.setGeometry(200, 200, 400, 300)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Usuário: {usuario.nome} (CPF: {usuario.cpf})"))

        layout.addWidget(QLabel("Telefone:"))
        self.campo_telefone = QLineEdit()
        self.campo_telefone.setText(usuario.telefone)
        layout.addWidget(self.campo_telefone)

        layout.addWidget(QLabel("Senha (nova):"))
        self.campo_senha = QLineEdit()
        self.campo_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.campo_senha)

        self.botao_salvar = QPushButton("Salvar Alterações")
        layout.addWidget(self.botao_salvar)

        self.setLayout(layout)
        self.botao_salvar.clicked.connect(self.salvar_alteracoes)

    def salvar_alteracoes(self):
        telefone_novo = self.campo_telefone.text().strip()
        senha_nova = self.campo_senha.text().strip()

        if not telefone_novo:
            QMessageBox.warning(self, "Erro", "Telefone não pode ser vazio.")
            return

        sucesso, mensagem = self.controller.atualizar_usuario(
            self.usuario.id_usuario,
            telefone=telefone_novo,
            senha=senha_nova if senha_nova else None
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Dados atualizados com sucesso!")
            self.close()
        else:
            QMessageBox.warning(self, "Erro", f"Falha na atualização: {mensagem}")

