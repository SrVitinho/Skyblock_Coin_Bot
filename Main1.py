import requests
from Classes import *
from Classes.basic_item import BasicItem
from Classes.especial_item import EspecialItem


def main():
    param = {"key": "f823311c-be1f-44d5-81e9-2cae41baa0e2", "Name": "SrVitinho"}
    r = requests.get('https://api.hypixel.net/skyblock/bazaar', param, timeout=2)
    rc = r.json()
    names = (rc['products']).keys()
    itens = []
    especial_itens = []
    error_normal = 0
    error_especial = 0

    for i in names:
        if not i.startswith('ENCHANTED_'):
            try:
                print('trying to add ' + i)
                itens.append(BasicItem(rc, i))
                print('Added')
            except Exception as err:
                print(type(err).__name__)
                print(err)
                error_normal = error_normal + 1

        if i.startswith('ENCHANTED_'):
            try:
                print('trying to add ' + i)
                especial_itens.append(EspecialItem(rc, i))
                print('Added')
            except Exception as err:
                print(type(err).__name__)
                print(err)
                error_especial = error_especial + 1

    print("Final error_normal count:" + error_normal.__str__())
    print("Final error_especial count:" + error_especial.__str__())


if __name__ == "__main__":
    main()
