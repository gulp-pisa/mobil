"""
In assenza dei dati riguardanti le preferenze, questo modulo crea una lista di
preferenze casuali per ogni candidato.
"""

import pandas as pd
import random

disponibilità = pd.read_excel('dati/Disponibilita_II grado Ambito.xlsx',
                              keep_default_na=False,
                              na_values=[''])

province = list(set(disponibilità['Sigla prov']))
ambiti = list(set(disponibilità['Ambito']))
scuole = list(set(disponibilità['Istituto principale']))

def crea_preferenze(*args):
    res = []
    if random.random() < .8:
        res.append(('s', random.choice(scuole)))
    
    n_prov = random.randint(1, min(100, len(province)))
    n_ambi = random.randint(1, min(100 - n_prov, len(ambiti)))
    prov = random.sample(province, n_prov)
    ambi = random.sample(ambiti, n_prov)
    
    tutti = [('p', p) for p in prov] + [('a', a) for a in ambi]
    random.shuffle(tutti)
    
    res.extend(tutti)
    return res
