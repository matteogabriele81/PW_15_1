"""
Modulo per la configurazione degli ortaggi nonchè la loro enumerazione.
Ognuno ha delle caratteristiche specifiche che ne influenzano la produttività
"""

from enum import Enum
from dataclasses import dataclass

class TipoOrtaggio(Enum):

    # Enumerazione degli ortaggi, punto per crearne anche altri alla bisogna.

    POMODORO = "Pomodoro San Marzano"
    MELANZANA = "Melanzana Violetta di Firenze"
    ZUCCHINA = "Zucchina Romanesco"

@dataclass
class ConfigurazioneOrtaggio:
    """
    Qui creiamo una clase per ogni ortaggio con tutto un set di
    parametri agronomici che lo contraddistingue.
    """

    tipo: TipoOrtaggio
    resa_base: float
    capacita_lavorazione: float
    tempo_crescita: int
    fabbisogno_idrico: float
    temperatura_ottimale: float
    tolleranza_termica: float

def crea_configurazioni_default() -> dict:
    """
    Qua andiamo a creare un dizionario con le configurazioni.
    I valori sono stati stimati prendendo fonti pubbliche su internet.
    In generale:
    - Produttività (parametro resa_base): quanto si raccoglie in kg per metro quadro
    - Capacità (parametro capacita_lavorazione): quanto terreno si riesce a coltivare in un giorno
    - Velocità (parametro tempo_crescita): quanto tempo richiede per produrre
    - Esigenze (parametro fabbisogno_idrico): quanta acqua serve al tipo di ortaggio
    - Adattabilità (parametro tolleranza_termica): quanto è resistente ad un temperatura diversa da quella ottimale
    Come returns avremo un dizionario con chiave TipoOrtaggio e valore ConfigurazioneOrtaggio
    """
    return {
        
        # la spiegazione dei parametri è riportata solo nel primo ortaggio per evitare ripetizioni

        TipoOrtaggio.POMODORO: ConfigurazioneOrtaggio(
            tipo=TipoOrtaggio.POMODORO,

            # 5.5 significa che su 1000 m² si ottengono circa 5500 kg, senza variazioni per cause esterne
            resa_base=5.5,

            # 120 vuol dire che in un giorno si riescono a coltivare 120 metri quadrati
            capacita_lavorazione=120.0,

            # 75 significa che per raccogliere gli ortaggi maturi servono 75 giorni
            tempo_crescita=75,

            # 3,5 indica i litri d'acqua al giorno che occorrono a questo tipo di ortaggio
            fabbisogno_idrico=3.5,

            # 24 gradi è la temperatura ottimale
            temperatura_ottimale=24.0,

            # l'ortaggio in questione tollera variazioni di temperatura di +/- 4 gradi
            tolleranza_termica=4.0
        ),

        TipoOrtaggio.MELANZANA: ConfigurazioneOrtaggio(
            tipo=TipoOrtaggio.MELANZANA,
            resa_base=4.0,
            capacita_lavorazione=100.0,
            tempo_crescita=80,
            fabbisogno_idrico=4.0,
            temperatura_ottimale=25.0,
            tolleranza_termica=4.5
        ),

        TipoOrtaggio.ZUCCHINA: ConfigurazioneOrtaggio(
            tipo=TipoOrtaggio.ZUCCHINA,
            resa_base=6.5,
            capacita_lavorazione=130.0,
            tempo_crescita=60,
            fabbisogno_idrico=4.5,
            temperatura_ottimale=22.0,
            tolleranza_termica=5.0
        )
    }