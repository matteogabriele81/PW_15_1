"""
Questo modulo si occupa della produzione degli ortaggi.
In sintesi tutto il modulo si compone di una classe (Produzione) che si
occupa di modellare una coltivazione di un ortaggio, considerndo tutte le
caratteristiche agrononmiche che provengono dal modulo Ortaggi e tutte le
variabili dovute all'ambiente che provengono dal modulo Ambiente.
E' in questo modulo che oltre a calcolare la quantità vengono anche calcolati 
i KPI scelti per valutare la performance.
"""

import random
from datetime import datetime, timedelta
from ortaggi import ConfigurazioneOrtaggio
from ambiente import VariabiliAmbientali


class Produzione:

    def __init__(self, config: ConfigurazioneOrtaggio, metri_quadri: float, 
                 variabili_ambientali: VariabiliAmbientali):
        
        # Inizializziamo la classe con i parametri importati.

        self.config = config
        self.metri_quadri = metri_quadri
        self.variabili = variabili_ambientali
        
        # Inizializziamo quanto calcoleremo in seguito.
        self.quantita_prodotta_kg = 0
        self.giorni_necessari = 0
        self.qualita_finale = 0.0
        self.efficienza_produttiva = 0.0
        
        # Inizializziamo le date, impostate in seguito
        self.data_inizio = None
        self.data_fine = None
        
    def calcola_produzione(self):
        """
        Calcola tutti i parametri della produzione considerando le variabili ambientali.
        
        Questo è il cuore della simulazione: calcola come ogni fattore ambientale
        influenza la resa finale. Il modello usa una moltiplicazione di fattori
        moltiplicativi (tutti tra 0.0 e 1.0+) per simulare l'effetto combinato
        delle condizioni.
        
        Fattori calcolati:
        1. Suolo: fertilità e composizione del terreno
        2. Irrigazione: disponibilità idrica
        3. Temperatura: vicinanza alla temperatura ottimale dell'ortaggio
        4. Umidità: condizioni di umidità relativa dell'aria
        5. Fertilizzante: bonus produttivo se utilizzato
        6. Casualità: fattori imprevedibili (meteo, parassiti, ecc.)
        
        Il metodo aggiorna gli attributi:
        - efficienza_produttiva
        - quantita_prodotta_kg
        - qualita_finale
        - giorni_necessari
        """
        
        # SUOLO. Impostiamo a minimo 0,5 e sommando il valore randomico proveniente dal modulo Ambiente
        fattore_suolo = 0.5 + (self.variabili.qualita_suolo * 0.5)
        
        # IRRIGAZIONE. Prendiamo il valore direttamente dal modulo Ambiente
        fattore_irrigazione = self.variabili.livello_irrigazione
        
        """
        TEMPERATURA.
        Calcolo un po' più complesso. Si calcola lo scostamento della temperatura presa
        dal modulo Ambiente rispetto a quella ideale dell'ortaggio.
        Poi si confronta con la tollerenza termica proveniente dal modulo Ortaggi.
        Se la differenza è minore della tolleranza, la resa diminuisce in modo graduale.
        Nello specifico se la differenza tende a 0 la resa è al massimo, man mano che si 
        avvicina al valore di tollerenza (in alto o in basso) la resa diminuisce fino a un
        minimo del 50%. Differente è il caso che la differenza suddetta sia superiore alla
        tolleranza, nel qual caso la resa diminuisce ancor di più ma senza andare mai sotto
        il 30%.
        """
        diff_temp = abs(self.variabili.temperatura_media - self.config.temperatura_ottimale)
        if diff_temp <= self.config.tolleranza_termica:
            fattore_temperatura = 1.0 - (diff_temp / (self.config.tolleranza_termica * 2))
        else:
            fattore_temperatura = max(0.3, 1.0 - (diff_temp / (self.config.tolleranza_termica * 3)))
        
        """
        UMIDITA.
        Anche qui similmente al calcolo della temperatura calcoliamo la differenza tra
        quella in output dal modulo Ambiente e quella caratteristica dell'ortaggio.
        Anche qui calcoliamo la differenza e la sottraiamo da un 100% ipotetico fino 
        a decrescere con un limite minimo del 50%.
        """
        if 60 <= self.variabili.umidita_relativa <= 80:
            fattore_umidita = 1.0
        else:
            diff_umidita = min(abs(self.variabili.umidita_relativa - 60), 
                              abs(self.variabili.umidita_relativa - 80))
            fattore_umidita = max(0.5, 1.0 - (diff_umidita / 50))
        
        # FERTILIZZANTE. Se usato aumenta di un 15% arbitrario.
        bonus_fertilizzante = 1.15 if self.variabili.fertilizzante_usato else 1.0
        
        # KPI EFFICIENZA. Moltiplico i fattori appena calcolati.
        self.efficienza_produttiva = (fattore_suolo * fattore_irrigazione * 
                                     fattore_temperatura * fattore_umidita * 
                                     bonus_fertilizzante)
        
        # VARIAZIONE CASUALE. Un +/- 10% per aumentare l'imponderabile.
        variazione_casuale = random.uniform(0.90, 1.10)
        
        """
        QUANTITA PRODOTTA.
        Formula finale che moltiplica i metri quadri (dal modulo Simulazione) per la resa
        dal modulo Ortaggi per il KPI di efficienza calcolato e la
        variabile casuale (questi calcolati appena sopra).
        """
        self.quantita_prodotta_kg = (self.metri_quadri * self.config.resa_base * 
                                     self.efficienza_produttiva * variazione_casuale)
        
        """
        KPI QUALITA.
        Similmente al calcolo dell'altro KPI ma qui con una media pesata che tiene
        conto degli stessi fattori dell'efficienza ma con pesi leggermente diversi.
        Si è scelto di date un piccolo risalto alla temperatura, tenere umidita e suolo
        allo stesso livello e considerare appena meno importante l'irrigazione.
        Naturalmente sono scelte arbitrarie basate su condiderazioni personali.
        Da notare che il fertilizzante non c'è, viene considerato solo per la quantità.
        """
        self.qualita_finale = (fattore_suolo * 0.25 + fattore_irrigazione * 0.2 + 
                              fattore_temperatura * 0.3 + fattore_umidita * 0.25)
        
        """
        GIORNI NECESSARI. Calcolo del tempo necessario totale.
        Un tot di giorni per coltivare (usando la capacità del modulo Ortaggi) e un
        tot di giorni per raccogliere (qui si usa il tempo di crescita di Ortaggi). 
        Questo passaggio è un aggancio per un'implementazione futura che potrebbe
        tener conto della manodopera.
        """
        giorni_lavorazione = self.metri_quadri / self.config.capacita_lavorazione
        self.giorni_necessari = int(giorni_lavorazione + self.config.tempo_crescita)
        
    def imposta_date(self, data_inizio: datetime):
        """
        In questa funzione impostiamo la data di inizio (definita 1 aprile in altro modulo)
        e sommiamo i giorni di produzione calcolati appena sopra così da avere una data di fine
        campagna produttiva dell'ortaggio.
        """
        self.data_inizio = data_inizio
        # il timedelta aiuta a gestire automaticamente il cambio di mese (o anno, se necessario) senza doverlo fare a mano.
        self.data_fine = data_inizio + timedelta(days=self.giorni_necessari)
    
    def __str__(self) -> str:
        # Qui siamo alla fine dove restituiamo una stringa con la sintesi di tutti i dati calcolati.
        return (f"{self.config.tipo.value}: {self.metri_quadri:.0f} m², "
                f"{self.quantita_prodotta_kg:.1f} kg, "
                f"efficienza {self.efficienza_produttiva*100:.1f}%, "
                f"qualita {self.qualita_finale*100:.0f}%")
