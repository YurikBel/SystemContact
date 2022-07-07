from UiNewContactWindow import Ui_Dialog
from contact import *
from PyQt5 import QtWidgets


class NewContactWindow(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, contact=None):
        super().__init__()
        self.setupUi(self)
        self.contact = None
        if contact is not None:
            self.contact = contact
            self.lineEditName.setText(contact.name)
            self.lineEditSurname.setText(contact.surname)

        self.buttonBox.accepted.connect(self.ok_click)

    def ok_click(self):
        if self.contact is None:
            self.contact = Contact(self.lineEditName.text(), self.lineEditSurname.text())
            self.contact.phones.append(Phone(self.lineEditNumber.text()))
        else:
            self.contact.surname = self.lineEditSurname.text()
            self.contact.name = self.lineEditName.text()
            self.contact.phones.append(Phone(self.lineEditNumber.text()))





