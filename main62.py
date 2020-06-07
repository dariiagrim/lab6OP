import pickle

class Client:
    def __init__(self, name, birth_date, id_number, mobile):
        self.name = name
        self.birth_date = birth_date
        self.id_number = id_number
        self.mobile = mobile
        self.tickets = []

class TicketOffice:
    def __init__(self):
        self.base: Base
        self.cash = 0


    #buy a ticket
    #return a ticket

class Base:
    #List of available tickets
    #List of reserved tickets
    #List of clients
    pass

class Ticket:
    def __init__(self, start, finish, date, time, car_class, price):
        self.start = start
        self.finish = finish
        self.date = date
        self.time = time
        self.car_class = car_class
        self.price = price
        self.status = "available"


with open('tickets.pickle', 'rb') as f:
    tickets = pickle.load(f)

print(tickets["Kyiv"]["Kharkiv"][0].price)
