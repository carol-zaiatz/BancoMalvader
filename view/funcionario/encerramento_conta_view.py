# view/funcionario/encerramento_conta_view.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox
)
from controller.encerramento_conta_controller import EncerramentoContaController

class EncerramentoContaView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controller = EncerramentoContaController(usuario)

        self.setWindowTitle(f"Encerramento de Conta - {usuario.nome}")
        self.setGeometry(150, 150, 400, 350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Selecione a conta para encerramento:"))

        self.lista_contas = QListWidget()
        layout.addWidget(self.lista_contas)

        self.btn_encerrar = QPushButton("Encerrar Conta Selecionada")
        layout.addWidget(self.btn_encerrar)

        self.setLayout(layout)

        self.btn_encerrar.clicked.connect(self.encerrar_conta)

        self.carregar_contas()

    def carregar_contas(self):
        try:
            contas = self.controller.get_contas_ativas()
            self.lista_contas.clear()
            if contas:
                for conta in contas:
                    texto = f"Número: {conta['numero_conta']} | Tipo: {conta['tipo_conta']} | Saldo: R$ {conta['saldo']:.2f}"
                    item = QListWidgetItem(texto)
                    # Guardar id da conta no item para referência
                    item.setData(1000, conta['id_conta'])
                    self.lista_contas.addItem(item)
            else:
                self.lista_contas.addItem("Nenhuma conta ativa encontrada.")
                self.btn_encerrar.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar contas: {str(e)}")

    def encerrar_conta(self):
        item_selecionado = self.lista_contas.currentItem()
        if not item_selecionado or self.lista_contas.count() == 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma conta para encerrar.")
            return

        id_conta = item_selecionado.data(1000)
        if id_conta is None:
            QMessageBox.warning(self, "Aviso", "Conta inválida selecionada.")
            return

        confirm = QMessageBox.question(
            self, "Confirmação",
            "Tem certeza que deseja encerrar esta conta? Essa ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            sucesso, msg = self.controller.encerrar_conta(id_conta)
            if sucesso:
                QMessageBox.information(self, "Sucesso", msg)
                self.carregar_contas()
            else:
                QMessageBox.warning(self, "Falha", msg)
