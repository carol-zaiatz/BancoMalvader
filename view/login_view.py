from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controller.login_controller import LoginController

class LoginView(QWidget):
    def __init__(self, tipo_usuario):
        super().__init__()
        self.tipo_usuario = tipo_usuario  # armazenar para controle
        self.setWindowTitle(f"Banco Malvader - Login ({tipo_usuario.title()})")
        self.setGeometry(100, 100, 300, 250)
        layout = QVBoxLayout()

        self.label = QLabel("CPF:")
        self.campo_cpf = QLineEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.campo_cpf)

        self.label_senha = QLabel("Senha:")
        self.campo_senha = QLineEdit()
        self.campo_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_senha)
        layout.addWidget(self.campo_senha)

        self.label_otp = QLabel("OTP:")
        self.campo_otp = QLineEdit()
        layout.addWidget(self.label_otp)
        layout.addWidget(self.campo_otp)

        self.botao_gerar_otp = QPushButton("Gerar OTP")
        self.botao_login = QPushButton("Entrar")

        layout.addWidget(self.botao_gerar_otp)
        layout.addWidget(self.botao_login)

        self.setLayout(layout)

        self.controller = LoginController(self)
        self.botao_login.clicked.connect(self.login)
        self.botao_gerar_otp.clicked.connect(self.gerar_otp)

    def login(self):
        cpf = self.campo_cpf.text()
        senha = self.campo_senha.text()
        otp = self.campo_otp.text()
        self.controller.autenticar(cpf, senha, otp)

    def gerar_otp(self):
        cpf = self.campo_cpf.text()
        self.controller.gerar_otp(cpf)
