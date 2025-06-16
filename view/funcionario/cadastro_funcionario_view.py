# view/funcionario/cadastro_funcionario_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QMessageBox

class CadastroFuncionarioView(QWidget):
    def __init__(self, usuario_logado, controller):
        super().__init__()
        self.usuario_logado = usuario_logado
        self.controller = controller  # Controller que gerencia cadastro no backend
        self.setWindowTitle("Cadastro de Funcionário")
        self.setGeometry(200, 200, 400, 400)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nome:"))
        self.campo_nome = QLineEdit()
        layout.addWidget(self.campo_nome)

        layout.addWidget(QLabel("CPF (apenas números):"))
        self.campo_cpf = QLineEdit()
        layout.addWidget(self.campo_cpf)

        layout.addWidget(QLabel("Data de Nascimento (YYYY-MM-DD):"))
        self.campo_data_nasc = QLineEdit()
        layout.addWidget(self.campo_data_nasc)

        layout.addWidget(QLabel("Telefone:"))
        self.campo_telefone = QLineEdit()
        layout.addWidget(self.campo_telefone)

        layout.addWidget(QLabel("Cargo:"))
        self.combo_cargo = QComboBox()
        self.combo_cargo.addItems(['ESTAGIARIO', 'ATENDENTE', 'GERENTE'])
        layout.addWidget(self.combo_cargo)

        layout.addWidget(QLabel("Senha:"))
        self.campo_senha = QLineEdit()
        self.campo_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.campo_senha)

        self.botao_cadastrar = QPushButton("Cadastrar Funcionário")
        layout.addWidget(self.botao_cadastrar)

        self.setLayout(layout)

        self.botao_cadastrar.clicked.connect(self.cadastrar_funcionario)

    def cadastrar_funcionario(self):
        nome = self.campo_nome.text().strip()
        cpf = self.campo_cpf.text().strip()
        data_nasc = self.campo_data_nasc.text().strip()
        telefone = self.campo_telefone.text().strip()
        cargo = self.combo_cargo.currentText()
        senha = self.campo_senha.text().strip()

        if not all([nome, cpf, data_nasc, telefone, cargo, senha]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return
        
        if not (cpf.isdigit() and len(cpf) == 11):
            QMessageBox.warning(self, "Erro", "CPF inválido. Deve ter 11 dígitos numéricos.")
            return

        sucesso, mensagem = self.controller.cadastrar_funcionario(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nasc,
            telefone=telefone,
            cargo=cargo,
            senha=senha
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Funcionário cadastrado com sucesso!")
            self.close()
        else:
            QMessageBox.warning(self, "Erro", f"Falha no cadastro: {mensagem}")
