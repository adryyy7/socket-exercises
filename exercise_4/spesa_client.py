"""
Lista della Spesa Client — TCP
Exercise 4

=== Risposte alle domande del protocollo ===

PROTOCOLLO SCELTO: TCP
Motivo: ogni comando modifica una lista sul server e il client deve
sempre ricevere una conferma dell'operazione. Con UDP un comando
potrebbe perdersi silenziosamente e il client non saprebbe se il
prodotto è stato aggiunto o no. TCP garantisce la consegna.

FORMATO DEI MESSAGGI: testo semplice (plain text)
  Client → Server:  "AGGIUNGI latte"  → aggiunge latte
  Client → Server:  "RIMUOVI latte"   → rimuove latte
  Client → Server:  "MOSTRA"          → mostra la lista
  Client → Server:  "QUIT"            → chiude la connessione

MESSAGGIO NON VALIDO: se il comando non è riconosciuto, il server
risponde con un messaggio di errore e la sessione continua normalmente.

TERMINAZIONE: il client invia "QUIT". Il server risponde "CIAO" e
chiude la connessione. È sempre il client a iniziare la terminazione.

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket

HOST = "127.0.0.1"
PORT = 65436


def crea_socket_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[Client] Connesso al server lista della spesa su {HOST}:{PORT}")
    print("[Client] Comandi disponibili:")
    print("         AGGIUNGI <prodotto>  — aggiunge un prodotto")
    print("         RIMUOVI <prodotto>   — rimuove un prodotto")
    print("         MOSTRA               — mostra tutta la lista")
    print("         QUIT                 — esci\n")
    return sock


def avvia():
    sock = crea_socket_client()

    try:
        while True:
            comando = input("[Client] > ").strip()

            if not comando:
                continue

            sock.sendall(comando.encode("utf-8"))

            dati = sock.recv(1024)

            if not dati:
                print("[Client] Il server ha chiuso la connessione.")
                break

            risposta = dati.decode("utf-8")
            print(f"[Client] {risposta}\n")

            if comando.upper() == "QUIT":
                break

    finally:
        sock.close()
        print("[Client] Disconnesso.")


if __name__ == "__main__":
    avvia()