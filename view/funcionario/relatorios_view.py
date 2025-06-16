from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
from controller.relatorios_controller import RelatoriosController
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table

class RelatoriosView(QWidget):
    def __init__(self, usuario, controller):
        super().__init__()
        self.usuario = usuario
        self.controller = controller

        self.setWindowTitle(f"Relatórios - {usuario.nome}")
        self.setGeometry(150, 150, 800, 500)

        main_layout = QVBoxLayout()
        filtro_layout = QHBoxLayout()

        filtro_layout.addWidget(QLabel("Tipo do Relatório:"))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItem("Movimentações", "MOVIMENTACOES")
        self.combo_tipo.addItem("Inadimplência", "INADIMPLENCIA")
        self.combo_tipo.addItem("Desempenho de Funcionários", "DESEMPENHO")
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
        self.btn_excel = QPushButton("Exportar Excel")
        self.btn_pdf = QPushButton("Exportar PDF")

        filtro_layout.addWidget(self.btn_filtrar)
        filtro_layout.addWidget(self.btn_excel)
        filtro_layout.addWidget(self.btn_pdf)

        main_layout.addLayout(filtro_layout)

        self.tabela = QTableWidget()
        main_layout.addWidget(self.tabela)

        self.setLayout(main_layout)

        self.btn_filtrar.clicked.connect(self.carregar_relatorios)
        self.btn_excel.clicked.connect(self.exportar_excel)
        self.btn_pdf.clicked.connect(self.exportar_pdf)

        self.carregar_relatorios()

    def carregar_relatorios(self):
        try:
            self.tipo = self.combo_tipo.currentData()
            self.data_inicio_val = self.data_inicio.date().toPyDate()
            self.data_fim_val = self.data_fim.date().toPyDate()

            self.relatorios = self.controller.obter_relatorios(
                self.tipo, self.data_inicio_val, self.data_fim_val
            )

            if not self.relatorios:
                self.tabela.setRowCount(0)
                return

            headers = list(self.relatorios[0].keys())
            self.tabela.setColumnCount(len(headers))
            self.tabela.setHorizontalHeaderLabels(headers)
            self.tabela.setRowCount(len(self.relatorios))

            for i, row in enumerate(self.relatorios):
                for j, key in enumerate(headers):
                    self.tabela.setItem(i, j, QTableWidgetItem(str(row[key])))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar relatórios: {str(e)}")

    def exportar_excel(self):
        if not self.relatorios:
            QMessageBox.warning(self, "Aviso", "Nenhum dado para exportar.")
            return
        df = pd.DataFrame(self.relatorios)
        df.to_excel("relatorio.xlsx", index=False)
        QMessageBox.information(self, "Sucesso", "Relatório exportado como Excel.")

    def exportar_pdf(self):
        if not self.relatorios:
            QMessageBox.warning(self, "Aviso", "Nenhum dado para exportar.")
            return

        doc = SimpleDocTemplate("relatorio.pdf")
        headers = list(self.relatorios[0].keys())
        data = [headers] + [[str(item[col]) for col in headers] for item in self.relatorios]
        table = Table(data)
        doc.build([table])
        QMessageBox.information(self, "Sucesso", "Relatório exportado como PDF.")
