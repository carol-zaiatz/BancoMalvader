# view/cliente/transferencia_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from dao.usuario_dao import transferir_valor
from dao.transacao_dao import TransacaoDAO

class TransferenciaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Transferência")
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_cpf_destino = QLineEdit()
        self.input_cpf_destino.setPlaceholderText("CPF do destinatário")
        layout.addWidget(self.input_cpf_destino)

        self.input_valor = QLineEdit()
        self.input_valor.setPlaceholderText("Valor a transferir")
        layout.addWidget(self.input_valor)

        self.btn_transferir = QPushButton("Transferir")
        self.btn_transferir.clicked.connect(self.realizar_transferencia)
        layout.addWidget(self.btn_transferir)

        self.setLayout(layout)

    def realizar_transferencia(self):
        cpf_destino = self.input_cpf_destino.text()
        try:
            valor = float(self.input_valor.text())
        except ValueError:
            QMessageBox.warning(self, "Erro", "Digite um valor válido.")
            return

        if cpf_destino == self.usuario.cpf:
            QMessageBox.warning(self, "Erro", "Não é possível transferir para si mesmo.")
            return

        resultado = transferir_valor(self.usuario.cpf, cpf_destino, valor)
        QMessageBox.information(self, "Resultado", resultado)

        