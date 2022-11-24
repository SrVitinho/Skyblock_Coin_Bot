import requests
import time
import json

tempo = time.time()
Lp1d = 12000
Lp1s = 12000
Llow = 12000
Lmax1d = 0
Lmax1s = 0
Tpd = tempo + 86400
Tps = tempo + 604800

while (True):

    if (time.time() >= tempo):
        print("Pedindo valor em:", time.asctime(time.localtime()))
        param = {"key": "f823311c-be1f-44d5-81e9-2cae41baa0e2", "Name": "SrVitinho"}
        r = requests.get('https://api.hypixel.net/skyblock/bazaar', param, timeout=3)

    if (r.status_code == 200):
        Lapis_raw = r.json()
        Lapis_price = Lapis_raw['products']['ENCHANTED_LAPIS_LAZULI']['sell_summary'][0]['pricePerUnit']
        r.status_code = 1337
        tempo_lct = time.asctime(time.localtime())

        if (Llow > Lapis_price):
            Llow = Lapis_price
            if (Llow > Lp1s):
                Lp1s = Llow
                Lp1d = Llow
            elif (Llow > Lp1d):
                Lp1d = Llow

        data = {"E.Lapis": {
            "Price": str(Lapis_price),
            "Lp1d": str(Lp1d),
            "Lp1s": str(Lp1s),
            "Lmax1d": str(Lmax1d),
            "Lmax1s": str(Lmax1s)
        }
        }

        with open('Chocobu.txt', 'a') as f:
            f.write(" \n ---------------------------- \n" + tempo_lct)
            f.write("|| Preco do Ench. Lapis --> ")
            potato = (str(Lapis_price) + " Menor valor do dia --> " + str(Lp1d) + " Menor valor da semana --> " + str(
                Lp1s) + "\n")
            print('potato')
            f.write(potato)
            potato = (" Maior valor do dia --> " + str(Lmax1d) + " Maior Valor da semana --> " + str(Lmax1s))
            f.write(potato)
        with open('Data.txt', 'a') as f:
            f.write(str(data))
        r.status_code = 1337
        tempo = tempo + 600
    elif (r.status_code == 1337):
        r.status_code = 1337
    else:
        r.status_code = 1337
        tempo_lct = time.asctime(time.localtime())
        with open('Chocobu.txt', 'a') as f:
            f.write("Erro na API as ")
            f.write(tempo_lct)
            f.write(' Erro ')
            f.write(r.status_code)
            f.write("\n")
    if (tempo > Tpd):
        Tpd = tempo + 86400
        Lp1d = 12000
        Lmax1d = 0
    if (tempo > Tps):
        Tps = tempo + 604800
        Lp1s = 12000
        Lmax1s = 0