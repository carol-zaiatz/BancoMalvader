# main.py
from PyQt5.QtWidgets import QApplication
from view.tipo_usuario_view import TipoUsuarioView
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TipoUsuarioView()
    window.show()
    sys.exit(app.exec_())
