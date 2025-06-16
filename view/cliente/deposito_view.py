from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from dao.usuario_dao import realizar_deposito

class DepositoView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Depósito")
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Valor do depósito")
        layout.addWidget(QLabel("Informe o valor a depositar:"))
        layout.addWidget(self.valor_input)

        btn_depositar = QPushButton("Depositar")
        btn_depositar.clicked.connect(self.depositar)
        layout.addWidget(btn_depositar)

        self.setLayout(layout)

    def depositar(self):
        try:
            valor = float(self.valor_input.text())
            if valor <= 0:
                raise ValueError("Valor deve ser positivo.")

            sucesso, mensagem = realizar_deposito(self.usuario.cpf, valor)
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.close()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

        except ValueError:
            QMessageBox.warning(self, "Erro", "Digite um valor numérico válido.")
