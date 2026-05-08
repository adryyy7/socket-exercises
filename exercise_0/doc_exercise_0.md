# Esercizio 0 — Refactoring con le funzioni

## Cosa chiedeva l'esercizio

Modificare il codice proposto usando le funzioni il più possibile.
Ottimizzare il codice spiegando la logica di ogni modifica.

---

## Problema del codice originale

Nel codice originale tutta la logica era dentro un'unica funzione `main()`
di oltre 80 righe. Funzionava, ma presentava due problemi:

1. **Difficile da leggere**: per capire cosa fa una singola parte bisogna
   scorrere tutta la funzione.
2. **Difficile da modificare**: cambiare la logica delle risposte significava
   toccare lo stesso blocco dove c'è il codice di rete.

---

## Modifiche apportate e perché

### 1. Suddivisione in funzioni con un compito solo

Ho diviso ogni file in funzioni piccole:

| Funzione | Compito |
|---|---|
| `crea_socket_server()` | Crea e configura il socket |
| `aspetta_client()` | Aspetta che un client si connetta |
| `scegli_risposta()` | Decide cosa rispondere |
| `gestisci_client()` | Gestisce il loop di comunicazione |
| `avvia()` | Chiama tutto nell'ordine giusto |

**Vantaggio concreto**: se voglio cambiare le risposte del server,
tocco solo `scegli_risposta()`. Se voglio cambiare come si crea il socket,
tocco solo `crea_socket_server()`. Le funzioni non si influenzano.

### 2. Blocco try/finally per la chiusura del socket

**Codice originale:**
```python
conn.close()
server_sock.close()
```
Se si verificava un errore prima di queste righe, i socket
non venivano mai chiusi. Il sistema operativo teneva la porta
occupata anche dopo la fine del programma (resource leak).

**Codice nuovo:**
```python
try:
    conn, indirizzo = aspetta_client(server_sock)
    gestisci_client(conn)
finally:
    server_sock.close()  # eseguito SEMPRE, anche in caso di errore
```

Il blocco `finally` garantisce la chiusura in ogni situazione.

### 3. Funzione separata per la logica delle risposte

**Prima (tutto dentro il loop):**
```python
if message == "PING":
    reply = "PONG"
else:
    reply = f"Unknown message: {message!r}"
```

**Dopo:**
```python
def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return "ERROR: messaggio sconosciuto"
```

Separare la logica del protocollo dal codice di rete è una buona
pratica: se il protocollo cambia, non tocco il codice di rete.

---

## Riepilogo modifiche per file

| File | Modifiche |
|---|---|
| `tcp_server.py` | 4 funzioni + try/finally |
| `tcp_client.py` | 3 funzioni + try/finally |
| `udp_server.py` | 3 funzioni + try/finally |
| `udp_client.py` | 3 funzioni + try/finally |

---

## Come eseguire

```bash
# Terminale 1
python exercise_0/tcp_server.py

# Terminale 2
python exercise_0/tcp_client.py
```