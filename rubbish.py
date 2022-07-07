from UiAddContactWindow import Ui_DialogAddNumber
from contact import *
from PyQt5 import QtWidgets


class AddNumberWindow(Ui_DialogAddNumber, QtWidgets.QDialog):
    def __init__(self, contact):
        super().__init__()
        self.setupUi(self)
        self.contact = contact

        self.buttonBox.accepted.connect(self.ok_click)

    def ok_click(self):
        phone = Phone(self.lineEdit.text())
        phone.note = self.textEdit.toPlainText()
        self.contact.phones.append(phone)