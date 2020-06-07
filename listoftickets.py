from main62 import Ticket
import random
import pickle

cities = ["Kyiv", "Kharkiv", "Odessa", "Dnipro", "Donetsk", "Zaporizhia", "Lviv", "Kryvyi Rih",
          "Mykolaiv", "Vinnytsia", "Kherson", "Poltava", "Chernihiv", "Cherkasy", "Khmelnytskyi",
          "Chernivtsi", "Zhytomyr", "Sumy", "Rivne", "Ternopyl", "Khrementchuk", "Lutsk"]

classes = ["S1", "S2", "S3"]
city_dict = {}
for city in cities:
    double_dict = {}
    for city1 in cities:
        if city != city1:
            double_dict[city1] = []
    city_dict[city] = double_dict


for i in range(10000):
    start = random.choice(cities)
    finish = random.choice([x for x in cities if x != start])
    num = str(random.randint(1, 30)).zfill(2)
    month = str(random.randint(6, 12)).zfill(2)
    date = f"{num}/{month}/2020"
    hours = str(random.randint(0, 23)).zfill(2)
    minutes = str(random.randint(0, 59)).zfill(2)
    time = f"{hours}:{minutes}"
    car_class = random.choice(classes)
    if car_class == "S1":
        price = random.randint(1201, 1700)
    elif car_class == "S2":
        price = random.randint(801, 1200)
    else:
        price = random.randint(300, 800)
    ticket = Ticket(start, finish, date, time, car_class, price)
    city_dict[ticket.start][ticket.finish].append(ticket)

with open("tickets.pickle", "wb") as f:
    pickle.dump(city_dict, f)

