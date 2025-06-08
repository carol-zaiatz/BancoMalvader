from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class AberturaContaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Abertura de Conta")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de abertura de conta (em construção)"))
        self.setLayout(layout)
