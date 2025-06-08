# view/cliente/limite_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class LimiteView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Consultar Limite")
        self.setGeometry(150, 150, 300, 200)
        self.usuario = usuario

        layout = QVBoxLayout()

        # Dados simulados, que viriam do controller com base no score
        limite_atual = "R$ 2.000,00"
        previsao_aumento = "R$ 3.000,00 (com score acima de 80)"

        layout.addWidget(QLabel(f"Limite atual: {limite_atual}"))
        layout.addWidget(QLabel(f"Previsão de aumento: {previsao_aumento}"))

        self.setLayout(layout)
