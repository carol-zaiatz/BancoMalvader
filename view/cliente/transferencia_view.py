# view/cliente/transferencia_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class TransferenciaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Transferência")
        self.setGeometry(150, 150, 400, 250)
        self.usuario = usuario

        layout = QVBoxLayout()

        self.destino_input = QLineEdit()
        self.destino_input.setPlaceholderText("Número da conta destino")
        layout.addWidget(self.destino_input)

        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Valor da transferência")
        layout.addWidget(self.valor_input)

        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("Descrição (opcional)")
        layout.addWidget(self.descricao_input)

        btn_enviar = QPushButton("Confirmar Transferência")
        btn_enviar.clicked.connect(self.enviar_transferencia)
        layout.addWidget(btn_enviar)

        self.setLayout(layout)

    def enviar_transferencia(self):
        conta_destino = self.destino_input.text()
        valor = self.valor_input.text()

        if not conta_destino or not valor:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        # Aqui você chamaria o controller para processar a transferência
        QMessageBox.information(self, "Sucesso", "Transferência realizada com sucesso.")
        self.close()
