# view/funcionario/funcionario_abertura_view.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox,
    QLineEdit, QPushButton, QMessageBox
)
from controller.abertura_conta_controller import AberturaContaController

class AberturaContaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controller = AberturaContaController(usuario)

        self.setWindowTitle(f"Abertura de Conta - {usuario.nome}")
        self.setGeometry(150, 150, 350, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Selecione o cliente para a conta:"))
        self.combo_clientes = QComboBox()
        layout.addWidget(self.combo_clientes)

        layout.addWidget(QLabel("Tipo de Conta:"))
        self.combo_tipo_conta = QComboBox()
        self.combo_tipo_conta.addItems(["CORRENTE", "POUPANCA", "INVESTIMENTO"])
        layout.addWidget(self.combo_tipo_conta)

        layout.addWidget(QLabel("Número da Conta:"))
        self.input_numero_conta = QLineEdit()
        layout.addWidget(self.input_numero_conta)

        self.btn_criar = QPushButton("Abrir Conta")
        layout.addWidget(self.btn_criar)

        self.setLayout(layout)

        self.btn_criar.clicked.connect(self.abrir_conta)

        self.carregar_clientes()

    def carregar_clientes(self):
        try:
            clientes = self.controller.get_clientes()
            self.combo_clientes.clear()
            if clientes:
                for cliente in clientes:
                    # Guarda id_cliente no combo junto com o nome
                    self.combo_clientes.addItem(cliente['nome'], cliente['id_cliente'])
            else:
                self.combo_clientes.addItem("Nenhum cliente encontrado")
                self.btn_criar.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar clientes: {str(e)}")

    def abrir_conta(self):
        id_cliente = self.combo_clientes.currentData()
        tipo_conta = self.combo_tipo_conta.currentText()
        numero_conta = self.input_numero_conta.text().strip()

        if not id_cliente:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente válido.")
            return
        if not numero_conta:
            QMessageBox.warning(self, "Aviso", "Informe o número da conta.")
            return

        sucesso, msg = self.controller.criar_conta(id_cliente, tipo_conta, numero_conta)
        if sucesso:
            QMessageBox.information(self, "Sucesso", msg)
            self.input_numero_conta.clear()
        else:
            QMessageBox.warning(self, "Erro", msg)
