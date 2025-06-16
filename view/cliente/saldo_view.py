from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from dao.conexao import conectar
from dao.usuario_dao import buscar_saldo_por_cpf

class SaldoClienteView(QWidget):
    def __init__(self, cpf_cliente, voltar_callback):
        super().__init__()
        self.cpf_cliente = cpf_cliente
        self.voltar_callback = voltar_callback
        self.setWindowTitle("Saldo da Conta")
        self.resize(300, 200)
        self.init_ui()
        self.buscar_saldo()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.label_saldo = QLabel("Saldo: Carregando...")
        self.layout.addWidget(self.label_saldo)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(self.voltar_callback)
        self.layout.addWidget(self.btn_voltar)

        self.setLayout(self.layout)

    def buscar_saldo(self):
        try:
            resultados = buscar_saldo_por_cpf(self.cpf_cliente)
            if not resultados:
                self.label_saldo.setText("Conta não encontrada.")
            else:
                texto = ""
                for linha in resultados:
                    tipo = linha["tipo_conta"]
                    saldo = float(linha["saldo"])
                    rendimento = float(linha["rendimento"])
                    texto += f"{tipo}: R${saldo:.2f} (+Rend. R${rendimento:.2f})\n"
                self.label_saldo.setText(texto)
        except Exception as e:
            self.label_saldo.setText(f"Erro ao buscar saldo: {e}")
