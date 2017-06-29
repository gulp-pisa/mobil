#! /usr/bin/python3

"""
Questo script effettua le assegnazioni, prendendo i punteggi dei singoli
candidati per dati.
"""

import pandas as pd
from utils.fake_prefs import crea_preferenze as preferenze_candidato

from collections import defaultdict

L_CLASSE = 'Tipo posto/classe di concorso'
L_CAND_CLASSE = 'Codice CLC / Tipo Posto Sostegno'

candidati = pd.read_excel('dati/candidati.xlsx')

# Dai punteggio 1000 a chi non ha alcuna precedenza:
ordine_precedenze = defaultdict(lambda : 1000,
{#I nessun caso
#II nessun caso
'personale che ha bisogno per gravi patologie di particolari cure a carattere continuativo  (art. 13  del CCNI comma 1 punto III)' : 3,
'Art. 21 della L. 104/92  (art. 13  comma 1 punto III)' : 3,
'Art. 33, comma 6, della L. 104/92  (art. 13   del CCNI comma 1 punto III)' : 3,
#IV nessun caso
'Art. 33, commi 5 e 7 L.104/92  - Assistenza Figlio (art. 13 del CCNI  comma 1 punto V)' : 5,
'Art. 33, commi 5 e 7 L.104/92  - Assistenza Coniuge/Genitore  (art. 13 del CCNI  comma 1 punto V)' : 5,
'Coniuge di Militare o di categoria equiparata  (art. 13   del CCNI comma 1 punto VI)' : 6,
'Personale che ricopre cariche pubbliche nelle amministrazioni locali (art. 13  del CCNI comma 1 punto VII)' : 7,
'Art. 13 del CCNI comma 1 punto VIII' : 8,
# FIXME: Non siamo certi che vada in fondo:
"Precedenza prevista per l'accesso ai corsi per l'istruzione e la formazione dell'età adulta  (art. 32 CCNI." : 10,
})

# Le preferenze sono numerate dalla più alla meno prioritaria:
candidati['ord_prec'] = -candidati['Precedenza'].apply(lambda x : ordine_precedenze[x])

# FIXME: c'è ancora da disambiguare alcuni pareggi
candidati.sort_values(['ord_prec', 'Punteggio'], inplace=True, ascending=False)

disponibilità = pd.read_excel('dati/Disponibilita_II grado Ambito.xlsx',
                              keep_default_na=False,
                              na_values=[''])

# Per ora solo per fare un esempio:
CLASSE = 'A013'
# Tutto ciò che segue andrà fatto per ogni classe

assegnati_per_zona = defaultdict(lambda : 0)

# Ci sono vari tipi di disponibilità:
disponibilità['tot'] = disponibilità[[c for c in disponibilità
                                      if c.startswith('Disponibilità')]].sum(axis=1)

disp_classe = disponibilità[disponibilità[L_CLASSE] == CLASSE]

# "zona" = scuola, provincia o ambito

posti_per_zona = {}
posti_per_zona.update(disp_classe.set_index('Istituto principale')['tot'])
posti_per_zona.update(disp_classe.groupby('Ambito').tot.sum())
posti_per_zona.update(disp_classe.groupby('Sigla prov').tot.sum())

ambito_per_zona = {}
ambito_per_zona.update(disp_classe.set_index('Istituto principale')['Ambito'])

provincia_per_zona = {}
provincia_per_zona.update(disp_classe.set_index('Istituto principale')['Sigla prov'])
provincia_per_zona.update(disp_classe.groupby('Ambito')['Sigla prov'].first())

cand_classe = candidati[candidati[L_CAND_CLASSE] == CLASSE]


for row_id, row in cand_classe.iterrows():
    preferenze = preferenze_candidato(row_id)
    for tipo_p, pref in preferenze:
        try:
            disp = posti_per_zona[pref]
        except KeyError:
            # "posti_per_zona" non riporta affatto zone che non hanno
            # proprio disponibilità per questa classe
            disp = 0
