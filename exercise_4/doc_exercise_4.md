# Esercizio 4 - Protocollo Custom: Lista della Spesa TCP

## Cosa chiedeva l'esercizio

Scegliere una qualsiasi interazione reale tra due parti e implementarla
come programma socket. Prima di scrivere il codice rispondere a quattro
domande sul protocollo in un blocco commenti in cima ad ogni file.

## La mia scelta: una lista della spesa condivisa

Il client puo' aggiungere prodotti, rimuoverli e vedere la lista completa.
Il server mantiene la lista in memoria e risponde ad ogni comando.

Ho scelto questa idea perché è un caso d'uso reale e quotidiano:
applicazioni come promemoria condivisi funzionano
esattamente in questo modo, un client manda comandi a un server che mantiene
lo stato aggiornato.

## Risposte alle domande del protocollo

### 1. TCP o UDP, e perché?

Ho scelto TCP.

Ogni comando modifica lo stato della lista sul server e il client deve
sempre ricevere una conferma. Con UDP un pacchetto potrebbe perdersi
silenziosamente: il client penserebbe di aver aggiunto "latte" ma il
server non avrebbe mai ricevuto il comando. L'utente si troverebbe con
una lista sbagliata senza saperlo.

TCP garantisce che ogni comando venga consegnato nell'ordine corretto
e che ogni risposta torni al client.

### 2. Formato esatto dei messaggi

Ho scelto il testo semplice (plain text).

| Direzione | Messaggio | Significato |
|---|---|---|
| Client > Server | AGGIUNGI latte | Aggiunge latte alla lista |
| Server > Client | OK: 'latte' aggiunto alla lista | Conferma |
| Client > Server | RIMUOVI latte | Rimuove latte dalla lista |
| Server > Client | OK: 'latte' rimosso dalla lista | Conferma |
| Client > Server | MOSTRA | Richiede la lista completa |
| Server > Client | Lista: latte, pane, uova | Lista attuale |
| Client > Server | MOSTRA (lista vuota) | Richiede la lista |
| Server > Client | Lista vuota | Nessun prodotto presente |
| Client > Server | ciao | Comando non valido |
| Server > Client | ERRORE: comando non riconosciuto... | Errore formato |
| Client > Server | QUIT | Fine sessione |
| Server > Client | CIAO | Conferma chiusura |

### 3. Cosa succede con un messaggio non valido?

La funzione elabora_comando() controlla la prima parola del messaggio.
Se non è AGGIUNGI, RIMUOVI, MOSTRA o QUIT, il server risponde:
ERRORE: comando non riconosciuto. Usa: AGGIUNGI, RIMUOVI, MOSTRA, QUIT

La sessione continua normalmente. Il server non crasha mai.

Vengono gestiti anche i casi in cui manca il nome del prodotto:
AGGIUNGI ->  ERRORE: specifica il prodotto. Esempio: AGGIUNGI latte
RIMUOVI ->  ERRORE: specifica il prodotto. Esempio: RIMUOVI latte
RIMUOVI patate ->  ERRORE: 'patate' non è nella lista

### 4. Condizione di terminazione, e chi la inizia?

Il client invia "QUIT". Il server risponde "CIAO" e chiude la connessione
con quel client. Il server rimane poi in ascolto per altri client.
E' sempre il client a iniziare la terminazione, il server non forza mai
la disconnessione.

## Dove viene salvata la lista?

La lista è una variabile Python di tipo list dichiarata dentro
gestisci_client(). Questo significa:

- La lista persiste per tutta la durata della connessione di un client.
- Se il client si disconnette e si riconnette, la lista riparte vuota.
- Se si volesse che la lista sopravviva tra una connessione e l'altra,
  bisognerebbe spostarla fuori dalla funzione o salvarla su un file.

## Esempio di sessione completa
[Client] > AGGIUNGI latte
[Client] OK: 'latte' aggiunto alla lista
[Client] > AGGIUNGI pane
[Client] OK: 'pane' aggiunto alla lista
[Client] > MOSTRA
[Client] Lista: latte, pane
[Client] > RIMUOVI pane
[Client] OK: 'pane' rimosso dalla lista
[Client] > RIMUOVI patate
[Client] ERRORE: 'patate' non è nella lista
[Client] > ciao
[Client] ERRORE: comando non riconosciuto. Usa: AGGIUNGI, RIMUOVI, MOSTRA, QUIT
[Client] > QUIT
[Client] CIAO

## File creati

| File | Descrizione |
|---|---|
| spesa_server.py | Server TCP che gestisce la lista in memoria |
| spesa_client.py | Client TCP con input interattivo |

## Come eseguire

```bash
python exercise_4/spesa_server.py   # Terminale 1
python exercise_4/spesa_client.py   # Terminale 2
```