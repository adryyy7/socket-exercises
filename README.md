# Esercizi di Programmazione Socket - Python TCP & UDP

Soluzioni agli esercizi di programmazione socket basati sul repository
[IsidurPaine/Socket](https://github.com/IsidurPaine/Socket).

**Autore:** Adriano Mizzi

---

## Struttura della repository

| Cartella | Contenuto |
|---|---|
| `original_code/` | File originali del repository di base, non modificati |
| `exercise_0/` | Refactoring: tutti e quattro i file riscritti con le funzioni |
| `exercise_1/` | Server UDP esteso con contatore messaggi |
| `exercise_2/` | Server TCP modificato per gestire più client |
| `exercise_3/` | Server UDP con simulazione perdita pacchetti |
| `exercise_4/` | Protocollo custom: lista della spesa condivisa via TCP |

---

## Diagrammi

Il repository originale include dei diagrammi che spiegano visivamente
come funzionano TCP e UDP internamente. Sono mantenuti in `original_code/`
insieme ai file sorgente originali e rimangono utili come riferimento
mentre si leggono le soluzioni degli esercizi.

Il diagramma del flusso TCP mostra la sequenza completa da `bind()`
attraverso `accept()` fino alla chiusura con `close()` e FIN teardown.
Il diagramma UDP evidenzia l'assenza dell'handshake e illustra perché
`recvfrom()` deve restituire l'indirizzo del mittente. Il diagramma
comparativo TCP vs UDP mette entrambi i modelli sulla stessa tavola
in modo che le differenze strutturali siano immediatamente visibili.

Usa i diagrammi come riferimento mentre studi il codice, non come
sostituto della lettura di esso. Ogni dettaglio mostrato visivamente
ha una riga corrispondente nel codice sorgente con un commento
che lo spiega.

---

## File

| File | Protocollo | Ruolo |
|---|---|---|
| `exercise_0/tcp_server.py` | TCP | Server originale riscritto con le funzioni |
| `exercise_0/tcp_client.py` | TCP | Client originale riscritto con le funzioni |
| `exercise_0/udp_server.py` | UDP | Server originale riscritto con le funzioni |
| `exercise_0/udp_client.py` | UDP | Client originale riscritto con le funzioni |
| `exercise_1/udp_server.py` | UDP | Server con contatore PING - risponde `PONG #N` |
| `exercise_1/udp_client.py` | UDP | Client che stampa la stringa di risposta completa |
| `exercise_2/tcp_server.py` | TCP | Server che accetta più client in sequenza |
| `exercise_3/udp_server.py` | UDP | Server che scarta casualmente le risposte |
| `exercise_3/udp_client.py` | UDP | Client che gestisce i timeout senza crashare |
| `exercise_4/spesa_server.py` | TCP | Server lista della spesa: AGGIUNGI, RIMUOVI, MOSTRA |
| `exercise_4/spesa_client.py` | TCP | Client interattivo per la lista della spesa |

---

## Requisiti

- Python 3.6 o superiore
- Nessun pacchetto esterno — solo la libreria standard (`socket`, `time`, `random`, `threading`)

---

## Come eseguire

Ogni esercizio richiede **due terminali aperti contemporaneamente**: uno
per il server e uno per il client. Avviare sempre prima il server.

### Exercise 0 — TCP
```bash
# Terminale 1
python exercise_0/tcp_server.py

# Terminale 2
python exercise_0/tcp_client.py
```

### Exercise 0 — UDP
```bash
# Terminale 1
python exercise_0/udp_server.py

# Terminale 2
python exercise_0/udp_client.py
```

### Exercise 1
```bash
# Terminale 1
python exercise_1/udp_server.py

# Terminale 2
python exercise_1/udp_client.py
```

### Exercise 2
```bash
# Terminale 1
python exercise_2/tcp_server.py

# Terminale 2 — usa il client dell'esercizio 0
python exercise_0/tcp_client.py
```
Il server accetta fino a 5 client in sequenza. Avvia più volte il client
in terminali separati per testare il comportamento multi-client.

### Exercise 3
```bash
# Terminale 1
python exercise_3/udp_server.py

# Terminale 2
python exercise_3/udp_client.py
```
Il server scarta circa il 30% delle risposte. Osserva come il meccanismo
di timeout del client diventa essenziale una volta introdotta la perdita
di pacchetti.

### Exercise 4
```bash
# Terminale 1
python exercise_4/spesa_server.py

# Terminale 2
python exercise_4/spesa_client.py
```

---

## TCP vs UDP — differenze principali

Questa tabella riassume ciò che il codice rende concreto.

| | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|---|---|---|
| Connessione | Three-way handshake obbligatorio | Nessuna — fire and forget |
| Setup server | `bind` -> `listen` → `accept` | Solo `bind` |
| Setup client | `connect` | Nessuno |
| Invio | `sendall(data)` | `sendto(data, indirizzo)` |
| Ricezione | `recv(n)` | `recvfrom(n)` → restituisce dati + indirizzo mittente |
| Garanzia consegna | Sì - TCP ritrasmette i pacchetti persi | No - i datagrammi possono perdersi o arrivare fuori ordine |
| Chiusura | `close()` invia FIN/ACK | `close()` rilascia solo il file descriptor locale |
| Casi d'uso tipici | HTTP, SSH, database | DNS, streaming video, giochi online |

### Perché `recvfrom` invece di `recv`?

In UDP non esiste una connessione persistente, quindi il socket non
ricorda chi ha inviato l'ultimo datagramma. `recvfrom()` risolve questo
problema restituendo l'indirizzo del mittente insieme ai dati. Il server
passa poi quell'indirizzo a `sendto()` per sapere dove inviare la risposta.

### Perché `settimeout` nel client UDP?

TCP garantisce la consegna, quindi `recv()` ritorna solo quando i dati
sono arrivati. UDP non offre questa garanzia: un datagramma può perdersi
silenziosamente. Senza un timeout, `recvfrom()` si bloccherebbe per sempre
se il server non è raggiungibile o il pacchetto viene scartato. Il timeout
di due secondi trasforma un blocco infinito in un'eccezione gestibile
`socket.timeout`.

---

## Documentazione tecnica

Ogni cartella contiene un documento tecnico in italiano che spiega
nel dettaglio tutte le modifiche apportate al codice:

| File | Contenuto |
|---|---|
| `exercise_0/doc_exercise_0.md` | Spiegazione del refactoring con le funzioni |
| `exercise_1/doc_exercise_1.md` | Spiegazione del contatore e risposta alle domande dell'esercizio |
| `exercise_2/doc_exercise_2.md` | Spiegazione del loop multi-client e del bonus threading |
| `exercise_3/doc_exercise_3.md` | Spiegazione della simulazione perdita pacchetti |
| `exercise_4/doc_exercise_4.md` | Descrizione del protocollo custom progettato da zero |