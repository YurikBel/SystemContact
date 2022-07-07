import psycopg2
from contact import *


class DataBase:

    def fill_contacts(self):
        conn = psycopg2.connect(dbname='System_contact', user='postgres',
                                password='karoq838', host='localhost')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        records = cursor.fetchall()
        arr = []
        for k in records:
            Id, name, surname = k
            cursor.execute(f'SELECT * FROM phones WHERE contact_id = {Id}')
            phones = cursor.fetchall()
            contact = Contact(name, surname)
            for phone in phones:
                temp = Phone(phone[1])
                temp.note = phone[2]
                contact.phones.append(temp)

            contact.Id = Id
            arr.append(contact)
        cursor.close()
        conn.close()
        return arr

    def new_contact(self, contact):
        conn = psycopg2.connect(dbname='System_contact', user='postgres',
                                password='karoq838', host='localhost')
        Id = int(contact.Id)
        name = contact.name
        surname = contact.surname
        phones = contact.phones
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO contacts (id, name, surname) VALUES ({Id}, '{name}', '{surname}')"
        )
        for k in phones:
            cursor.execute(
                f"INSERT INTO phones (number, note, contact_id) VALUES ('{k.number}', '{None}', '{Id}')"
            )
        conn.commit()
        conn.close()

    def delete(self, contact):
        conn = psycopg2.connect(dbname='System_contact', user='postgres',
                                password='karoq838', host='localhost')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM phones WHERE contact_id = {contact.Id}")
        cursor.execute(f"DELETE FROM contacts WHERE Id = {contact.Id}")
        conn.commit()
        conn.close()

    def edit_contact(self, contact):
        self.delete(contact)
        self.new_contact(contact)

    def add_number(self, contact, phone):
        conn = psycopg2.connect(dbname='System_contact', user='postgres',
                                password='karoq838', host='localhost')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO phones (number, note, contact_id) VALUES ('{phone.number}', '{phone.note}',"
                       f" '{contact.Id}')")
        conn.commit()
        conn.close()

    def delete_number(self, phone):
        conn = psycopg2.connect(dbname='System_contact', user='postgres',
                                password='karoq838', host='localhost')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM phones WHERE number = {phone.number}")
        conn.commit()
        conn.close()



