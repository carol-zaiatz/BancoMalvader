# controller/login_controller.py
from dao.usuario_dao import (
    buscar_usuario_por_cpf,
    buscar_usuario_por_cpf_e_senha_e_otp,
    chamar_procedure_gerar_otp,
    limpar_otp
)
from view.cliente.cliente_view import ClienteView
from view.funcionario.funcionario_view import FuncionarioView
from hashlib import md5
from PyQt5.QtWidgets import QMessageBox

class LoginController:
    def __init__(self, view):
        self.view = view

    def autenticar(self, cpf, senha, otp):
        if not cpf or not senha or not otp:
            QMessageBox.warning(self.view, "Erro", "Preencha CPF, senha e OTP para entrar.")
            return

        senha_hash = md5(senha.encode()).hexdigest()
        usuario = buscar_usuario_por_cpf_e_senha_e_otp(cpf, senha_hash, otp)

        if usuario:
            if usuario.tipo_usuario != self.view.tipo_usuario:
                QMessageBox.warning(self.view, "Erro", f"Usuário não é do tipo '{self.view.tipo_usuario}' selecionado.")
                return

            QMessageBox.information(self.view, "Login", f"Bem-vindo, {usuario.nome}!")
            self.view.close()
            limpar_otp(usuario.id)

            if usuario.tipo_usuario == "CLIENTE":
                self.abrir_tela_cliente(usuario)
            else:
                self.abrir_tela_funcionario(usuario)
        else:
            QMessageBox.warning(self.view, "Erro", "CPF, senha ou OTP incorretos ou expirados.")

    def gerar_otp(self, cpf):
        if not cpf:
            QMessageBox.warning(self.view, "Erro", "Informe o CPF para gerar OTP.")
            return

        usuario = buscar_usuario_por_cpf(cpf)
        if usuario:
            otp = chamar_procedure_gerar_otp(usuario.id)
            if otp:
                QMessageBox.information(self.view, "OTP Gerado", f"OTP: {otp} (válido por 5 minutos)")
            else:
                QMessageBox.warning(self.view, "Erro", "Não foi possível gerar OTP. Tente novamente.")
        else:
            QMessageBox.warning(self.view, "Erro", "Usuário não encontrado com este CPF.")

    def abrir_tela_cliente(self, usuario):
        self.cliente_view = ClienteView(usuario)
        self.cliente_view.show()

    def abrir_tela_funcionario(self, usuario):
        self.funcionario_view = FuncionarioView(usuario)
        self.funcionario_view.show()
