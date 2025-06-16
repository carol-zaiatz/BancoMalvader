# view/cliente/saldo_view.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from dao.conexao import conectar
from dao.usuario_dao import buscar_saldo_por_cpf
from dao.conta_dao import ContaDAO

class SaldoClienteView(QWidget):

    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.setWindowTitle("Saldo Consolidado")
        self.resize(300, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_saldo = QLabel("Carregando saldo...")
        layout.addWidget(self.label_saldo)

        self.carregar_saldo()

    def carregar_saldo(self):
        dao = ContaDAO()
        saldo = dao.obter_saldo_consolidado(self.id_cliente)
        self.label_saldo.setText(f"Saldo total: R$ {saldo:.2f}")
    
    def __init__(self, cpf_cliente, voltar_callback):
        super().__init__()
        self.cpf_cliente = cpf_cliente
        self.voltar_callback = voltar_callback
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
        conexao = conectar()
        cursor = conexao.cursor()
        resultados = buscar_saldo_por_cpf(self.cpf_cliente)

        try:
            query = """
                SELECT c.tipo_conta, c.saldo, c.rendimento
                FROM conta c
                JOIN cliente cl ON c.cliente_id = cl.id
                WHERE cl.cpf = %s;
            """
            cursor.execute(query, (self.cpf_cliente,))
            resultados = cursor.fetchall()

            if not resultados:
                self.label_saldo.setText("Conta não encontrada.")
            else:
                texto = ""
                for tipo, saldo, rendimento in resultados:
                    texto += f"{tipo}: R${saldo:.2f} (+Rend. R${rendimento:.2f})\n"
                self.label_saldo.setText(texto)

        except Exception as e:
            self.label_saldo.setText(f"Erro ao buscar saldo: {e}")

        cursor.close()
        conexao.close()