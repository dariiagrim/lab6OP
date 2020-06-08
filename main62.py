import pickle
import random

cities = ["Kyiv", "Kharkiv", "Odessa", "Dnipro", "Donetsk", "Zaporizhia", "Lviv", "Kryvyi Rih",
          "Mykolaiv", "Vinnytsia", "Kherson", "Poltava", "Chernihiv", "Cherkasy", "Khmelnytskyi",
          "Chernivtsi", "Zhytomyr", "Sumy", "Rivne", "Ternopyl", "Khrementchuk", "Lutsk"]


class Client:
    def __init__(self, name, birth_date, id_number, mobile):
        self.name = name
        self.birth_date = birth_date
        self.id_number = id_number
        self.mobile = mobile
        self.tickets = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._name = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._birth_date = value

    @property
    def id_number(self):
        return self._id_number

    @id_number.setter
    def id_number(self, value):
        if not isinstance(value, str):
            raise ValueError
        if len(value) != 12 or not value.isnumeric():
            raise ValueError
        self._id_number = value

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        if not isinstance(value, str):
            raise ValueError
        if len(value) != 10 or not value.isnumeric():
            raise ValueError
        self._mobile = value

    def __str__(self):
        return f"{self.name}, {self.birth_date}, {self.id_number}, {self.mobile}"


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

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._start = value

    @property
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._finish = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._date = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._time = value

    @property
    def car_class(self):
        return self._car_class

    @car_class.setter
    def car_class(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._car_class = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            raise ValueError
        self._price = value

    def __str__(self):
        return f"{self.start}->{self.finish}, {self.date}, {self.time}, {self.car_class}, {self.price}"


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

    @staticmethod
    def count_difference(day, day1, month, month1):
        if month == month1:
            dif = day1 - day
        elif month1 - month == 1:
            dif = day1 - day + 30
        else:
            dif = 30
        return dif

    @staticmethod
    def count_percent(dif):
        if dif >= 30:
            return 0.01
        if dif >= 15:
            return 0.05
        if dif >= 3:
            return 0.1
        else:
            return 0.3

    def try_again(self):
        again = int(input("Can we help you with anything else?(1 - yes) "))
        if again:
            self.ask_needs()
        else:
            print("Cash: ", round(self.base.cash, 3))
            print("Thanks for using our services. Have a nice day!")
            exit()

    def purchase_info(self):
        start = input("From: ")
        finish = input("To: ")
        date = input("When(00/00/0000): ")
        if start not in cities or finish not in cities:
            print("Sorry, our office doesn't work with this destination.")
            self.try_again()
        wish_type = input("Preferable class(S1, S2, S3): ")
        return start, finish, date, wish_type

    def appropriate_tickets(self, start, finish, date, wish_type):
        apr_tickets = []
        for ticket in self.base.a_tickets[start][finish]:
            if ticket.available and ticket.date == date and ticket.car_class == wish_type:
                apr_tickets.append(ticket)
                ticket.available = False
        for ticket in self.base.a_tickets[start][finish]:
            if ticket.available and ticket.date == date and ticket.car_class != wish_type:
                apr_tickets.append(ticket)
                ticket.available = False
        return apr_tickets

    @staticmethod
    def print_options(apr_tickets):
        for i in range(len(apr_tickets)):
            print(f"{i + 1}. {apr_tickets[i]}")
        index = int(input("Choose your ticket(0, if nothing is OK): ")) - 1
        return index

    def if_nothing_is_ok(self, start, finish, apr_tickets):
        for ticket in self.base.a_tickets[start][finish]:
            if ticket in apr_tickets:
                ticket.available = True
        self.try_again()

    def return_client(self, was_before_l):
        was_before_l[0] = int(input("Have you ever bought ticket through our office? (1 - yes) "))
        client_r = None
        if was_before_l[0]:
            name = input("Name and last name: ")
            for cl in self.base.clients:
                if cl.name == name:
                    client_r = cl
        else:
            name, birth_date, id_number, mobile = self.ask_info()
            try:
                client_r = Client(name, birth_date, id_number, mobile)
            except ValueError:
                print("Not correct data.")
                self.try_again()

        if client_r is None:
            print("You are not in our base.")
            self.try_again()
        return client_r

    def restore_availability(self, tick, apr_tickets, start, finish):
        for ticket in self.base.a_tickets[start][finish]:
            if ticket in apr_tickets and ticket != tick:
                ticket.available = True

    def pickling(self):
        with open('cash.pickle', 'wb') as f:
            pickle.dump(self.base.cash, f)
        with open('client.pickle', 'wb') as f:
            pickle.dump(self.base.clients, f)
        with open('reserved.pickle', 'wb') as f:
            pickle.dump(self.base.reserved, f)
        with open('tickets.pickle', 'wb') as f:
            pickle.dump(self.base.a_tickets, f)

    def find_client(self, clients):
        name = input("Name and last name: ")
        for cl in self.base.clients:
            if cl.name == name:
                clients[0] = cl
                break
        if clients[0] is None:
            print("You are not in our base.")
            self.try_again()
        if not clients[0].tickets:
            print("No tickets to return")
            self.try_again()

    def choose_ticket_to_return(self, client: Client):
        for ticket in client.tickets:
            print(ticket, "id:", ticket.id)
        tick_id = input("Enter id: ")
        tick1 = None
        for ticket in client.tickets:
            if ticket.id == int(tick_id):
                tick1 = ticket
                break
        if tick1 is None:
            self.try_again()
        return tick1

    @staticmethod
    def deal_with_date(tick):
        date = input("Current date(00/00/0000): ")
        day = int(date[0:2])
        month = int(date[3:5])
        day1 = int(tick.date[0:2])
        month1 = int(tick.date[3:5])
        return day, month, day1, month1

    def pickling2(self):
        with open('returned.pickle', 'wb') as f:
            pickle.dump(self.base.returned, f)
        with open('client.pickle', 'wb') as f:
            pickle.dump(self.base.clients, f)
        with open('reserved.pickle', 'wb') as f:
            pickle.dump(self.base.reserved, f)
        with open('cash.pickle', 'wb') as f:
            pickle.dump(self.base.cash, f)

    def restore_availability2(self, tick: Ticket):
        for ticket in self.base.a_tickets[tick.start][tick.finish]:
            if ticket.id == int(tick.id):
                ticket.available = True
        with open('tickets.pickle', 'wb') as f:
            pickle.dump(self.base.a_tickets, f)
        tick.available = True

    def ask_needs(self):
        buy = int(input("What do you want to do? (0 - return a ticket , 1 - buy a ticket, 2 - exit): "))
        if buy == 2:
            print("Cash: ", round(self.base.cash, 3))
            exit()
        if buy:
            start, finish, date, wish_type = self.purchase_info()
            apr_tickets = self.appropriate_tickets(start, finish, date, wish_type)
            if not apr_tickets:
                print("No tickets is available.")
                self.try_again()
            else:
                index = self.print_options(apr_tickets)
                if index == -1:
                    self.if_nothing_is_ok(start, finish, apr_tickets)
                else:
                    was_before_l = [0]
                    client = self.return_client(was_before_l)
                    was_before = was_before_l[0]
                    tick = apr_tickets[index]
                    self.restore_availability(tick, apr_tickets, start, finish)
                    client.tickets.append(tick)
                    if not was_before:
                        self.base.clients.append(client)
                    tick.available = False
                    self.base.reserved.append(tick)
                    self.base.cash += tick.price
                    tick.id = random.randint(1, 10000)
                    self.pickling()
                    self.try_again()
        else:
            clients = [None]
            self.find_client(clients)
            client = clients[0]
            tick = self.choose_ticket_to_return(client)
            day, month, day1, month1 = self.deal_with_date(tick)
            dif = self.count_difference(day, day1, month, month1)
            client.tickets.remove(tick)
            percent = self.count_percent(dif)
            self.base.reserved = [x for x in self.base.reserved if x.id != tick.id]
            self.base.cash -= tick.price - tick.price*percent
            self.base.returned.append(tick)
            self.pickling2()
            self.restore_availability2(tick)
            self.try_again()


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


if __name__ == "__main__":
    office = TicketOffice()
    print("Cash:", round(office.base.cash, 3))
    for client1 in office.base.clients:
        print(client1)
    for ticket1 in office.base.reserved:
        print(ticket1)
    for ticket1 in office.base.returned:
        print("*", ticket1)

    office.ask_needs()




