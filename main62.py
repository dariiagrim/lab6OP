import pickle
import random
from listoftickets import cities

class Client:
    def __init__(self, name, birth_date, id_number, mobile):
        self.name = name
        self.birth_date = birth_date
        self.id_number = id_number
        self.mobile = mobile
        self.tickets = []

    def __str__(self):
        return f"{self.name}, {self.birth_date}, {self.id_number}, {self.mobile}"

class TicketOffice:
    def __init__(self):
        self.base = Base()



    @staticmethod
    def ask_info():
        name = input("Name and last name: ")
        birth_date = input("Date of birth(00/00/0000): ")
        id_number = input("Id(12 numbers): ")
        mobile = input("Telephone(10 numbers): ")
        return name, birth_date, id_number, mobile

    def ask_needs(self):
        buy = int(input("What do you want to do? (0 - return a ticket , 1 - buy a ticket): "))
        if buy:
            start = input("From: ")
            finish = input("To: ")
            date = input("When(00/00/0000): ")
            if start not in cities or finish not in cities:
                print("Sorry, our office doesn't work with this destination.")
                try_again = int(input("Can we help you with anything else?(1 - yes) "))
                if try_again:
                    self.ask_needs()
                else:
                    return
            wish_type = input("Preferable class(S1, S2, S3): ")
            apr_tickets = []
            for ticket in self.base.a_tickets[start][finish]:
                if ticket.available and ticket.date == date and ticket.car_class == wish_type:
                    apr_tickets.append(ticket)
                    ticket.available = False
            for ticket in self.base.a_tickets[start][finish]:
                if ticket.available and ticket.date == date and ticket.car_class != wish_type:
                    apr_tickets.append(ticket)
                    ticket.available = False
            if not apr_tickets:
                try_again = int(input("No tickets are available on this date. Wanna try the other one?(1 - yes) "))
                if try_again:
                    self.ask_needs()
            else:
                for i in range(len(apr_tickets)):
                    print(f"{i+1}. {apr_tickets[i]}")
                index = int(input("Choose your ticket(0, if nothing is OK): ")) - 1
                if index == -1:
                    for ticket in self.base.a_tickets[start][finish]:
                        if ticket in apr_tickets:
                            ticket.available = True
                    try_again = int(input("Can we help you with anything else?(1 - yes) "))
                    if try_again:
                        self.ask_needs()
                else:
                    was_before = int(input("Have you ever bought ticket through our office? (1 - yes) "))
                    if was_before:
                        name = input("Name and last name: ")
                        for cl in self.base.clients:
                            if cl.name == name:
                                client = cl
                    else:
                        name, birth_date, id_number, mobile = self.ask_info()
                        client = Client(name, birth_date, id_number, mobile)
                    tick = apr_tickets[index]
                    for ticket in self.base.a_tickets[start][finish]:
                        if ticket in apr_tickets and ticket != tick:
                            ticket.available = True
                    client.tickets.append(tick)
                    if not was_before:
                        self.base.clients.append(client)
                    tick.available = False
                    self.base.reserved.append(tick)
                    self.base.cash += tick.price
                    with open('cash.pickle', 'wb') as f:
                        pickle.dump(self.base.cash, f)
                    tick.id = random.randint(1, 10000)
                    with open('client.pickle', 'wb') as f:
                        pickle.dump(self.base.clients, f)
                    with open('reserved.pickle', 'wb') as f:
                        pickle.dump(self.base.reserved, f)
                    with open('tickets.pickle', 'wb') as f:
                        pickle.dump(self.base.a_tickets, f)
                    try_again = int(input("Can we help you with anything else?(1 - yes) "))
                    if try_again:
                        self.ask_needs()
                    else:
                        return
        else:
            name = input("Name and last name: ")
            client = None
            for cl in self.base.clients:
                if cl.name == name:
                    client = cl
                    break
            if client is None:
                try_again = int(input("Sorry, you are not in our base. Do you want to try again?(1 - yes) "))
                if try_again:
                    self.ask_needs()
                else:
                    return
            if not client.tickets:
                try_again = int(input("You have no tickets. Can we help you with smth else?(1 - yes) "))
                if try_again:
                    self.ask_needs()
                else:
                    return
            date = input("Current date(00/00/0000): ")
            day = int(date[0:2])
            month = int(date[3:5])
            for ticket in client.tickets:
                print(ticket, "id:", ticket.id)
            tick_id = input("Enter id: ")
            for ticket in client.tickets:
                if ticket.id == int(tick_id):
                    tick = ticket
                    break
            day1 = int(tick.date[0:2])
            month1 = int(tick.date[3:5])
            if month == month1:
                dif = day1 - day
            elif month1 - month == 1:
                dif = day1 - day + 30
            else:
                dif = 30
            client.tickets.remove(tick)
            self.base.reserved = [x for x in self.base.reserved if x.id != tick.id]
            percent = count_percent(dif)
            self.base.cash -= tick.price - tick.price*percent
            self.base.returned.append(tick)
            with open('returned.pickle', 'wb') as f:
                pickle.dump(self.base.returned, f)
            with open('client.pickle', 'wb') as f:
                pickle.dump(self.base.clients, f)
            with open('reserved.pickle', 'wb') as f:
                pickle.dump(self.base.reserved, f)
            with open('cash.pickle', 'wb') as f:
                pickle.dump(self.base.cash, f)
            for ticket in self.base.a_tickets[tick.start][tick.finish]:
                if ticket.id == int(tick_id):
                    ticket.available = True
            with open('tickets.pickle', 'wb') as f:
                pickle.dump(self.base.a_tickets, f)
            tick.available = True
            try_again = int(input("Can we help you with anything else?(1 - yes) "))
            if try_again:
                self.ask_needs()
            else:
                return

            def try_again(self):
                pass



class Base:
    def __init__(self):
        self.a_tickets = None
        self.clients = None
        self.returned = None
        self.reserved = None
        self.cash = None
        self.create_lists()

    def create_lists(self):
        with open('tickets.pickle', 'rb') as f:
            self.a_tickets = pickle.load(f)
        with open('client.pickle', 'rb') as f:
            self.clients = pickle.load(f)
        with open('reserved.pickle', 'rb') as f:
            self.reserved = pickle.load(f)
        with open('returned.pickle', 'rb') as f:
            self.returned = pickle.load(f)
        with open('cash.pickle', 'rb') as f:
            self.cash = pickle.load(f)


class Ticket:
    def __init__(self, start, finish, date, time, car_class, price):
        self.start = start
        self.finish = finish
        self.date = date
        self.time = time
        self.car_class = car_class
        self.price = price
        self.available = True
        self.id = None

    def __str__(self):
        return f"{self.start}->{self.finish}, {self.date}, {self.time}, {self.car_class}, {self.price}"


def rewrite_data():
    data = []
    cash = 0
    with open('cash.pickle', 'wb') as f:
        pickle.dump(cash, f)
    with open('client.pickle', 'wb') as f:
        pickle.dump(data, f)
    with open('reserved.pickle', 'wb') as f:
        pickle.dump(data, f)
    with open('returned.pickle', 'wb') as f:
        pickle.dump(data, f)

def count_percent(dif):
    if dif >= 30:
        return 0.01
    if dif  >= 15:
        return 0.05
    if dif >= 3:
        return 0.1
    else:
        return 0.3

if __name__ == "__main__":




    office = TicketOffice()
    print(office.base.cash)
    for client1 in office.base.clients:
        print(client1)
    for ticket in office.base.reserved:
        print(ticket)
    for ticket in office.base.returned:
        print("*", ticket)

    office.ask_needs()
    print(office.base.cash)

