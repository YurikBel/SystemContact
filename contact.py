class Contact:
    def __init__(self, name, surname):
        self.Id = None
        self.name = name
        self.surname = surname
        self.phones = []

    @property
    def fullname(self):
        return f'{self.surname} {self.name}'


class Phone:
    def __init__(self, number):
        self.number = number
        self.note = None