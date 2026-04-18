"""
Entry point principale per permettere all'utente di eseguire
la simulazione.
Questo modulo coordina l'esecuzione del programma gestendone il flusso.
"""

from datetime import datetime
from simulatore import SimulatoreFattoria


def main():

    print("="*80)
    print("SIMULAZIONE PRODUZIONE DI ORTAGGI")
    print("="*80)
    print("\nQuesto programma simula la coltivazione simultanea di 3 tipi di ortaggi:")
    print("  - Pomodoro San Marzano - Ortaggio da sugo")
    print("  - Melanzana Violetta di Firenze - Ortaggio toscano per parmigiane")
    print("  - Zucchina Romanesco - Ortaggio romano")
    print("\nVariabili ambientali considerati nel calcolo della produzione:")
    print("  - Qualita del suolo")
    print("  - Livello di irrigazione")
    print("  - Temperatura media")
    print("  - Umidita")
    print("  - Uso di fertilizzanti")
    print()

    # Qui creiamo un'istanza del SimulatoreFattoria, che è la classe principale
    simulatore = SimulatoreFattoria()

    # Qui richiamiamo il modulo orchestratore Simulatore
    print("\n>> Generazione condizioni di coltivazione casuali...")
    produzioni = simulatore.genera_produzioni_casuali()

    # Qui definiamo la data di inizio teorica, il 1 aprile per considerare 
    # la primavera come inizio della stagione.
    data_inizio = datetime(2026, 4, 1)

    # Qui eseguiamo la simulazione vera e propria con tutti i calcoli
    _, statistiche = simulatore.simula_produzione(produzioni, data_inizio)

    # Qui stampiamo il report finale con tutti i risultati
    simulatore.stampa_report(statistiche)

    # Messaggio finale per indicare la fine del prog
    print("\n*** Simulazione completata con successo! ***\n")


if __name__ == "__main__":
    main()