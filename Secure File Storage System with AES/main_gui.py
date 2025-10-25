# main_gui.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from crypto_utils import encrypt_file, decrypt_file

class SecureFileStorageGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES Secure File Storage")
        self.setGeometry(300, 300, 500, 250)
        self.file_paths = []

        # Enable drag & drop
        self.setAcceptDrops(True)

        # Widgets
        self.label = QLabel("Drag & drop files here or use 'Browse Files'")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")

        self.file_button = QPushButton("Browse Files")
        self.file_button.clicked.connect(self.browse_files)

        self.password_label = QLabel("Enter password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.encrypt_button = QPushButton("Encrypt Files")
        self.encrypt_button.clicked.connect(self.encrypt_files_action)

        self.decrypt_button = QPushButton("Decrypt Files")
        self.decrypt_button.clicked.connect(self.decrypt_files_action)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        self.setLayout(layout)

    # Drag-and-drop events
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.file_paths = files
        display = ", ".join([os.path.basename(f) for f in files])
        self.label.setText(f"Selected Files: {display}")

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.file_paths = files
            display = ", ".join([os.path.basename(f) for f in files])
            self.label.setText(f"Selected Files: {display}")

    def encrypt_files_action(self):
        if not self.file_paths:
            QMessageBox.warning(self, "Error", "No files selected!")
            return
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Error", "Enter a password!")
            return
        success, fail = [], []
        for file in self.file_paths:
            try:
                encrypt_file(file, password)
                success.append(os.path.basename(file))
            except Exception as e:
                fail.append(f"{os.path.basename(file)}: {str(e)}")
        msg = f"Encrypted: {', '.join(success)}" if success else ""
        if fail:
            msg += f"\nFailed: {', '.join(fail)}"
        QMessageBox.information(self, "Encryption Result", msg)

    def decrypt_files_action(self):
        if not self.file_paths:
            QMessageBox.warning(self, "Error", "No files selected!")
            return
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Error", "Enter a password!")
            return
        success, fail = [], []
        for file in self.file_paths:
            try:
                file_to_decrypt = file
                if file_to_decrypt.endswith('.meta'):
                    file_to_decrypt = file_to_decrypt.replace('.meta', '')
                decrypt_file(file_to_decrypt, password)
                success.append(os.path.basename(file_to_decrypt))
            except Exception as e:
                fail.append(f"{os.path.basename(file)}: {str(e)}")
        msg = f"Decrypted: {', '.join(success)}" if success else ""
        if fail:
            msg += f"\nFailed: {', '.join(fail)}"
        QMessageBox.information(self, "Decryption Result", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecureFileStorageGUI()
    window.show()
    sys.exit(app.exec_())
