from UiMainWindow import Ui_MainWindow
import sys
from NewContactWindow import NewContactWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget
from AddContactNumberWindow import AddNumberWindow
from base import *


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionCreateContact.triggered.connect(self.create_contact_click)
        self.actionEditContact.triggered.connect(self.edit_contact_click)
        self.actionRemoveContact.triggered.connect(self.remove_contact_click)
        self.actionShowContacts.triggered.connect(self.show_contact_numbers)
        self.actionAppendNumber.triggered.connect(self.add_contact_number)
        self.actionEditNumber.triggered.connect(self.edit_number)
        self.actionDeleteNumber.triggered.connect(self.delete_number)
        self.listWidget.currentItemChanged.connect(self.show_contact_numbers)
        self.pushButtonSearch.clicked.connect(self.search_contact)
        self.pushButtonAll.clicked.connect(self.show_contacts)
        self.contacts = []

    def search_contact(self):
        name = self.lineSearchContact.text().strip()
        contacts = [c for c in self.contacts if c.name == name]
        self.listWidget.clear()
        if len(contacts) != 0:
            self.listWidget.addItems([f'{c.surname} {c.name}' for c in contacts])
        else:
            self.listWidget.addItem(f'Нет таких контактов')

    def create_contact_click(self):
        window = NewContactWindow()
        res = window.exec_()
        contact = window.contact
        contact.Id = max(k.Id for k in self.contacts) + 1
        if res == 1:
            self.contacts.append(contact)
            self.show_contacts()
            DataBase().new_contact(contact)

    def edit_contact_click(self):
        fullname = self.listWidget.currentItem().text()
        contact = next(c for c in self.contacts if c.fullname == fullname)
        if contact is not None:
            window = NewContactWindow(contact)
            contact = window.contact
            res = window.exec_()
            DataBase().edit_contact(contact)
            if res == 1:
                self.show_contacts()

    def show_contacts(self):
        self.listWidget.clear()
        self.listWidget.addItems([f'{c.surname} {c.name}' for c in self.contacts])

    def remove_contact_click(self):
        fullname = self.listWidget.currentItem().text()
        contact = next(c for c in self.contacts if c.fullname == fullname)
        self.contacts.remove(contact)
        self.show_contacts()
        DataBase().delete(contact)

    def show_contact_numbers(self, current, previous):
        if self.listWidget.currentItem() is not None:
            fullname = self.listWidget.currentItem().text()
            contact = next(c for c in self.contacts if c.fullname == fullname)
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(contact.phones))
            self.tableWidget.setHorizontalHeaderLabels(['Номер', 'Комментарий'])
            for i in range(len(contact.phones)):
                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(f'{contact.phones[i].number}'))
                if contact.phones[i].note is not None:
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(f'{contact.phones[i].note}'))
                else:
                    self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(f' '))

    def add_contact_number(self):
        fullname = self.listWidget.currentItem().text()
        contact = next(c for c in self.contacts if c.fullname == fullname)
        window = AddNumberWindow(contact)
        res = window.exec_()
        if res == 1:
            DataBase().add_number(contact, contact.phones[-1])
            self.show_contacts()

    def edit_number(self):
        c_number = self.tableWidget.currentItem().text()
        contact = next((s for s in self.contacts if c_number in [k.number for k in s.phones]), None)
        phone = next((s for s in contact.phones if s.number == c_number), None)
        window = AddNumberWindow(phone)
        res = window.exec_()
        if res == 1:
            self.show_contacts()

    def delete_number(self):
        c_number = self.tableWidget.currentItem().text()
        contact = next((s for s in self.contacts if c_number in [k.number for k in s.phones]), None)
        phone = next((s for s in contact.phones if s.number == c_number), None)
        contact.phones.remove(phone)
        DataBase().delete_number(phone)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    arr_contacts = DataBase().fill_contacts()
    for k in arr_contacts:
        window.contacts.append(k)
    window.show_contacts()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
