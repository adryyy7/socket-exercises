"""
UDP Client - Ping Pong con contatore messaggi (Esercizio 1)

Aggiorna il client dell'esercizio 0 per stampare la stringa di risposta
completa, in modo che il contatore incluso dal server sia visibile.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Modifica rispetto all'esercizio 0:
    - Nessuna modifica strutturale necessaria: il client gia' stampava
      la risposta completa. E' stato aggiunto un commento per chiarire
      che l'output mostra ora il contatore, ad esempio "PONG #3".

Nota: avviare udp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket
import time


HOST        = "127.0.0.1"
PORT        = 65433
BUFFER_SIZE = 1024
NUMERO_PING = 5


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    print(f"[Client] Socket UDP pronto. Inviero' a {HOST}:{PORT}\n")
    return sock


def invia_ping(sock, numero):
    messaggio = "PING"

    print(f"[Client] Invio #{numero}: {messaggio!r}")

    sock.sendto(messaggio.encode("utf-8"), (HOST, PORT))

    try:
        dati, indirizzo_server = sock.recvfrom(BUFFER_SIZE)

        # Stampo la stringa di risposta completa per rendere visibile il contatore.
        # Con il server aggiornato l'output sara' ad esempio: 'PONG #3'
        risposta = dati.decode("utf-8")
        print(f"[Client] Risposta da {indirizzo_server}: {risposta!r}")

    except socket.timeout:
        print(f"[Client] Timeout, nessuna risposta per il ping #{numero}")


def avvia():
    sock = crea_socket_udp()
    try:
        for i in range(1, NUMERO_PING + 1):
            invia_ping(sock, i)
            time.sleep(0.5)
    finally:
        print("\n[Client] Fine. Chiudo il socket.")
        sock.close()


if __name__ == "__main__":
    avvia()