from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class RelatoriosView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Geração de Relatórios")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de geração de relatórios (em construção)"))
        self.setLayout(layout)
