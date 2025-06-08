# view/cliente/saldo_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class SaldoView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Saldo da Conta")
        self.setGeometry(150, 150, 300, 200)
        self.usuario = usuario

        layout = QVBoxLayout()

        # Estes dados viriam do controller (simulados aqui)
        saldo_atual = "R$ 8.500,00"
        rendimento_estimado = "R$ 120,00/mês"

        layout.addWidget(QLabel(f"Saldo atual: {saldo_atual}"))
        layout.addWidget(QLabel(f"Projeção de rendimentos: {rendimento_estimado}"))

        self.setLayout(layout)
