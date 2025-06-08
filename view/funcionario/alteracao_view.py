from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class AlteracaoView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Alteração de Dados")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de alteração de dados (em construção)"))
        self.setLayout(layout)
