# view/tipo_usuario_view.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from view.login_view import LoginView

class TipoUsuarioView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banco Malvader - Tipo de Usuário")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Escolha o tipo de usuário:"))

        self.btn_cliente = QPushButton("Cliente")
        self.btn_funcionario = QPushButton("Funcionário")
        self.btn_sair = QPushButton("Sair")

        layout.addWidget(self.btn_cliente)
        layout.addWidget(self.btn_funcionario)
        layout.addWidget(self.btn_sair)

        self.setLayout(layout)

        self.btn_cliente.clicked.connect(lambda: self.abrir_login("CLIENTE"))
        self.btn_funcionario.clicked.connect(lambda: self.abrir_login("FUNCIONARIO"))
        self.btn_sair.clicked.connect(self.close)

    def abrir_login(self, tipo):
        self.login_view = LoginView(tipo)
        self.login_view.show()
        self.close()
