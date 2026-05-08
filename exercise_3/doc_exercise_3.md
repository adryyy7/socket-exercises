# Esercizio 3 — Simulazione Canale Inaffidabile

## Cosa chiedeva l'esercizio

Simulare una rete inaffidabile aggiungendo `DROP_PROBABILITY` al server UDP.
Prima di ogni PONG, estrarre un numero casuale: se è sotto `DROP_PROBABILITY`,
non inviare la risposta e stampare `"[Server] Dropped reply (simulated loss)"`.
Sul client, gestire il timeout in modo che stampi un messaggio utile e
continui al ping successivo senza crashare.

---

## Modifiche al server

### La costante DROP_PROBABILITY

```python
DROP_PROBABILITY = 0.3  # 30% di probabilità di perdita
```

### Il controllo prima di sendto()

```python
if random.random() < DROP_PROBABILITY:
    print("[Server] Dropped reply (simulated loss)")
    # sendto() non viene chiamato: il client non riceve risposta
else:
    sock.sendto(risposta.encode("utf-8"), indirizzo_client)
```

**Come funziona `random.random()`?**
Genera un numero decimale casuale tra 0.0 e 1.0 con distribuzione uniforme.
Ogni chiamata dà un numero diverso e indipendente. Se `DROP_PROBABILITY`
è 0.3, circa il 30% dei numeri generati sarà inferiore a 0.3 — quindi
circa il 30% delle risposte viene scartato.

---

## Modifiche al client

### Perché il timeout diventa fondamentale

Su `localhost` i pacchetti UDP non si perdono quasi mai.
La simulazione li forza a perdersi artificialmente.

**Senza `settimeout()`:**
[Client] Invio ping #3
il programma si blocca qui per sempre in attesa di una risposta che non arriverà

**Con `settimeout(2.0)` e gestione dell'eccezione:**
```python
except socket.timeout:
    print(f"[Client] Timeout — nessuna risposta per il ping #{numero}")
    persi = persi + 1
    # il loop continua normalmente al ping successivo
```

Il timeout trasforma un blocco infinito in un'eccezione gestibile.
Il client non crasha mai, anche con perdite continue.

### Riepilogo finale

Ho aggiunto i contatori `ricevuti` e `persi` per mostrare le statistiche:
[Client] Risultati: 7 ricevuti, 3 persi su 10 ping

---

## File modificati

| File | Modifiche |
|---|---|
| `udp_server.py` | `DROP_PROBABILITY`, `import random`, controllo drop con log esatto |
| `udp_client.py` | Gestione timeout con messaggio chiaro, contatori, riepilogo finale |

---

## Come eseguire

```bash
# Terminale 1
python exercise_3/udp_server.py

# Terminale 2
python exercise_3/udp_client.py
```

Prova a cambiare `DROP_PROBABILITY` a `0.0` (zero perdite) o `0.9`
(90% perdite) e osserva come cambia l'output del client.