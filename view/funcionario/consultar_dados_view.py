# view/funcionario/consultar_dados_view.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from controller.consulta_cliente_controller import ConsultaClienteController


class ConsultarDadosClienteView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de Cliente por CPF")
        self.setGeometry(200, 200, 500, 400)

        self.controller = ConsultaClienteController()

        layout = QVBoxLayout()

        # Campo para CPF
        self.campo_cpf = QLineEdit()
        self.campo_cpf.setPlaceholderText("Digite o CPF do cliente")
        layout.addWidget(QLabel("CPF do Cliente:"))
        layout.addWidget(self.campo_cpf)

        # Botão de consulta
        self.botao_consultar = QPushButton("Consultar")
        self.botao_consultar.clicked.connect(self.consultar_cliente)
        layout.addWidget(self.botao_consultar)

        # Labels de exibição
        self.label_nome = QLabel("Nome:")
        self.label_telefone = QLabel("Telefone:")
        self.label_tipo = QLabel("Tipo de Usuário:")
        layout.addWidget(self.label_nome)
        layout.addWidget(self.label_telefone)
        layout.addWidget(self.label_tipo)

        layout.addWidget(QLabel("Contas Ativas:"))

        # Lista de contas
        self.lista_contas = QListWidget()
        layout.addWidget(self.lista_contas)

        self.setLayout(layout)

    def consultar_cliente(self):
        cpf = self.campo_cpf.text().strip()
        if not cpf:
            QMessageBox.warning(self, "Aviso", "Digite um CPF válido.")
            return

        try:
            dados = self.controller.get_dados_cliente(cpf)
            if dados:
                self.label_nome.setText(f"Nome: {dados['nome']}")
                self.label_telefone.setText(f"Telefone: {dados['telefone']}")
                self.label_tipo.setText(f"Tipo de Usuário: {dados['tipo_usuario']}")
            else:
                QMessageBox.warning(self, "Aviso", "Cliente não encontrado.")
                return

            contas = self.controller.get_contas_ativas(cpf)
            self.lista_contas.clear()
            if contas:
                for conta in contas:
                    texto = (
                        f"Número: {conta['numero_conta']} | "
                        f"Tipo: {conta['tipo_conta']} | "
                        f"Saldo: R$ {conta['saldo']:.2f}"
                    )
                    self.lista_contas.addItem(QListWidgetItem(texto))
            else:
                self.lista_contas.addItem(QListWidgetItem("Nenhuma conta ativa encontrada."))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao consultar cliente: {str(e)}")