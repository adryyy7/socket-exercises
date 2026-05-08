exercise_0/doc_exercise_0.mdmarkdown# Esercizio 0 - Riscrittura del codice con le funzioni

## Cosa chiedeva l'esercizio

Modificare il codice proposto usando le funzioni il piu' possibile.
Ottimizzare il codice spiegando la logica di ogni modifica.

## Problema del codice originale

Nel codice originale tutta la logica era concentrata dentro un'unica
funzione main() di oltre 80 righe. Questo approccio funziona, ma presenta
due problemi concreti:

- E' difficile da leggere: per capire cosa fa una singola parte bisogna
  scorrere tutta la funzione.
- E' difficile da modificare: cambiare la logica delle risposte significa
  toccare lo stesso blocco dove si trova il codice di rete.

## Modifiche apportate e motivazione

### 1. Suddivisione in funzioni con un compito solo

Ho diviso ogni file in funzioni piccole, ognuna con una responsabilita'
precisa:

| Funzione | Compito |
|---|---|
| crea_socket_server() | Crea e configura il socket |
| aspetta_client() | Aspetta che un client si connetta |
| scegli_risposta() | Decide cosa rispondere |
| gestisci_client() | Gestisce il loop di comunicazione |
| avvia() | Chiama tutto nell'ordine giusto |

Il vantaggio concreto e' che se voglio cambiare le risposte del server
tocco solo scegli_risposta(). Se voglio cambiare come si crea il socket
tocco solo crea_socket_server(). Le funzioni non si influenzano.

### 2. Aggiunta del blocco try/finally

Codice originale:
```pythonconn.close()
server_sock.close()
Se si verificava un errore prima di queste righe, i socket non venivano
mai chiusi. Il sistema operativo teneva la porta occupata anche dopo
la fine del programma. Questo si chiama resource leak.

Codice nuovo:
```pythontry:
conn, indirizzo = aspetta_client(server_sock)
gestisci_client(conn)
finally:
server_sock.close()
Il blocco finally garantisce che server_sock.close() venga chiamato
sempre, anche se si verifica un errore.

### 3. Funzione separata per la logica delle risposte

Codice originale (dentro il loop):
```pythonif message == "PING":
reply = "PONG"
else:
reply = f"Unknown message: {message!r}"

Codice nuovo:
```pythondef scegli_risposta(messaggio):
if messaggio == "PING":
return "PONG"
else:
return f"Messaggio sconosciuto: {messaggio!r}"
Separare la logica del protocollo dal codice di rete e' una buona
pratica: se il protocollo cambia, non tocco il codice di rete.

## Riepilogo modifiche per file

| File | Modifiche |
|---|---|
| tcp_server.py | 4 funzioni + try/finally |
| tcp_client.py | 3 funzioni + try/finally |
| udp_server.py | 3 funzioni + try/finally |
| udp_client.py | 3 funzioni + try/finally |

## Come eseguire

```bash
python exercise_0/tcp_server.py   # Terminale 1
python exercise_0/tcp_client.py   # Terminale 2
```