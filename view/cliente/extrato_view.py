# view/cliente/extrato_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem

class ExtratoView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Extrato da Conta")
        self.setGeometry(150, 150, 500, 300)
        self.usuario = usuario

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Últimas transações"))

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Data", "Tipo", "Valor", "Descrição"])

        # Dados simulados (normalmente obtidos via controller)
        transacoes = [
            ("01/06/2025", "Depósito", "R$ 1.000,00", "Salário"),
            ("02/06/2025", "Saque", "R$ 200,00", "Caixa 24h"),
            ("03/06/2025", "Transferência", "R$ 300,00", "Para João")
        ]

        self.tabela.setRowCount(len(transacoes))
        for i, transacao in enumerate(transacoes):
            for j, valor in enumerate(transacao):
                self.tabela.setItem(i, j, QTableWidgetItem(valor))

        layout.addWidget(self.tabela)
        self.setLayout(layout)
