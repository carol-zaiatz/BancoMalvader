from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from dao.conta_dao import ContaDAO

class AbrirContaView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Abrir Conta")
        self.resize(400, 250)
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("CPF do Cliente:"))
        self.cpf_input = QLineEdit()
        layout.addWidget(self.cpf_input)

        layout.addWidget(QLabel("Tipo de Conta:"))
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(['POUPANCA', 'CORRENTE', 'INVESTIMENTO'])
        layout.addWidget(self.tipo_combo)

        layout.addWidget(QLabel("Saldo Inicial:"))
        self.saldo_input = QLineEdit()
        layout.addWidget(self.saldo_input)

        btn_abrir = QPushButton("Abrir Conta")
        btn_abrir.clicked.connect(self.abrir_conta)
        layout.addWidget(btn_abrir)

    def abrir_conta(self):
        cpf = self.cpf_input.text()
        tipo = self.tipo_combo.currentText()
        try:
            saldo = float(self.saldo_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erro", "Saldo inválido")
            return

        dao = ContaDAO()
        sucesso, msg = dao.abrir_conta(cpf, tipo, saldo)
        if sucesso:
            QMessageBox.information(self, "Sucesso", "Conta aberta com sucesso")
            self.close()
        else:
            QMessageBox.warning(self, "Erro", msg)