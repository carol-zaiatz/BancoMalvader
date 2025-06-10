from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, 
                             QPushButton, QFormLayout, QMessageBox, QDateEdit, QDoubleSpinBox)
from PyQt5.QtCore import QDate
from controller.conta_controller import salvar_nova_conta # Importaremos o controller

class AberturaContaView(QWidget):
    def __init__(self, usuario_logado):
        super().__init__()
        self.usuario_logado = usuario_logado
        self.setWindowTitle("Banco Malvader - Abertura de Conta")
        self.setGeometry(150, 150, 450, 550)
        
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # --- Campos Comuns  ---
        self.tipo_conta_combo = QComboBox()
        self.tipo_conta_combo.addItems(["POUPANCA", "CORRENTE", "INVESTIMENTO"])
        self.nome_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.cpf_input.setInputMask('999.999.999-99')
        self.data_nasc_input = QDateEdit(QDate.currentDate())
        self.data_nasc_input.setDisplayFormat("yyyy-MM-dd")
        self.telefone_input = QLineEdit()
        self.telefone_input.setInputMask('(99) 99999-9999')
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        
        # --- Endereço ---
        self.cep_input = QLineEdit()
        self.cep_input.setInputMask('99999-999')
        self.local_input = QLineEdit()
        self.numero_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.estado_input = QLineEdit()
        self.estado_input.setMaxLength(2)

        self.form_layout.addRow(QLabel("Tipo de Conta:"), self.tipo_conta_combo)
        self.form_layout.addRow(QLabel("Nome Completo:"), self.nome_input)
        self.form_layout.addRow(QLabel("CPF:"), self.cpf_input)
        self.form_layout.addRow(QLabel("Data de Nascimento:"), self.data_nasc_input)
        self.form_layout.addRow(QLabel("Telefone:"), self.telefone_input)
        self.form_layout.addRow(QLabel("Senha Provisória:"), self.senha_input)
        self.form_layout.addRow(QLabel("--- Endereço ---"))
        self.form_layout.addRow(QLabel("CEP:"), self.cep_input)
        self.form_layout.addRow(QLabel("Logradouro:"), self.local_input)
        self.form_layout.addRow(QLabel("Número:"), self.numero_input)
        self.form_layout.addRow(QLabel("Bairro:"), self.bairro_input)
        self.form_layout.addRow(QLabel("Cidade:"), self.cidade_input)
        self.form_layout.addRow(QLabel("Estado (UF):"), self.estado_input)

        # --- Campos Específicos ---
        self.setup_campos_especificos()

        self.layout.addLayout(self.form_layout)

        self.salvar_btn = QPushButton("Abrir Conta")
        self.layout.addWidget(self.salvar_btn)
        
        self.setLayout(self.layout)

        # --- Conexões (Sinais e Slots) ---
        self.tipo_conta_combo.currentIndexChanged.connect(self.atualizar_campos_especificos)
        self.salvar_btn.clicked.connect(self.coletar_e_salvar_dados)
        self.atualizar_campos_especificos() # Chamar uma vez para configurar a tela inicial

    def setup_campos_especificos(self):
        """Cria os widgets para os campos específicos de cada conta."""
        # Campos Conta Corrente 
        self.limite_label = QLabel("Limite (R$):")
        self.limite_input = QDoubleSpinBox()
        self.limite_input.setRange(0, 100000)
        self.vencimento_label = QLabel("Data de Vencimento:")
        self.vencimento_input = QDateEdit(QDate.currentDate().addMonths(1))
        self.vencimento_input.setDisplayFormat("yyyy-MM-dd")
        self.taxa_manut_label = QLabel("Taxa de Manutenção (R$):")
        self.taxa_manut_input = QDoubleSpinBox()
        
        # Campos Conta Poupança 
        self.taxa_rend_label = QLabel("Taxa de Rendimento (%):")
        self.taxa_rend_input = QDoubleSpinBox()
        self.taxa_rend_input.setDecimals(2)

        # Campos Conta Investimento 
        self.perfil_risco_label = QLabel("Perfil de Risco:")
        self.perfil_risco_combo = QComboBox()
        self.perfil_risco_combo.addItems(["BAIXO", "MEDIO", "ALTO"])
        self.valor_min_label = QLabel("Valor Mínimo Invest. (R$):")
        self.valor_min_input = QDoubleSpinBox()
        self.taxa_rend_base_label = QLabel("Taxa Rend. Base (%):")
        self.taxa_rend_base_input = QDoubleSpinBox()
        
        # Adiciona ao layout mas oculta
        self.form_layout.addRow(self.limite_label, self.limite_input)
        self.form_layout.addRow(self.vencimento_label, self.vencimento_input)
        self.form_layout.addRow(self.taxa_manut_label, self.taxa_manut_input)
        self.form_layout.addRow(self.taxa_rend_label, self.taxa_rend_input)
        self.form_layout.addRow(self.perfil_risco_label, self.perfil_risco_combo)
        self.form_layout.addRow(self.valor_min_label, self.valor_min_input)
        self.form_layout.addRow(self.taxa_rend_base_label, self.taxa_rend_base_input)
        

    def atualizar_campos_especificos(self):
        """Mostra/oculta os campos com base no tipo de conta selecionado."""
        tipo = self.tipo_conta_combo.currentText()
        
        # Oculta todos primeiro
        for widget in [self.limite_label, self.limite_input, self.vencimento_label, self.vencimento_input, 
                       self.taxa_manut_label, self.taxa_manut_input, self.taxa_rend_label, self.taxa_rend_input, 
                       self.perfil_risco_label, self.perfil_risco_combo, self.valor_min_label, self.valor_min_input,
                       self.taxa_rend_base_label, self.taxa_rend_base_input]:
            widget.setVisible(False)

        # Mostra os campos relevantes
        if tipo == 'CORRENTE':
            for widget in [self.limite_label, self.limite_input, self.vencimento_label, self.vencimento_input, self.taxa_manut_label, self.taxa_manut_input]:
                widget.setVisible(True)
        elif tipo == 'POUPANCA':
            for widget in [self.taxa_rend_label, self.taxa_rend_input]:
                widget.setVisible(True)
        elif tipo == 'INVESTIMENTO':
            for widget in [self.perfil_risco_label, self.perfil_risco_combo, self.valor_min_label, self.valor_min_input, self.taxa_rend_base_label, self.taxa_rend_base_input]:
                widget.setVisible(True)

    def coletar_e_salvar_dados(self):
        """Coleta os dados do formulário e envia para o controller."""
        # Coleta dados comuns
        dados = {
            "tipo_conta": self.tipo_conta_combo.currentText(),
            "nome": self.nome_input.text(),
            "cpf": self.cpf_input.text().replace('.', '').replace('-', ''),
            "data_nascimento": self.data_nasc_input.text(),
            "telefone": self.telefone_input.text(),
            "senha": self.senha_input.text(),
            "cep": self.cep_input.text(),
            "local": self.local_input.text(),
            "numero_casa": self.numero_input.text(),
            "bairro": self.bairro_input.text(),
            "cidade": self.cidade_input.text(),
            "estado": self.estado_input.text().upper()
        }

        # Coleta dados específicos
        tipo_conta = dados["tipo_conta"]
        if tipo_conta == 'POUPANCA':
            dados["taxa_rendimento"] = self.taxa_rend_input.value()
        elif tipo_conta == 'CORRENTE':
            dados["limite"] = self.limite_input.value()
            dados["data_vencimento"] = self.vencimento_input.text()
            dados["taxa_manutencao"] = self.taxa_manut_input.value()
        elif tipo_conta == 'INVESTIMENTO':
            dados["perfil_risco"] = self.perfil_risco_combo.currentText()
            dados["valor_minimo"] = self.valor_min_input.value()
            dados["taxa_rendimento_base"] = self.taxa_rend_base_input.value()
            
        # Envia para o controller
        mensagem, sucesso = salvar_nova_conta(dados)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.close() # Fecha a janela após o sucesso
        else:
            QMessageBox.warning(self, "Erro", mensagem)