# Esercizio 2 — Server TCP Multi-client

## Cosa chiedeva l'esercizio

Modificare il server TCP affinché possa servire più client uno dopo l'altro
(sequenziale, non parallelo): dopo che un client si disconnette, il server
deve tornare a chiamare `accept()` e aspettare il prossimo.
Aggiungere un flag `server_running` o un numero massimo di client in modo
che il server abbia un modo pulito per fermarsi.

Bonus: usare il modulo `threading` per gestire più client contemporaneamente.

---

## Il problema del server originale

Il server originale gestiva esattamente un client e poi usciva,
perché `accept()` veniva chiamato una sola volta fuori da qualsiasi loop:

```python
# Codice originale (semplificato)
conn, addr = server_sock.accept()   # chiamato una volta sola
gestisci_client(conn)
server_sock.close()                 # il server esce
```

---

## Soluzione: loop con flag server_running e MAX_CLIENTS

Ho aggiunto due meccanismi di controllo:

```python
server_running = True   # flag: diventa False per fermare il server
MAX_CLIENTS = 5         # numero massimo di client

while server_running and clients_serviti < MAX_CLIENTS:
    conn, indirizzo = server_sock.accept()   # aspetta il prossimo client
    clients_serviti = clients_serviti + 1
    gestisci_client(conn, indirizzo)         # serve questo client
    # il loop torna automaticamente ad accept()
```

Il server si ferma in modo pulito quando accade una delle due cose:
- `server_running` diventa `False`
- Il numero di client serviti raggiunge `MAX_CLIENTS`

Avere due meccanismi è utile: `server_running` permette di fermare il
server dall'esterno (ad esempio da un altro thread o da un segnale),
mentre `MAX_CLIENTS` garantisce comunque un limite massimo.

---

## Bonus: threading per client simultanei

Senza threading (versione sequenziale), se il client A è connesso,
il client B deve aspettare che A si disconnetta. Il flusso è:
accept() → gestisci A → A si disconnette → accept() → gestisci B → ...

Con `threading`, ogni client viene smistato su un thread separato,
e il thread principale torna subito ad `accept()`:

```python
t = threading.Thread(target=gestisci_client, args=(conn, indirizzo))
t.daemon = True   # il thread si chiude automaticamente col programma
t.start()
# il main thread torna subito ad accept() senza aspettare
```

Il flusso diventa:
accept() → avvia Thread A → accept() → avvia Thread B → accept() → ...
Thread A gestisce A          Thread B gestisce B

**Cos'è `daemon = True`?**
Se il programma principale finisce mentre ci sono thread attivi,
con `daemon = True` quei thread vengono terminati automaticamente.
Senza di esso, il programma resterebbe aperto finché tutti i thread
non completano il loro lavoro.

Il codice per il threading è presente nel file come commento,
pronto per essere attivato.

---

## Confronto tra le due versioni

| Caratteristica | Sequenziale | Con threading |
|---|---|---|
| Client contemporanei | No, uno alla volta | Sì |
| Complessità | Semplice | Maggiore |
| Rischio conflitti dati condivisi | Nessuno | Possibile |
| Uso tipico | Pochi client, semplice | Molti client, server reale |

---

## File modificati

| File | Modifiche |
|---|---|
| `tcp_server.py` | Loop `while`, flag `server_running`, `MAX_CLIENTS`, bonus threading commentato |

---

## Come eseguire

```bash
# Terminale 1
python exercise_2/tcp_server.py

# Terminale 2 (ripeti per testare più client in sequenza)
python exercise_0/tcp_client.py
```