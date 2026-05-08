# Esercizio 1 — Contatore messaggi UDP

## Cosa chiedeva l'esercizio

Estendere il server UDP per tenere un conteggio dei PING ricevuti.
Ogni risposta PONG deve includere quel conteggio, ad esempio `"PONG #3"`.
Aggiornare il client per stampare la stringa di risposta completa.

---

## Modifica principale: la variabile contatore

Ho aggiunto `contatore_ping = 0` prima del loop in `servi_sempre()`.
Ogni volta che arriva un PING, la incremento di 1 e la passo a
`scegli_risposta()`, che costruisce la risposta con il numero incluso:

```python
contatore_ping = 0   # parte da 0 prima del loop

while True:
    ...
    if messaggio == "PING":
        contatore_ping = contatore_ping + 1
    risposta = scegli_risposta(messaggio, contatore_ping)
    # risposta sarà: "PONG #1", "PONG #2", "PONG #3" ...
```

---

## Risposte alle domande dell'esercizio

### Dove si trova la variabile contatore?

La variabile `contatore_ping` è dichiarata all'interno della funzione
`servi_sempre()`, appena prima del loop `while True`.
Vive nella **memoria RAM del processo Python** del server.

### Cosa succede al contatore se si riavvia il server mentre il client è ancora in esecuzione?

Se il server viene riavviato, `contatore_ping` viene ricreata da zero
perché Python cancella tutte le variabili locali quando un programma si
chiude. La RAM usata dal processo viene liberata dal sistema operativo.

Questo significa che il client vedrà improvvisamente la risposta tornare
a `"PONG #1"` anche se era arrivato a `"PONG #5"`, perché il nuovo server
non sa nulla di quello che era successo prima.

Per rendere il contatore persistente tra i riavvii bisognerebbe salvarlo
su un file o un database — ma va oltre lo scopo di questo esercizio.

---

## Modifica al client

Non erano necessarie modifiche strutturali: il client stampava già la
risposta completa. Ho aggiunto un commento per chiarire che l'output
mostra ora il numero del contatore.

**Esempio di output:**
[Client] Risposta: 'PONG #1'
[Client] Risposta: 'PONG #2'
[Client] Risposta: 'PONG #3'

---

## File modificati

| File | Modifiche |
|---|---|
| `udp_server.py` | Aggiunta variabile `contatore_ping`, incremento, risposta con numero |
| `udp_client.py` | Aggiunto commento sulla stampa della risposta completa |

---

## Come eseguire

```bash
# Terminale 1
python exercise_1/udp_server.py

# Terminale 2
python exercise_1/udp_client.py
```