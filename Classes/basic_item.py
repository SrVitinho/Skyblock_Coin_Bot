from datetime import datetime
from pymongo import MongoClient


class BasicItem:
    idcounter = 0

    def __init__(self, dada_raw, name, database):
        self.db = database
        summary = dada_raw['products'][name]['buy_summary']
        self.id = BasicItem.idcounter
        self.id_name = dada_raw['products'][name]['product_id']
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
        try:
            query = {"name": self.name}
            update = {"$push": {"price_history": self.price}}
            self.db.collection.update_one(query, update)
            update = {"$push": {"time_history": self.time}}
            self.db.collection.update_one(query, update)
        except Exception as err:
            print(err)
            print("Em casos de recadrasto é esperado um erro temporario")

    def get_prices(self):
        x_raw = self.db.collection.find_one({'name': self.name})
        x = x_raw['price_history']
        y = x_raw['time_history']
        return x, y

    def get_item(self):
        item = self.db.collection.find_one({'name': self.name})
        return item

    def time_to_die(self):
        res = self.db.collection.delete_one({"name": self.name})
        print(f"Motorista deletado: {res.deleted_count} documento(s) deletados")

    def update_cli(self):
        query = {"name": self.name}
        print("Insira os novos valores")
        print("nome")
        name = input()
        print("preço")
        self.price = input()
        self.time = (datetime.now().strftime("%H:%M:%S"))
        print("Ordens")
        self.order = input()
        print("Quantidade")
        self.amount = input()
        update = {"$set": {"name": name, "price": self.price, "time": self.time, "order": self.order, "amount": self.amount}}
        self.db.collection.update_one(query, update)
        self.name = name
        print("Atualizado!")