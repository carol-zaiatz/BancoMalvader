from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QListWidget, QListWidgetItem, QMessageBox
from dao.consulta_dao import (
    obter_dados_usuario, obter_contas_usuario, 
    obter_score_credito, obter_projecao_rendimentos
)

class ConsultaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario

        self.setWindowTitle(f"Consulta de Dados - {usuario.nome}")
        self.setGeometry(150, 150, 500, 400)

        layout_principal = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tab_usuario = QWidget()
        self.tab_conta = QWidget()

        self.tabs.addTab(self.tab_usuario, "Usuário")
        self.tabs.addTab(self.tab_conta, "Contas")

        self.inicializar_tab_usuario()
        self.inicializar_tab_conta()

        layout_principal.addWidget(self.tabs)
        self.setLayout(layout_principal)

        self.carregar_dados_usuario()
        self.carregar_dados_contas()

    def inicializar_tab_usuario(self):
        layout = QVBoxLayout()
        self.label_nome = QLabel()
        self.label_cpf = QLabel()
        self.label_telefone = QLabel()
        self.label_tipo = QLabel()
        self.label_score = QLabel()

        layout.addWidget(self.label_nome)
        layout.addWidget(self.label_cpf)
        layout.addWidget(self.label_telefone)
        layout.addWidget(self.label_tipo)
        layout.addWidget(self.label_score)

        self.tab_usuario.setLayout(layout)

    def inicializar_tab_conta(self):
        layout = QVBoxLayout()
        self.lista_contas = QListWidget()
        layout.addWidget(self.lista_contas)
        self.tab_conta.setLayout(layout)

    def carregar_dados_usuario(self):
        try:
            dados = obter_dados_usuario(self.usuario.id_usuario)
            score = obter_score_credito(self.usuario.id_usuario)
            if dados:
                self.label_nome.setText(f"Nome: {dados['nome']}")
                self.label_cpf.setText(f"CPF: {dados['cpf']}")
                self.label_telefone.setText(f"Telefone: {dados['telefone']}")
                self.label_tipo.setText(f"Tipo de Usuário: {dados['tipo_usuario']}")
                self.label_score.setText(f"Score de Crédito: {score if score is not None else 'N/A'}")
                self.usuario.tipo_usuario = dados['tipo_usuario']  # salvar para uso na conta
            else:
                QMessageBox.warning(self, "Aviso", "Dados do usuário não encontrados.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados do usuário: {str(e)}")

    def carregar_dados_contas(self):
        try:
            tipo_usuario = getattr(self.usuario, 'tipo_usuario', None)
            contas = obter_contas_usuario(self.usuario.id_usuario, tipo_usuario)
            self.lista_contas.clear()
            if contas:
                for conta in contas:
                    rendimento = obter_projecao_rendimentos(conta['id_conta'])
                    texto = (
                        f"N°: {conta['numero_conta']} | Tipo: {conta['tipo_conta']} | "
                        f"Saldo: R$ {conta['saldo']:.2f} | Status: {conta['status']} | "
                        f"Rendimento Estimado: R$ {rendimento:.2f}"
                    )
                    self.lista_contas.addItem(QListWidgetItem(texto))
            else:
                self.lista_contas.addItem(QListWidgetItem("Nenhuma conta ativa encontrada."))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar contas: {str(e)}")
