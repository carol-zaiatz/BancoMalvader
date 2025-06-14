# view/funcionario/relatorios_view.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
from controller.relatorios_controller import RelatoriosController

class RelatoriosView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controller = RelatoriosController(usuario)

        self.setWindowTitle(f"Relatórios - {usuario.nome}")
        self.setGeometry(150, 150, 600, 400)

        main_layout = QVBoxLayout()

        # Filtros
        filtro_layout = QHBoxLayout()

        filtro_layout.addWidget(QLabel("Tipo do Relatório:"))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItem("Todos", "")
        self.combo_tipo.addItem("Financeiro", "FINANCEIRO")
        self.combo_tipo.addItem("Operacional", "OPERACIONAL")
        filtro_layout.addWidget(self.combo_tipo)

        filtro_layout.addWidget(QLabel("Data Inicial:"))
        self.data_inicio = QDateEdit()
        self.data_inicio.setCalendarPopup(True)
        self.data_inicio.setDate(QDate.currentDate().addMonths(-1))
        filtro_layout.addWidget(self.data_inicio)

        filtro_layout.addWidget(QLabel("Data Final:"))
        self.data_fim = QDateEdit()
        self.data_fim.setCalendarPopup(True)
        self.data_fim.setDate(QDate.currentDate())
        filtro_layout.addWidget(self.data_fim)

        self.btn_filtrar = QPushButton("Filtrar")
        filtro_layout.addWidget(self.btn_filtrar)

        main_layout.addLayout(filtro_layout)

        # Tabela de relatórios
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["ID", "Tipo", "Data Geração", "Conteúdo"])
        self.tabela.setColumnWidth(3, 300)
        main_layout.addWidget(self.tabela)

        self.setLayout(main_layout)

        # Conectar botão
        self.btn_filtrar.clicked.connect(self.carregar_relatorios)

        # Carrega relatório inicial
        self.carregar_relatorios()

    def carregar_relatorios(self):
    try:
        contas, movimentacoes, scores = self.controller.obter_dados_relatórios()

        # Carregar Resumo de Contas
        self.tabela_contas.setColumnCount(len(contas[0]) if contas else 0)
        self.tabela_contas.setRowCount(len(contas))
        self.tabela_contas.setHorizontalHeaderLabels(contas[0].keys() if contas else [])
        for i, conta in enumerate(contas):
            for j, (key, value) in enumerate(conta.items()):
                self.tabela_contas.setItem(i, j, QTableWidgetItem(str(value)))

        # Carregar Movimentações
        self.tabela_mov.setColumnCount(len(movimentacoes[0]) if movimentacoes else 0)
        self.tabela_mov.setRowCount(len(movimentacoes))
        self.tabela_mov.setHorizontalHeaderLabels(movimentacoes[0].keys() if movimentacoes else [])
        for i, mov in enumerate(movimentacoes):
            for j, (key, value) in enumerate(mov.items()):
                self.tabela_mov.setItem(i, j, QTableWidgetItem(str(value)))

        # Carregar Scores
        self.tabela_scores.setColumnCount(len(scores[0]) if scores else 0)
        self.tabela_scores.setRowCount(len(scores))
        self.tabela_scores.setHorizontalHeaderLabels(scores[0].keys() if scores else [])
        for i, sc in enumerate(scores):
            for j, (key, value) in enumerate(sc.items()):
                self.tabela_scores.setItem(i, j, QTableWidgetItem(str(value)))

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Erro ao carregar relatórios: {str(e)}")