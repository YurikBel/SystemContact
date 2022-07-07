from UiAddContactWindow import Ui_DialogAddNumber
from contact import *
from PyQt5 import QtWidgets


class AddNumberWindow(Ui_DialogAddNumber, QtWidgets.QDialog):
    def __init__(self, other):
        super().__init__()
        self.setupUi(self)
        self.other = other
        if isinstance(self.other, Phone):
            self.lineEdit.setText(self.other.number)
            self.textEdit.setText(self.other.note)
        self.buttonBox.accepted.connect(self.ok_click)

    def ok_click(self):
        if isinstance(self.other, Contact):
            phone = Phone(self.lineEdit.text())
            phone.note = self.textEdit.toPlainText()
            self.other.phones.append(phone)
        else:
            self.other.number = self.lineEdit.text()
            self.other.note = self.textEdit.toPlainText()




