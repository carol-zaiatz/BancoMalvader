# view/funcionario/consulta_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox
from controller.consulta_controller import ConsultaController

class ConsultaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controller = ConsultaController(usuario)

        self.setWindowTitle(f"Consulta de Dados - {usuario.nome}")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()

        # Labels para mostrar os dados do usuário
        self.label_nome = QLabel()
        self.label_cpf = QLabel()
        self.label_telefone = QLabel()
        self.label_tipo = QLabel()

        layout.addWidget(self.label_nome)
        layout.addWidget(self.label_cpf)
        layout.addWidget(self.label_telefone)
        layout.addWidget(self.label_tipo)

        layout.addWidget(QLabel("Contas ativas:"))

        # Lista para mostrar as contas do usuário
        self.lista_contas = QListWidget()
        layout.addWidget(self.lista_contas)

        self.setLayout(layout)

        # Carregar os dados ao abrir a janela
        self.carregar_dados()

    def carregar_dados(self):
        try:
            dados = self.controller.get_dados_usuario()
            if dados:
                self.label_nome.setText(f"Nome: {dados['nome']}")
                self.label_cpf.setText(f"CPF: {dados['cpf']}")
                self.label_telefone.setText(f"Telefone: {dados['telefone']}")
                self.label_tipo.setText(f"Tipo de Usuário: {dados['tipo_usuario']}")
            else:
                QMessageBox.warning(self, "Aviso", "Dados do usuário não encontrados.")

            contas = self.controller.get_contas()
            self.lista_contas.clear()
            if contas:
                for conta in contas:
                    texto = f"Número: {conta['numero_conta']} | Tipo: {conta['tipo_conta']} | Saldo: R$ {conta['saldo']:.2f} | Status: {conta['status']}"
                    item = QListWidgetItem(texto)
                    self.lista_contas.addItem(item)
            else:
                self.lista_contas.addItem("Nenhuma conta ativa encontrada.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados: {str(e)}")
