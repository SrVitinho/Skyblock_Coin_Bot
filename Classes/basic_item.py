class BasicItem:
    def __init__(self, dada_raw, name):
        summary = dada_raw['products'][name]['buy_summary']
        if type(summary) is list:
            self.name = name
            self.price = dada_raw['products'][name]['buy_summary'][0]['pricePerUnit']
            self.order = dada_raw['products'][name]['buy_summary'][0]['orders']
            self.amount = dada_raw['products'][name]['buy_summary'][0]['amount']
        else:
            self.name = name
            self.price = dada_raw['products'][name]['buy_summary']['pricePerUnit']
            self.order = dada_raw['products'][name]['buy_summary']['orders']
            self.amount = dada_raw['products'][name]['buy_summary']['amount']

