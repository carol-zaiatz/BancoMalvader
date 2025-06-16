from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from .transferencia_view import TransferenciaView
from .extrato_view import ExtratoClienteView
from .limite_view import LimiteView
from .saldo_view import SaldoClienteView
from .deposito_view import DepositoView
from .saque_view import SaqueView  # Opcional, se você já criou
from dao.usuario_dao import buscar_id_cliente_por_id_usuario

class ClienteView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"Cliente - {usuario.nome}")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Bem-vindo, {usuario.nome}!"))

        btn_saldo = QPushButton("Ver Saldo")
        btn_transferencia = QPushButton("Fazer Transferência")
        btn_extrato = QPushButton("Consultar Extrato")
        btn_limite = QPushButton("Consultar Limite")
        btn_deposito = QPushButton("Realizar Depósito")
        btn_saque = QPushButton("Realizar Saque")  # Novo botão (opcional)
        btn_sair = QPushButton("Encerrar Sessão")

        btn_saldo.clicked.connect(self.abrir_saldo)
        btn_transferencia.clicked.connect(self.abrir_transferencia)
        btn_extrato.clicked.connect(self.abrir_extrato)
        btn_limite.clicked.connect(self.abrir_limite)
        btn_deposito.clicked.connect(self.abrir_deposito)
        btn_saque.clicked.connect(self.abrir_saque)
        btn_sair.clicked.connect(self.close)

        layout.addWidget(btn_saldo)
        layout.addWidget(btn_transferencia)
        layout.addWidget(btn_extrato)
        layout.addWidget(btn_limite)
        layout.addWidget(btn_deposito)
        layout.addWidget(btn_saque)
        layout.addWidget(btn_sair)

        self.setLayout(layout)

    def abrir_saldo(self):
        self.saldo_view = SaldoClienteView(self.usuario.cpf, self.show)
        self.saldo_view.show()
        self.hide()

    def abrir_transferencia(self):
        self.transf_view = TransferenciaView(self.usuario)
        self.transf_view.show()

    def abrir_extrato(self):
        id_cliente = buscar_id_cliente_por_id_usuario(self.usuario.id_usuario)
        if id_cliente is None:
            QMessageBox.warning(self, "Erro", "ID do cliente não encontrado.")
            return
        self.extrato_view = ExtratoClienteView(id_cliente)
        self.extrato_view.show()

    def abrir_limite(self):
        self.limite_view = LimiteView(self.usuario)
        self.limite_view.show()

    def abrir_deposito(self):
        self.deposito_view = DepositoView(self.usuario)
        self.deposito_view.show()

    def abrir_saque(self):
        self.saque_view = SaqueView(self.usuario)
        self.saque_view.show()
