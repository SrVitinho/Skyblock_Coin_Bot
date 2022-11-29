from Classes.basic_item import BasicItem


class EspecialItem(BasicItem):
    def __init__(self, dada_raw, name):
        super().__init__(dada_raw, name)
        summary = dada_raw['products'][name]['quick_status']
        if type(summary) is list:
            self.volumeSold = dada_raw['products'][name]['quick_status'][0]['buyMovingWeek']
            self.putosale = dada_raw['products'][name]['quick_status'][0]['sellMovingWeek']
        else:
            self.volumeSold = dada_raw['products'][name]['quick_status']['buyMovingWeek']
            self.putosale = dada_raw['products'][name]['quick_status']['sellMovingWeek']


