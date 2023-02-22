# ----- initialistion des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process


# ----- initialistion des modules -----#

# ----- initialistion des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE


w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
# ----- initialistion des couleurs du modules pystyle -----#

# ----- initialistion des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_5m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
# ----- initialistion des temps de recherches -----#

# ----- initialistion de l'API key et ticker -----#
api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
ticker = 'X:IOSTUSD'
tiker_live = 'IOST/USD'


# ----- initialistion de l'API key et ticker -----#

# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#


def Finder_IETE(time1, time_name1, start1):
    # global proxies
    # while True:

    with my_lock:

        api_url_livePrice = f'http://api.polygon.io/v1/last/crypto/{tiker_live}?apiKey={api_key}'
        data = requests.get(api_url_livePrice).json()
        df_livePrice = pd.DataFrame(data)

        # api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/15/minute/2022-07-01/2022-07-15?adjusted=true&sort=asc&limit=30000&apiKey={api_key}'
        api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start1}/{end}?adjusted=true&limit=50000&apiKey={api_key}'

        data = requests.get(api_url_OHLC).json()
        df = pd.DataFrame(data['results'])
        la_place_de_p = 0

        for k in range(0, len(df_livePrice.index)):
            if df_livePrice.index[k] == 'price':
                la_place_de_p = k
        livePrice = df_livePrice['last'][la_place_de_p]
    dernligne = len(df['c']) - 1
    df.drop([dernligne], axis=0, inplace=True)

    # df = df.drop(columns=['o', 'h', 'l', 'v', 'vw', 'n'])
    # df = df.append({'o': NAN, 'h': NAN, 'l': NAN, 'v': NAN, 'vw': NAN, 'n': NAN, 'c': livePrice, 't': NAN}, ignore_index=True)
    df_new_line = pd.DataFrame([[NAN, NAN, NAN, NAN, NAN, NAN, livePrice, NAN]],
                               columns=['o', 'h', 'l', 'v', 'vw', 'n', 'c', 't'])
    df = pd.concat([df, df_new_line], ignore_index=True)
    df_data_date = []
    df_data_price = []
    for list_df in range(len(df)):
        df_data_date.append(df['t'].iloc[list_df])
        df_data_price.append(df['c'].iloc[list_df])
    data_date = pd.DataFrame(df_data_date, columns=['Date'])
    data_price = pd.DataFrame(df_data_price, columns=['Price'])
    df_wise_index = pd.concat([data_date, data_price], axis=1)

    place_liveprice = (len(df) - 1)

    for data in range(len(df_wise_index)):

        try:

            if df_wise_index['Price'].iloc[data] == df_wise_index['Price'].iloc[data + 1]:
                df = df.drop(df_wise_index['Date'].iloc[data + 1])
        except:

            # print('ok')
            aaa = 0

    # ----- creation des local(min/max) -----#
    local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
    local_max1 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min1 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

    local_max2 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min2 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

    # ----- creation des local(min/max) -----#

    # ----- suppresion des points morts de la courbe -----#
    test_min = []
    test_max = []

    # if local_min[0] > local_max[0]:
    #        local_max = local_max[1:]
    #        print('On a supprimer le premier point')
    #
    q = 0
    p = 0

    len1 = len(local_min)
    len2 = len(local_max)
    while p < len1 - 5 or p < len2 - 5:
        if local_min[p + 1] < local_max[p]:
            test_min.append(local_min[p])
            local_min = np.delete(local_min, p)

            p = p - 1
        if local_max[p + 1] < local_min[p + 1]:
            test_max.append(local_max[p])
            local_max = np.delete(local_max, p)

            p = p - 1
        p = p + 1

        len1 = len(local_min)
        len2 = len(local_max)

    highs = df.iloc[local_max, :]
    lows = df.iloc[local_min, :]
    highs1 = df.iloc[test_max, :]
    lows1 = df.iloc[test_min, :]

    decalage = 0

    # ----- suppresion des points morts de la courbe -----#
    AA = float(df['c'].iloc[local_min[-4]])
    BB = float(df['c'].iloc[local_max[-3]])
    A = float(df['c'].iloc[local_min[-3]])
    B = float(df['c'].iloc[local_max[-2]])
    C = float(df['c'].iloc[local_min[-2]])
    D = float(df['c'].iloc[local_max[-1]])
    E = float(df['c'].iloc[local_min[-1]])
    F = float(livePrice)

    print('--- Mode recherche IOST', time1, time_name1, ' ---', flush=True)

    data_A = []
    data_B = []
    data_C = []
    data_D = []
    data_E = []
    data_F = []

    rouge = []
    vert = []
    bleu = []

    rouge.append(local_min[-4])
    rouge.append(local_max[-3])
    rouge.append(local_min[-3])
    rouge.append(local_max[-2])
    rouge.append(local_min[-2])
    rouge.append(local_max[-1])
    rouge.append(local_min[-1])
    rouge.append(place_liveprice)


    i = 0
    for i in range(local_max[-4] - 1, len(df)):
        bleu.append(i)

    mirande = df.iloc[rouge, :]
    mirande3 = df.iloc[bleu, :]


    rouge1 = {'c': rouge}
    rouge2 = pd.DataFrame(data=rouge1)
    bleu1 = {'c': bleu}
    bleu2 = pd.DataFrame(data=bleu1)

    pourcent = False
    placement = False

    if ((BB - AA)*100)/A >= 3:
        pourcent = True

    if local_min[-4] < local_max[-3] < local_min[-3] < local_max[-2] < local_min[-2] < local_max[-1] < local_min[-1] < place_liveprice :
        placement = True

    if ((BB - AA) > (BB - A) and (BB - A) > (B - A) and (B - A) > (B - C) and (B - C) > (D - C) and (D - C) > (D - E) and (D - E) > (F - E) and df['c'].values[-2] == lows['c'].iloc[-1]) or ((AA - BB) > (A - BB) and (A - BB) > (A - B) and (A - B) > (C - B) and (C - B) > (C - D) and (C - D) > (E - D) and (E - D) > (F - E) and df['c'].values[-2] == highs['c'].iloc[-1]) and pourcent == True and placement == True:



            #plus_grand = round((J[1] + (moyenne_tete) / 2), 5)
            #plus_petit = round(G, 5)
            #pourcent_chercher = ((plus_grand - plus_petit) / plus_petit)*100
            #pourcent_chercher = round(pourcent_chercher, 3)
            fig = plt.figure(figsize=(10, 7))
            # fig.patch.set_facecolor('#17abde'
            plt.plot([], [], ' ')
            plt.title(f'IETE : {tiker_live} | {time1} {time_name1} ', fontweight="bold", color='black')
            mirande3['c'].plot(color=['blue'], label='Clotures')
            # mirande['c'].plot(color=['#FF0000'])

            plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
            # point_max = J[0]+((J[0] - I[0])/taille_diviser)
            # plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red',label='Max temps realisation')
            plt.legend()
            plt.text(local_min[-4], AA, "AA", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[-3], BB, "BB", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[-3], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
            #plt.text(J[0], J[1] + (moyenne_tete) / 2, f"{round((J[1] + (moyenne_tete) / 2), 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[-2], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[-2], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[-1], D, "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[-1], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(place_liveprice, F, f"F  {round(F, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            #plt.text(place_liveprice, G, f"G  {round(G, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            #plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
            # test_valeur = df['c'].iloc[round(J[0]) + 1]
            # plt.text(round(J[0]), df['c'].iloc[round(J[0])], f"J+1 {test_valeur}", ha='left',style='normal', size=10.5, color='#00FF36', wrap=True)
            plt.scatter(len(df['c']) - 1, df['c'].values[-1], color='blue', label='liveprice')
            plt.show()
            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#
            # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'r')
            # compteur_nombre_image = int(file.read())
            # file.close()
            # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'w')
            # compteur_nombre_image = compteur_nombre_image + 1
            # file.write(f'{compteur_nombre_image}')
            # file.close(
            # plt.savefig(f'images/figure_{compteur_nombre_image}.png'
            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

            data_A.append(A)
            data_B.append(B)
            data_C.append(C)
            data_D.append(D)
            data_E.append(E)
            data_F.append(F)
            data_A_ = pd.DataFrame(data_A, columns=['A'])
            data_B_ = pd.DataFrame(data_B, columns=['B'])
            data_C_ = pd.DataFrame(data_C, columns=['C'])
            data_D_ = pd.DataFrame(data_D, columns=['D'])
            data_E_ = pd.DataFrame(data_E, columns=['E'])
            data_F_ = pd.DataFrame(data_E, columns=['F'])
            df_IETE = pd.concat([data_A_, data_B_, data_C_, data_D_, data_E_, data_F_], axis=1)
    print('----------------------------------------------------------------------', flush=True)
    time.sleep(0.5)


minute = "minute"
heure = "hour"
jour = "day"

th1 = Process(target=Finder_IETE, args=(15,minute,start_15m))
th2 = Process(target=Finder_IETE, args=(20,minute,start_15m))
th3 = Process(target=Finder_IETE, args=(25,minute,start_15m))
th4 = Process(target=Finder_IETE, args=(30,minute,start_30m))
th5 = Process(target=Finder_IETE, args=(35,minute,start_30m))
th7 = Process(target=Finder_IETE, args=(45,minute,start_30m))
th9 = Process(target=Finder_IETE, args=(1,heure,start_1h))
th10 = Process(target=Finder_IETE, args=(2,heure,start_1h))
th11 = Process(target=Finder_IETE, args=(4,heure,start_1h))
th12 = Process(target=Finder_IETE, args=(6,heure,start_6h))
th13 = Process(target=Finder_IETE, args=(10,heure,start_6h))
th14 = Process(target=Finder_IETE, args=(12,heure,start_6h))
th15 = Process(target=Finder_IETE, args=(1,jour,start_1d))

th1.start()
th2.start()
th3.start()
th4.start()
th5.start()
th7.start()
th9.start()
th10.start()
th11.start()
th12.start()
th13.start()
th14.start()
th15.start()


th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
th7.join()
th9.join()
th10.join()
th11.join()
th12.join()
th13.join()
th14.join()
th15.join()















