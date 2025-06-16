from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QMessageBox
)
from dao.transacao_dao import TransacaoDAO
import pandas as pd
from fpdf import FPDF

class ExtratoClienteView(QWidget):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.setWindowTitle("Extrato - Últimos 30 dias")
        self.resize(700, 450)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabela = QTableWidget()
        self.layout.addWidget(self.tabela)

        self.btn_exportar_excel = QPushButton("Exportar para Excel")
        self.btn_exportar_pdf = QPushButton("Exportar para PDF")
        self.layout.addWidget(self.btn_exportar_excel)
        self.layout.addWidget(self.btn_exportar_pdf)

        self.btn_exportar_excel.clicked.connect(self.exportar_excel)
        self.btn_exportar_pdf.clicked.connect(self.exportar_pdf)

        self.transacoes = []
        self.carregar_extrato()

    def carregar_extrato(self):
        dao = TransacaoDAO()
        self.transacoes = dao.obter_transacoes_30_dias(self.id_cliente)

        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(['Data', 'Tipo', 'Valor', 'Conta Origem', 'Conta Destino'])
        self.tabela.setRowCount(len(self.transacoes))

        for i, t in enumerate(self.transacoes):
            self.tabela.setItem(i, 0, QTableWidgetItem(str(t['data_hora'])))
            self.tabela.setItem(i, 1, QTableWidgetItem(t['tipo_transacao']))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"R$ {float(t['valor']):.2f}"))
            self.tabela.setItem(i, 3, QTableWidgetItem(str(t['id_conta_origem'])))
            self.tabela.setItem(i, 4, QTableWidgetItem(str(t.get('id_conta_destino') or '')))
        self.tabela.resizeColumnsToContents()

    def exportar_excel(self):
        if not self.transacoes:
            QMessageBox.warning(self, "Erro", "Nenhuma transação para exportar.")
            return

        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar como Excel", "", "Arquivos Excel (*.xlsx)")
        if caminho:
            df = pd.DataFrame(self.transacoes)
            df.to_excel(caminho, index=False)
            QMessageBox.information(self, "Exportado", "Extrato exportado para Excel com sucesso!")

    def exportar_pdf(self):
        if not self.transacoes:
            QMessageBox.warning(self, "Erro", "Nenhuma transação para exportar.")
            return

        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar como PDF", "", "Arquivos PDF (*.pdf)")
        if caminho:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, "Extrato - Últimos 30 dias", ln=True, align="C")
            pdf.ln(5)

            colunas = ['Data', 'Tipo', 'Valor', 'Conta Origem', 'Conta Destino']
            for col in colunas:
                pdf.cell(38, 10, col, border=1)
            pdf.ln()

            for t in self.transacoes:
                pdf.cell(38, 10, str(t['data_hora']), border=1)
                pdf.cell(38, 10, t['tipo_transacao'], border=1)
                pdf.cell(38, 10, f"R$ {float(t['valor']):.2f}", border=1)
                pdf.cell(38, 10, str(t['id_conta_origem']), border=1)
                pdf.cell(38, 10, str(t.get('id_conta_destino') or ''), border=1)
                pdf.ln()

            pdf.output(caminho)
            QMessageBox.information(self, "Exportado", "Extrato exportado para PDF com sucesso!")
