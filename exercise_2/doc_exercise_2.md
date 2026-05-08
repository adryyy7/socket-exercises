# Esercizio 2 - Server TCP Multi-client

## Cosa chiedeva l'esercizio

Modificare il server TCP in modo che possa servire più client uno dopo
l'altro (sequenziale, non parallelo): dopo che un client si disconnette,
il server deve tornare a chiamare accept() e aspettare il prossimo.
Aggiungere un flag server_running o un numero massimo di client in modo
che il server abbia un modo pulito per fermarsi.

## Il problema del server originale

Il server originale gestiva esattamente un client e poi usciva, perché
accept() veniva chiamato una sola volta fuori da qualsiasi loop:

```python
conn, addr = server_sock.accept()   
gestisci_client(conn)
server_sock.close()           
```

## La mia soluzione: loop con flag e MAX_CLIENTS

Ho messo la chiamata ad accept() dentro un loop while controllato da
due meccanismi di stop:

```python
server_running = True
MAX_CLIENTS = 5

while server_running and clients_serviti < MAX_CLIENTS:
    conn, indirizzo = server_sock.accept()
    clients_serviti = clients_serviti + 1
    gestisci_client(conn, indirizzo)
    # il loop torna automaticamente ad accept()
```

Avere due meccanismi è utile:
- server_running permette di fermare il server dall'esterno in futuro
- MAX_CLIENTS garantisce comunque un limite massimo come sicurezza

## Bonus threading

Senza threading, se il client A è connesso, il client B deve aspettare
che A si disconnetta prima di potersi connettere. Il flusso è:
accept() -> gestisci A -> A si disconnette -> accept() -> gestisci B

Con threading ogni client viene smistato su un thread separato e
il thread principale torna subito ad accept():

```python
t = threading.Thread(target=gestisci_client, args=(conn, indirizzo))
t.daemon = True
t.start()
# il thread principale torna subito ad accept() senza aspettare
```

Il flusso diventa:
accept() -> avvia Thread A -> accept() -> avvia Thread B -> accept()
Thread A gestisce A          Thread B gestisce B

daemon = True significa che se il programma principale si ferma,
tutti i thread vengono terminati automaticamente. Senza di esso
il programma resterebbe aperto finché tutti i thread non finiscono.

## File modificati

| File | Modifiche |
|---|---|
| tcp_server.py | Loop while, flag server_running, MAX_CLIENTS, bonus threading commentato |

## Come eseguire

```bash
python exercise_2/tcp_server.py        # Terminale 1
python exercise_0/tcp_client.py        # Terminale 2
# Aprire altri terminali per testare piu' client in sequenza
```