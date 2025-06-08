from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ConsultaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Consulta de Dados")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de consulta de dados (em construção)"))
        self.setLayout(layout)
