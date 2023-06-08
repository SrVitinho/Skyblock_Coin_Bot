from Classes.basic_item import BasicItem


class EspecialItem(BasicItem):
    def __init__(self, dada_raw, name, db):
        super().__init__(dada_raw, name, db)
        summary = dada_raw['products'][name]['quick_status']
        if type(summary) is list:
            self.volumeSold = dada_raw['products'][name]['quick_status'][0]['buyMovingWeek']
            self.putosale = dada_raw['products'][name]['quick_status'][0]['sellMovingWeek']
        else:
            self.volumeSold = dada_raw['products'][name]['quick_status']['buyMovingWeek']
            self.putosale = dada_raw['products'][name]['quick_status']['sellMovingWeek']

        self.Especial_Json = {
            "name": self.name,
            "price": self.price,
            "time": self.time,
            "order": self.order,
            "amount": self.amount,
            "summary": [
                {
                    "Volume_Sold": self.volumeSold,
                    "Put_to_Sale": self.putosale
                }
            ],
            "price_history": [],
            "time_history": []
        }

        self.db.collection.insert_one(self.Especial_Json)

