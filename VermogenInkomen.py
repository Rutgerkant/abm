


import numpy as np

import random


# Definieer de vermogensintervallen en bijbehorende aantallen huishoudens
vermogensintervallen = [
    ("nulde Deciel", -np.inf, -1.5, -8, 19),
    ("eerste Deciel", -1.5, 2, 19, 25),
    ("tweede Deciel", 2, 12.4, 25, 29),
    ("derde Deciel", 12.4, 50.2, 29, 35),
    ("vierde Deciel", 50.2, 135.1, 35, 41),
    ("vijfde Deciel", 135.1, 218.6, 41, 51),
    ("zesde Deciel", 218.6, 312.0, 51, 59),
    ("zevende Deciel", 312.0, 434.80, 59, 71),
    ("achtste Deciel", 434.80, 670.5, 71, 89),
    ("negende Deciel", 670.5, np.inf, 89, 150)
]

aantallen_huishoudens = [793, 793, 793, 793, 793, 793, 793, 793, 793, 793]



def genereer_random_vermogen():
    vermogenswaarden = []
    vermogensgewichten = []

    for interval in vermogensintervallen:
        label, min_vermogen, max_vermogen, ondergrens_inkomen, bovengrens_inkomen = interval
        if np.isinf(min_vermogen) or np.isinf(max_vermogen):
            vermogenswaarden.append(max_vermogen if np.isinf(min_vermogen) else min_vermogen)  
        else:
            vermogenswaarden.append((min_vermogen + max_vermogen) / 2)  
        vermogensgewichten.append(aantallen_huishoudens[vermogensintervallen.index(interval)])


    gekozen_index = np.random.choice(len(vermogenswaarden), p=vermogensgewichten/np.sum(vermogensgewichten))
    min_vermogen, max_vermogen = vermogensintervallen[gekozen_index][1], vermogensintervallen[gekozen_index][2]
    if np.isinf(min_vermogen) or np.isinf(max_vermogen):
        vermogen_agent = vermogenswaarden[gekozen_index] * 1000  # Verander de waarde naar euro's
    else:
        vermogen_agent = np.random.uniform(min_vermogen, max_vermogen) * 1000  # Verander de waarde naar euro's en genereer binnen het interval

    min_inkomen, max_inkomen = vermogensintervallen[gekozen_index][3], vermogensintervallen[gekozen_index][4]   
    inkomen_agent = random.randint(min_inkomen, max_inkomen) * 1000

    vermogen_auto = vermogen_agent * 0.125
    inkomen_auto = inkomen_agent * 0.15 / 12


    return (vermogen_auto, inkomen_auto)


random_vermogen, random_inkomen = genereer_random_vermogen()


