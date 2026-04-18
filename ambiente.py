"""
Modulo per gestire le variabili ambientali
Qui vengono definite tutte le condizioni ambientali che influenzano
la produzione e in generale la crescita degli ortaggi nella simulazione.
"""

import random
from dataclasses import dataclass

@dataclass
class VariabiliAmbientali:
    """
    Ogni coltura ha il proprio set di parametri ambientali che
    ne determinano la quantità e qualità.
    """

    # Qualità del suolo (0.0 a 1.0)
    # 0.0 = suolo povero
    # 0.5 = suolo medio
    # 1.0 = suolo ricco e fertile
    qualita_suolo: float

    # Livello di irrigazione (0.0 a 1.0)
    # 0.0 = siccità
    # 0.5 = poca irrigazione
    # 1.0 = irrigazione adeguata
    livello_irrigazione: float

    # Temperatura media in gradi Celsius
    # Ogni coltura ha una temperatura ideale e una tolleranza a questa
    # Temperature fuori dai range riducono la capacità produttiva
    temperatura_media: float

    # Umidità dell'aria (percentuale 0-100)
    # Influenza la traspirazione e quindi potenziali malattie delle piante
    umidita_relativa: float

    # Uso di fertilizzanti
    # True/False: fertilizzanti usati/non usati
    fertilizzante_usato: bool

    def __str__(self) -> str:
        # Qui formattiamo per la visualizzazione del report finale
        # tutte le informazioni in una stringa riepilogativa.
        return (f"Suolo: {self.qualita_suolo:.2f}, Irrigazione: {self.livello_irrigazione:.2f}, "
                f"Temp: {self.temperatura_media:.1f}°C, Umidita: {self.umidita_relativa:.0f}%, "
                f"Fertilizzante: {'Si' if self.fertilizzante_usato else 'No'}")

def genera_variabili_casuali() -> VariabiliAmbientali:
    """
    Qui viene generato il set di variabili legate all'ambiente per ogni
    coltura.
    I range scelti sono rappresentativi di condizioni realistiche senza
    introdurre valori estremi tipici di ambienti che non rappresentano
    quelli italiani.
    Range scelti:
    - qualita_suolo: 0.5-0.95 (no ai terrei completamente non adatti)
    - livello_irrigazione: 0.6-1.0 (irrigazione da buona a ottima)
    - temperatura: 20-30°C (temperature medie italiane)
    - umidita: 50-90% (umidità media italiana)
    - fertilizzante: 50% probabilità (è scelto col 50/50, si può impostare)
    Come returns abbiamo VariabiliAmbientali, un oggetto con tutte le condizioni generate
    """
    return VariabiliAmbientali(
        qualita_suolo=random.uniform(0.5, 0.95),
        livello_irrigazione=random.uniform(0.6, 1.0),
        temperatura_media=random.uniform(20.0, 30.0),
        umidita_relativa=random.uniform(50.0, 90.0),
        fertilizzante_usato=random.choice([True, False])
    )