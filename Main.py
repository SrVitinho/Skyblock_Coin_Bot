import requests
from Classes import *
from Classes.basic_item import BasicItem
from Classes.especial_item import EspecialItem
import matplotlib.pyplot as plt
import time
import threading as tdr
import Keys
from datetime import datetime

from Database import Database

watchers = {}
db = Database(database="Skyblock", collection="Coin")


def getsjson():
    param = {"key": Keys.hypixel_api, "Name": Keys.hypixel_name}
    r = requests.get('https://api.hypixel.net/skyblock/bazaar', param, timeout=2)  # Request from API
    rc = r.json()
    return rc


def graph(especial_itens, itens, name, Case):
    if Case:
        y, x = itens[name].get_prices()
    else:
        y, x = especial_itens[name].get_prices()

    print(y)
    print(x)
    plt.plot(x, y)
    plt.ylabel('Preco')
    plt.xlabel('Tempo')
    plt.show()


def getdata(i_name, e_name, itens, e_itens):
    while True:
        print('New circle started')
        rc = getsjson()

        for i in i_name:
            summary = rc['products'][i]['buy_summary']
            if type(summary) is list:
                i_price = rc['products'][i]['buy_summary'][0]['pricePerUnit']
                itens[i].price = i_price
                itens[i].time = (datetime.now().strftime("%H:%M:%S"))
            else:
                i_price = rc['products'][i]['buy_summary']['pricePerUnit']
                itens[i].price = i_price
                itens[i].time = (datetime.now().strftime("%H:%M:%S"))
            itens[i].update_price()

        for i in e_name:
            summary = rc['products'][i]['buy_summary']
            if type(summary) is list:
                e_price = rc['products'][i]['buy_summary'][0]['pricePerUnit']
                e_itens[i].price = e_price
                e_itens[i].time = (datetime.now().strftime("%H:%M:%S"))
            else:
                e_price = rc['products'][i]['buy_summary']['pricePerUnit']
                e_itens[i].price = e_price
                e_itens[i].time = (datetime.now().strftime("%H:%M:%S"))
            e_itens[i].update_price()
        checkwatcher(itens)
        time.sleep(5)


def itensregistration():
    db.resetDatabase()
    rc = getsjson()
    names = (rc['products']).keys()
    itens = {}
    especial_itens = {}
    itens_names = []
    especial_names = []
    error_normal = 0
    error_especial = 0
    added_normal = 0
    added_especial = 0

    for i in names:  # loop adição dos itens
        if not ((i.startswith('ENCHANTED_')) or (i.startswith('ENCHANTMENT_'))):
            try:  # try - except para itens nao disponiveis
                print('trying to add ' + i)
                itens[i] = BasicItem(rc, i, db)
                itens_names.append(i)
                added_normal += 1
                print('Added')
            except Exception as err:
                print(type(err).__name__)
                print(err)
                error_normal = error_normal + 1

        if (i.startswith('ENCHANTED_')) or (i.startswith('ENCHANTMENT_')):
            try:
                print('trying to add ' + i)
                especial_itens[i] = EspecialItem(rc, i, db)
                especial_names.append(i)
                added_especial += 1
                print('Added')
            except Exception as err:
                print(type(err).__name__)
                print(err)
                error_especial = error_especial + 1

    print("Final error_normal count:" + error_normal.__str__())
    print("Final error_especial count:" + error_especial.__str__())
    print("Final added_especial count:" + added_especial.__str__())
    print("Final added_normal count:" + added_normal.__str__())
    return especial_itens, itens, itens_names, especial_names


def menuwatchers():  # needs change -s
    print("1 -> Adicionar Watcher")
    print("2 -> Listar Watchers")
    print("3 -> Remover Watchers")

    user_input = int(input())

    if user_input == 1:
        id = input("Qual o id do item?")
        price_target = float(input("Qual o valor alvo?"))

        watchers = addwatcher(id, price_target)

    elif user_input == 2:
        listwatcher()

    elif user_input == 3:
        id_to_remove = input("Qual o id do item a ser removido?")

        watchers = removewatcher(id_to_remove)


def checkwatcher(itens):  # needs change -s
    watchers_keys = watchers.keys()
    for i in watchers_keys:
        if watchers[i] <= itens[i].price[-1]:
            print('ALARME NO WATCHER: ' + i)


def removewatcher(id):  # needs change -s
    try:
        del watchers[id]
    except Exception as err:
        print('Item nao cadastrado dentro dos watchers')


def addwatcher(id, price_target):  # needs change -s
    try:
        watchers[id] = price_target
    except Exception as err:
        print('Item ja cadastrado')


def listwatcher():  # needs change -s
    for i in watchers:
        print(i + " com price target de " + str(watchers[i]))


if __name__ == "__main__":
    especial_itens, itens, itens_name, especial_itens_names = itensregistration()

    x = tdr.Thread(target=getdata, args=(itens_name, especial_itens_names, itens, especial_itens))
    x.start()

    #  graph(especial_itens, itens, 'INK_SACK:4', 1)

    while True:
        print("Qual operacao gostaria de realizar?")
        print("1 -> Verificar um grafico")
        print("2 -> Menu Watcher")
        print("3 -> Cadastrar Itens (ATENCAO ESSA OPERACAO RESETA TODAS AS TABELAS e seus valores!)")
        decision = int(input())
        print(decision)
        if decision == 1:
            print("Insira o ID do produto")
            name = input()
            if name.startswith('ENCHANTED_') or (name.startswith('ENCHANTMENT_')):
                graph(especial_itens, itens, name, 0)
            else:
                graph(especial_itens, itens, name, 1)
        elif decision == 2:
            menuwatchers()
        else:
            print('Entrada Invalida')
