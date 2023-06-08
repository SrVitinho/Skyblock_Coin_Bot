from datetime import datetime
from pymongo import MongoClient


class BasicItem:
    idcounter = 0

    def __init__(self, dada_raw, name, database):
        self.db = database
        summary = dada_raw['products'][name]['buy_summary']
        self.id = BasicItem.idcounter
        self.id_name = dada_raw['products'][name]['product_id']
        #  self.price = []
        #  self.time = []
        BasicItem.idcounter += 1
        if type(summary) is list:  # Caso nao possua muitas ofertas de compra não será lista
            self.name = name
            self.price = (dada_raw['products'][name]['buy_summary'][0]['pricePerUnit'])
            self.time = (datetime.now().strftime("%H:%M:%S"))
            self.order = dada_raw['products'][name]['buy_summary'][0]['orders']
            self.amount = dada_raw['products'][name]['buy_summary'][0]['amount']
        else:
            self.name = name
            self.price = (['products'][name]['buy_summary']['pricePerUnit'])
            self.time = (datetime.now().strftime("%H:%M:%S"))
            self.order = dada_raw['products'][name]['buy_summary']['orders']
            self.amount = dada_raw['products'][name]['buy_summary']['amount']

        self.Basic_Json = {
            "name": self.name,
            "price": self.price,
            "time": self.time,
            "order": self.order,
            "amount": self.amount,
            "price_history": [],
            "time_history": []
        }

        self.db.collection.insert_one(self.Basic_Json)

    def update_price(self):
        query = {"name": self.name}
        update = {"$push": {"price_history": self.price}}
        self.db.collection.update_one(query, update)
        update = {"$push": {"time_history": self.time}}
        self.db.collection.update_one(query, update)

    def get_prices(self):
        y_raw = self.db.collection.find_one({'name': self.name})
        x_raw = self.db.collection.find_one({'name': self.name})
        x = x_raw['price_history']
        y = y_raw['time_history']
        return x, y
