from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from view.funcionario.abertura_conta_view import AberturaContaView
from view.funcionario.encerramento_conta_view import EncerramentoContaView
from view.funcionario.consulta_view import ConsultaView
from view.funcionario.alteracao_view import AlteracaoView
from view.funcionario.cadastro_funcionario_view import CadastroFuncionarioView
from view.funcionario.relatorios_view import RelatoriosView
from controller.relatorios_controller import RelatoriosController

class FuncionarioView(QWidget):
    def __init__(self, usuario, controller):
        super().__init__()
        self.usuario = usuario
        self.controller = controller
        self.setWindowTitle(f"Funcionário - {usuario.nome}")
        self.setGeometry(100, 100, 400, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Bem-vindo, {usuario.nome}!"))
        layout.addWidget(QLabel("Menu do Funcionário:"))

        self.btn_abertura = QPushButton("Abrir Conta")
        self.btn_encerramento = QPushButton("Encerrar Conta")
        self.btn_consulta = QPushButton("Consultar Dados")
        self.btn_alteracao = QPushButton("Alterar Dados")
        self.btn_cadastro = QPushButton("Cadastrar Funcionário")
        self.btn_relatorios = QPushButton("Relatórios")
        self.btn_logout = QPushButton("Encerrar Sessão")

        layout.addWidget(self.btn_abertura)
        layout.addWidget(self.btn_encerramento)
        layout.addWidget(self.btn_consulta)
        layout.addWidget(self.btn_alteracao)
        layout.addWidget(self.btn_cadastro)
        layout.addWidget(self.btn_relatorios)
        layout.addWidget(self.btn_logout)

        self.setLayout(layout)

        # Conectar botões às funções
        self.btn_abertura.clicked.connect(self.abrir_abertura_conta)
        self.btn_encerramento.clicked.connect(self.abrir_encerramento_conta)
        self.btn_consulta.clicked.connect(self.abrir_consulta)
        self.btn_alteracao.clicked.connect(self.abrir_alteracao)
        self.btn_cadastro.clicked.connect(self.abrir_cadastro)
        self.btn_relatorios.clicked.connect(self.abrir_relatorios)
        self.btn_logout.clicked.connect(self.close)

    def abrir_abertura_conta(self):
        self.abertura_view = AberturaContaView(self.usuario, self.controller)
        self.abertura_view.show()

    def abrir_encerramento_conta(self):
        self.encerramento_view = EncerramentoContaView(self.usuario)  
        self.encerramento_view.show()

    def abrir_consulta(self):
        self.consulta_view = ConsultaView(self.usuario)
        self.consulta_view.show()

    def abrir_alteracao(self):
        self.alteracao_view = AlteracaoView(self.usuario, self.controller)
        self.alteracao_view.show()

    def abrir_cadastro(self):
        self.cadastro_view = CadastroFuncionarioView(self.usuario, self.controller)
        self.cadastro_view.show()

    def abrir_relatorios(self):
        relatorios_controller = RelatoriosController(self.usuario)
        self.relatorios_view = RelatoriosView(self.usuario, relatorios_controller)
        self.relatorios_view.show()
