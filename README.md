# Socket Exercises — Python TCP & UDP

Esercizi di programmazione socket in Python, basati sul repository
[IsidurPaine/Socket](https://github.com/IsidurPaine/Socket).

**Autore:** Adriano Mizzi  

---

## Struttura della repository
socket-exercises/
│
├── README.md
│
├── original_code/
│   ├── tcp_server.py
│   ├── tcp_client.py
│   ├── udp_server.py
│   └── udp_client.py
│
├── exercise_0/
│   ├── tcp_server.py
│   ├── tcp_client.py
│   ├── udp_server.py
│   ├── udp_client.py
│   └── doc_exercise_0.md
│
├── exercise_1/
│   ├── udp_server.py
│   ├── udp_client.py
│   └── doc_exercise_1.md
│
├── exercise_2/
│   ├── tcp_server.py
│   └── doc_exercise_2.md
│
├── exercise_3/
│   ├── udp_server.py
│   ├── udp_client.py
│   └── doc_exercise_3.md
│
└── exercise_4/
├── spesa_server.py
├── spesa_client.py
└── doc_exercise_4.md

---

## Descrizione degli esercizi

### Exercise 0 — Refactoring con le funzioni
Il codice originale è stato riscritto suddividendo la logica in funzioni
con un compito solo ciascuna. Sono stati modificati tutti e quattro i file
originali (TCP server, TCP client, UDP server, UDP client).
Ogni modifica è spiegata nel documento tecnico.

### Exercise 1 — Contatore messaggi UDP
Il server UDP è stato esteso per tenere un conteggio di quanti PING ha
ricevuto. Ogni risposta PONG include il numero, ad esempio `"PONG #3"`.
Il client stampa la stringa di risposta completa per rendere il contatore
visibile.

### Exercise 2 — Server TCP multi-client
Il server TCP è stato modificato per servire più client uno dopo l'altro
(versione sequenziale). Usa un flag `server_running` e una costante
`MAX_CLIENTS` per fermarsi in modo pulito.
Come bonus, il codice per gestire più client contemporaneamente con
`threading` è incluso nel file come commento, pronto da attivare.

### Exercise 3 — Simulazione canale inaffidabile
Il server UDP simula la perdita di pacchetti tramite la costante
`DROP_PROBABILITY`. Prima di ogni risposta viene estratto un numero
casuale: se è sotto la soglia, la risposta viene scartata e viene
stampato `"[Server] Dropped reply (simulated loss)"`.
Il client gestisce il timeout senza crashare e mostra le statistiche
finali di pacchetti ricevuti e persi.

### Exercise 4 — Protocollo custom: lista della spesa
Implementazione di una lista della spesa condivisa via socket TCP.
Il client può inviare tre comandi: `AGGIUNGI <prodotto>`, `RIMUOVI <prodotto>`
e `MOSTRA`. Il server mantiene la lista in memoria e risponde ad ogni
comando con una conferma o un messaggio di errore.

---

## Come eseguire

Ogni esercizio richiede **due terminali aperti contemporaneamente**.
Avviare sempre prima il server.

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

# Apri altri terminali per testare più client in sequenza
```

### Exercise 3
```bash
# Terminale 1
python exercise_3/udp_server.py

# Terminale 2
python exercise_3/udp_client.py
```

### Exercise 4
```bash
# Terminale 1
python exercise_4/spesa_server.py

# Terminale 2
python exercise_4/spesa_client.py
```

---

## Comandi disponibili — Exercise 4

| Comando | Esempio | Effetto |
|---|---|---|
| `AGGIUNGI <prodotto>` | `AGGIUNGI latte` | Aggiunge il prodotto alla lista |
| `RIMUOVI <prodotto>` | `RIMUOVI latte` | Rimuove il prodotto dalla lista |
| `MOSTRA` | `MOSTRA` | Mostra tutti i prodotti nella lista |
| `QUIT` | `QUIT` | Chiude la connessione |

---

## Requisiti

- Python 3.6 o superiore
- Nessun pacchetto esterno (solo libreria standard)

---

## Riferimenti

- Repository originale: [IsidurPaine/Socket](https://github.com/IsidurPaine/Socket)
- Documentazione Python socket: [docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)