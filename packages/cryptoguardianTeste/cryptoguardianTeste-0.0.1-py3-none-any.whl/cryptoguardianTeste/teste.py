import sys
import random
import string
from cryptography.fernet import Fernet
from PyQt5 import QtCore, QtGui, QtWidgets

class CryptoGuardianEncrypt(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("CryptoGuardianEncrypt")
        self.resize(576, 419)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 130, 111, 41))
        self.pushButton.setObjectName("pushButton")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 30, 191, 41))
        self.label.setObjectName("label")
        
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 21))
        self.menubar.setObjectName("menubar")
        
        self.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.pushButton.clicked.connect(self.encrypt_file)
    
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("CryptoGuardianEncrypt", "CryptoGuardian - Encrypt"))
        self.pushButton.setText(_translate("CryptoGuardianEncrypt", "Criptografar"))
        self.label.setText(_translate("CryptoGuardianEncrypt", "<html><head/><body><p><span style=\" font-size:20pt;\">CryptoGuardian - Encrypt</span></p></body></html>"))
    
    def generate_random_password(self, length=16):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(caracteres) for _ in range(length))

    def encrypt_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Selecione um arquivo para criptografar", "", "Todos os arquivos (*)")
        if file_path:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)

            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = cipher_suite.encrypt(file_data)

            encrypted_file_path = file_path + '.encrypted'
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

            self.copy_password_to_clipboard(key)
            self.show_message(f'Arquivo criptografado: {encrypted_file_path}', "Senha de criptografia copiada para a área de transferência.")

    def copy_password_to_clipboard(self, password):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(password.decode())

    def show_message(self, message, password):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("CryptoGuardian")
        if password:
            msg.setInformativeText(password)
        msg.exec_()

class CryptoGuardianDecrypt(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("CryptoGuardianDecrypt")
        self.resize(576, 419)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 130, 111, 41))
        self.pushButton.setObjectName("pushButton")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 30, 191, 41))
        self.label.setObjectName("label")
        
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 21))
        self.menubar.setObjectName("menubar")
        
        self.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.pushButton.clicked.connect(self.decrypt_file)
    
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("CryptoGuardianDecrypt", "CryptoGuardian - Decrypt"))
        self.pushButton.setText(_translate("CryptoGuardianDecrypt", "Descriptografar"))
        self.label.setText(_translate("CryptoGuardianDecrypt", "<html><head/><body><p><span style=\" font-size:20pt;\">CryptoGuardian - Decrypt</span></p></body></html>"))
    
    def decrypt_file(self):
        encrypted_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Selecione um arquivo para descriptografar", "", "Encrypted Files (*.encrypted)")
        if encrypted_file_path:
            senha_usuario, ok = QtWidgets.QInputDialog.getText(None, "Senha", "Digite a senha de descriptografia:")
            if ok:
                key = senha_usuario.encode()

                cipher_suite = Fernet(key)

                with open(encrypted_file_path, 'rb') as encrypted_file:
                    encrypted_data = encrypted_file.read()

                decrypted_data = cipher_suite.decrypt(encrypted_data)

                decrypted_file_path = encrypted_file_path.replace('.encrypted', '.decrypted')
                with open(decrypted_file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

                self.show_message(f'Arquivo descriptografado: {decrypted_file_path}', "")

    def show_message(self, message, password):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("CryptoGuardian")
        if password:
            msg.setInformativeText(password)
        msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    encrypt_window = CryptoGuardianEncrypt()
    decrypt_window = CryptoGuardianDecrypt()
    
    encrypt_window.show()
    decrypt_window.show()
    
    sys.exit(app.exec_())
