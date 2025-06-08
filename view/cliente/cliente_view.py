# view/cliente/cliente_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from .saldo_view import SaldoView
from .transferencia_view import TransferenciaView
from .extrato_view import ExtratoView
from .limite_view import LimiteView

class ClienteView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"Cliente - {usuario.nome}")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Bem-vindo, {usuario.nome}!"))

        btn_saldo = QPushButton("Ver Saldo")
        btn_saldo.clicked.connect(self.abrir_saldo)
        layout.addWidget(btn_saldo)

        btn_transferencia = QPushButton("Fazer Transferência")
        btn_transferencia.clicked.connect(self.abrir_transferencia)
        layout.addWidget(btn_transferencia)

        btn_extrato = QPushButton("Consultar Extrato")
        btn_extrato.clicked.connect(self.abrir_extrato)
        layout.addWidget(btn_extrato)

        btn_limite = QPushButton("Consultar Limite")
        btn_limite.clicked.connect(self.abrir_limite)
        layout.addWidget(btn_limite)

        btn_sair = QPushButton("Encerrar Sessão")
        btn_sair.clicked.connect(self.close)
        layout.addWidget(btn_sair)

        self.setLayout(layout)

    def abrir_saldo(self):
        self.saldo_view = SaldoView(self.usuario)
        self.saldo_view.show()

    def abrir_transferencia(self):
        self.transf_view = TransferenciaView(self.usuario)
        self.transf_view.show()

    def abrir_extrato(self):
        self.extrato_view = ExtratoView(self.usuario)
        self.extrato_view.show()

    def abrir_limite(self):
        self.limite_view = LimiteView(self.usuario)
        self.limite_view.show()
