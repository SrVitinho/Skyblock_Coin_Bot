from datetime import datetime


class BasicItem:
    idcounter = 0
    def __init__(self, dada_raw, name):
        summary = dada_raw['products'][name]['buy_summary']
        self.id = BasicItem.idcounter
        self.id_name = dada_raw['products'][name]['product_id']
        self.price = []
        self.time = []
        BasicItem.idcounter += 1
        if type(summary) is list:  # Caso nao possua muitas ofertas de compra não será lista
            self.name = name
            self.price.append(dada_raw['products'][name]['buy_summary'][0]['pricePerUnit'])
            self.time.append(datetime.now().strftime("%H:%M:%S"))
            self.order = dada_raw['products'][name]['buy_summary'][0]['orders']
            self.amount = dada_raw['products'][name]['buy_summary'][0]['amount']
        else:
            self.name = name
            self.price.append(['products'][name]['buy_summary']['pricePerUnit'])
            self.time.append(datetime.now().strftime("%H:%M:%S"))
            self.order = dada_raw['products'][name]['buy_summary']['orders']
            self.amount = dada_raw['products'][name]['buy_summary']['amount']
