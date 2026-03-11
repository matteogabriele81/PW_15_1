"""
Questo il modulo principale per tutta la simulazione, si occupa
di orchestrare tutta la logica contattando gli altri moduli.
E alla fine prepara un report da restituire al modulo Main.
"""

import random
from datetime import datetime
from typing import List, Dict, Tuple
from ortaggi import crea_configurazioni_default
from ambiente import genera_variabili_casuali
from produzione import Produzione


class SimulatoreFattoria:
    """
    SimulatoreFattoria è la classe principale, richiama i metodi degli
    altri moduli per prendere i dati ambientali, agronomici e di produzione
    nonchè di aggregare il tutto in una stringa di report come return
    da restituire all'utente che ha lanciato il software.
    """

    def __init__(self):
        # Carichiamo le tre (o piu) configurazioni degli ortaggi
        self.configurazioni = crea_configurazioni_default()

    def genera_produzioni_casuali(self) -> List[Produzione]:
        # Carichiamo i parametri di produzione in una lista che inizializziamo
        produzioni = []
        
        # Iteriamo su tutte le configurazioni di ortaggio esistenti
        for config in self.configurazioni.values():
            # Generiamo una superficie di coltivazione casuale con min e max impostati
            metri_quadri = random.uniform(300, 1200)

            # Generiamo le variabili ambientali richiamando il metodo di Ambiente
            variabili = genera_variabili_casuali()
            
            # In ogni oggetto Produzione salviamo la configurazione, i metri quadrati e i parametri ambientali
            produzione = Produzione(config, metri_quadri, variabili)
            produzioni.append(produzione)
            
        # Restituiamo la lista con tutti i dati
        return produzioni
    
    def simula_produzione(self, produzioni: List[Produzione], 
                         data_inizio: datetime = None) -> Tuple[List[Produzione], Dict]:
        """
        Questo è il cuore della simulazione. Impostiamo l'inizio, uguale per tutti,
        e calcoliamo la data di fine per ogni coltivazione, calcoliamo le statistiche
        e restituiamo in output informazioni durante la simulazione.
        In return avremo una tupla con la lista delle produzioni della funzione
        precedente e un dizionario con i dati calcolati qui.
        """
        
        # La data è settata nel modulo Main ma prevediamo che se non ci fosse, imposteremmo il momento di esecuzione
        if data_inizio is None:
            data_inizio = datetime.now()
        
        # Output con intestazione di landing per l'utente
        print("\n" + "="*80)
        print("SIMULAZIONE PRODUZIONE ORTAGGI")
        print("="*80)
        print("I tre tipi di ortaggi vengono coltivati contemporaneamente.")
        print()
        
        # Ora iteriamo enumerando tutte le produzioni del modulo precedente e calcoliamo
        for i, produzione in enumerate(produzioni, 1):
            # La produzione con tempi e KPI
            produzione.calcola_produzione()
            
            # passiamo il data_inizio a Produzione che restituisce la data di fine
            produzione.imposta_date(data_inizio)
            
            # Generaimo un output dei dati fino a questo punto
            
            print(f"\n[{i}] {produzione.config.tipo.value}")
            print(f"    Periodo: {produzione.data_inizio.strftime('%d/%m/%Y')} - {produzione.data_fine.strftime('%d/%m/%Y')}")
            print(f"    Area coltivata: {produzione.metri_quadri:.0f} m²")
            print(f"    Produzione: {produzione.quantita_prodotta_kg:.1f} kg")
            print(f"    Efficienza produttiva: {produzione.efficienza_produttiva*100:.1f}%")
            print(f"    Qualita finale: {produzione.qualita_finale*100:.0f}%")
            print(f"    Giorni: {produzione.giorni_necessari}")
            print(f"    Condizioni: {produzione.variabili}")
        
        # restituiamo una tupla con i dati
        return produzioni, self._calcola_statistiche(produzioni, data_inizio)
    
    def _calcola_statistiche(self, produzioni: List[Produzione], 
                            data_inizio: datetime) -> Dict:
        """
        Qui facciamo un po' il punto della situazione facendo qualche confronto
        per vedere in generale come è andata la stagione di coltivazione dell'azienda
        agricola teorica che viene simulata. Calcoliamo i tempi più lunghi, il
        totale prodotto e delle medie.
        """
        
        # Troviamo la data più lontana di fine di tutti gli ortaggi coltivati
        data_fine_totale = max(p.data_fine for p in produzioni)
        
        # Calcoliamo il totale dei giorni della stazione facendo la differenza tra la data di fine
        # piu lontana e la data di inizio (comune) a tuttle coltivazioni simulate.
        giorni_totali = (data_fine_totale - data_inizio).days
        
        # Sommiamo tutte le produzioni in kilogrammi
        produzione_totale_kg = sum(p.quantita_prodotta_kg for p in produzioni)
        
        # Sommiamo il totale dei metri quadrati utilizzati
        area_totale_m2 = sum(p.metri_quadri for p in produzioni)
        
        # Calcoliamo un KPI di efficienza e qualità globali facendo la media matematica dei KPI singoli
        efficienza_media = sum(p.efficienza_produttiva for p in produzioni) / len(produzioni)
        qualita_media = sum(p.qualita_finale for p in produzioni) / len(produzioni)
        
        # Mandiamo in output un dizionare con queste statistiche globali
        return {
            'giorni_totali': giorni_totali,
            'data_inizio': data_inizio,
            'data_fine': data_fine_totale,
            'produzione_totale_kg': produzione_totale_kg,
            'area_totale_m2': area_totale_m2,
            'efficienza_media': efficienza_media,
            'qualita_media': qualita_media,
            # Calcoliamo una resa media avendo il totale prodotto e quanto terreno è stato impiegato
            # teniamo conto di un possibile div by zero e intercettiamolo
            'resa_media_per_m2': produzione_totale_kg / area_totale_m2 if area_totale_m2 > 0 else 0
        }
    
    def stampa_report(self, statistiche: Dict):
        # Stampiamo un report dei dati aggregati.

        print("\n" + "-"*80)
        print(f"REPORT FINALE")
        print("-"*80)
        
        # Info sulle date con formattazione della data in formato italiano
        print(f"Periodo: {statistiche['data_inizio'].strftime('%d/%m/%Y')} - "
              f"{statistiche['data_fine'].strftime('%d/%m/%Y')}")
        print(f"Durata totale: {statistiche['giorni_totali']} giorni")
        print()
        
        # Dati produttivi
        print(f"Area coltivata totale:      {statistiche['area_totale_m2']:,.0f} m²")
        print(f"Produzione totale:          {statistiche['produzione_totale_kg']:,.1f} kg")
        print(f"Resa media:                 {statistiche['resa_media_per_m2']:.2f} kg/m²")
        print()
        
        # KPI
        print(f"Efficienza produttiva media: {statistiche['efficienza_media']*100:.1f}%")
        print(f"Qualita media:              {statistiche['qualita_media']*100:.0f}%")
        
        print("-"*80)
