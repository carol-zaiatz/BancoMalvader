# # view/cliente/extrato_view.py
# from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem
# from dao.usuario_dao import buscar_extrato  # IMPORTANTE

# class ExtratoView(QWidget):
#     def __init__(self, usuario):
#         super().__init__()
#         self.setWindowTitle("Extrato da Conta")
#         self.setGeometry(150, 150, 600, 400)
#         self.usuario = usuario

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("Últimas transações"))

#         self.tabela = QTableWidget()
#         self.tabela.setColumnCount(4)
#         self.tabela.setHorizontalHeaderLabels(["Data", "Tipo", "Valor", "Descrição"])
#         layout.addWidget(self.tabela)

#         self.setLayout(layout)
#         self.carregar_dados()

#     def carregar_dados(self):
#         transacoes = buscar_extrato(self.usuario.cpf)

#         self.tabela.setRowCount(len(transacoes))
#         for i, t in enumerate(transacoes):
#             data_formatada = t["data"].strftime("%d/%m/%Y %H:%M") if hasattr(t["data"], "strftime") else str(t["data"])
#             self.tabela.setItem(i, 0, QTableWidgetItem(data_formatada))
#             self.tabela.setItem(i, 1, QTableWidgetItem(t["tipo"].capitalize()))
#             self.tabela.setItem(i, 2, QTableWidgetItem(f"R$ {t['valor']:.2f}"))
#             self.tabela.setItem(i, 3, QTableWidgetItem(t["descricao"]))

# view/extrato_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from dao.transacao_dao import TransacaoDAO  # Você vai precisar criar este DAO

class ExtratoClienteView(QWidget):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.setWindowTitle("Extrato - Últimos 30 dias")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabela = QTableWidget()
        self.layout.addWidget(self.tabela)
        self.carregar_extrato()

    def carregar_extrato(self):
        dao = TransacaoDAO()
        transacoes = dao.obter_transacoes_30_dias(self.id_cliente)
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(['Data', 'Tipo', 'Valor', 'Conta Origem', 'Conta Destino'])
        self.tabela.setRowCount(len(transacoes))

        for i, t in enumerate(transacoes):
            self.tabela.setItem(i, 0, QTableWidgetItem(str(t['data_hora'])))
            self.tabela.setItem(i, 1, QTableWidgetItem(t['tipo_transacao']))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"R$ {t['valor']:.2f}"))
            self.tabela.setItem(i, 3, QTableWidgetItem(str(t['id_conta_origem'])))
            self.tabela.setItem(i, 4, QTableWidgetItem(str(t.get('id_conta_destino', ''))))
        self.tabela.resizeColumnsToContents()