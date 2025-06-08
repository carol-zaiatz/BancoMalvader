from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class CadastroFuncionarioView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Cadastro de Funcionário")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de cadastro de funcionário (em construção)"))
        self.setLayout(layout)
