"""
UDP Client - Ping Pong
Exercise 0: riscritto con le funzioni

Codice originale: https://github.com/IsidurPaine/Socket
Modificato da: [Il tuo nome]
"""

import socket
import time

HOST = "127.0.0.1"
PORT = 65433
NUMERO_PING = 5


def crea_socket_udp():
    """
    Crea il socket UDP e imposta un timeout di 2 secondi.
    Il timeout è necessario perché UDP non garantisce la consegna:
    senza di esso, recvfrom() si bloccherebbe per sempre se il server
    non risponde.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    print(f"[Client] Socket UDP pronto. Invio a {HOST}:{PORT}")
    return sock


def invia_un_ping(sock, numero):
    messaggio = "PING"
    print(f"\n[Client] Invio ping #{numero}: {messaggio}")
    sock.sendto(messaggio.encode("utf-8"), (HOST, PORT))

    try:
        dati, indirizzo_server = sock.recvfrom(1024)
        risposta = dati.decode("utf-8")
        print(f"[Client] Risposta da {indirizzo_server}: {risposta}")
    except socket.timeout:
        print(f"[Client] Nessuna risposta per il ping #{numero} (timeout)")


def avvia():
    sock = crea_socket_udp()
    try:
        for i in range(1, NUMERO_PING + 1):
            invia_un_ping(sock, i)
            time.sleep(0.5)
    finally:
        print("\n[Client] Fine. Chiudo il socket.")
        sock.close()


if __name__ == "__main__":
    avvia()