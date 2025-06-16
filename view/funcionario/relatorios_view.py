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
            tipo = self.combo_tipo.currentData()
            data_inicio = self.data_inicio.date().toPyDate()
            data_fim = self.data_fim.date().toPyDate()

            relatorios = self.controller.obter_relatorios_filtrados(tipo, data_inicio, data_fim)

            self.tabela.setRowCount(len(relatorios))

            for i, relatorio in enumerate(relatorios):
                self.tabela.setItem(i, 0, QTableWidgetItem(str(relatorio['id'])))
                self.tabela.setItem(i, 1, QTableWidgetItem(relatorio['tipo']))
                self.tabela.setItem(i, 2, QTableWidgetItem(relatorio['data_geracao'].strftime('%d/%m/%Y')))
                self.tabela.setItem(i, 3, QTableWidgetItem(relatorio['conteudo']))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar relatórios: {str(e)}")