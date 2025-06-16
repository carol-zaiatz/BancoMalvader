from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from dao.usuario_dao import realizar_saque

class SaqueView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Saque")
        self.setGeometry(100, 100, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Digite o valor do saque:")
        layout.addWidget(self.label)

        self.input_valor = QLineEdit()
        layout.addWidget(self.input_valor)

        btn_sacar = QPushButton("Confirmar Saque")
        btn_sacar.clicked.connect(self.sacar)
        layout.addWidget(btn_sacar)

        self.setLayout(layout)

    def sacar(self):
        try:
            valor = float(self.input_valor.text())
            sucesso, msg = realizar_saque(self.usuario.cpf, valor)
            if sucesso:
                QMessageBox.information(self, "Sucesso", msg)
                self.close()
            else:
                QMessageBox.warning(self, "Erro", msg)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Digite um valor numérico válido.")
