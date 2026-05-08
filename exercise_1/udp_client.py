"""
UDP Client - Ping Pong con contatore messaggi
Exercise 1

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket
import time

HOST = "127.0.0.1"
PORT = 65433
NUMERO_PING = 5


def crea_socket_udp():
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
        # Stampo la stringa di risposta completa per vedere il contatore
        # Esempio: Risposta: 'PONG #3'
        risposta = dati.decode("utf-8")
        print(f"[Client] Risposta: {risposta}")
    except socket.timeout:
        print(f"[Client] Nessuna risposta per il ping #{numero}")


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