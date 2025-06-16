# view/cliente/limite_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from dao.usuario_dao import consultar_limite

class LimiteView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Consultar Limite")
        self.setGeometry(150, 150, 300, 200)
        self.usuario = usuario

        layout = QVBoxLayout()

        cpf = usuario.cpf
        limite_atual = consultar_limite(cpf)

        if limite_atual >= 3000:
            previsao = "R$ 4.500,00 (com score acima de 90)"
        elif limite_atual >= 2000:
            previsao = "R$ 3.000,00 (com score acima de 80)"
        else:
            previsao = "R$ 2.000,00 (com score acima de 70)"

        layout.addWidget(QLabel(f"Limite atual: R$ {limite_atual:,.2f}"))
        layout.addWidget(QLabel(f"Previsão de aumento: {previsao}"))

        self.setLayout(layout)
