from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class EncerramentoContaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Encerramento de Conta")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de encerramento de conta (em construção)"))
        self.setLayout(layout)
