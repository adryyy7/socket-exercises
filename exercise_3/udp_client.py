"""
UDP Client - Gestione timeout su canale inaffidabile
Exercise 3

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket
import time

HOST = "127.0.0.1"
PORT = 65433
NUMERO_PING = 10


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    print(f"[Client] Invio {NUMERO_PING} ping a {HOST}:{PORT}. Aspettati delle perdite!\n")
    return sock


def invia_un_ping(sock, numero, ricevuti, persi):
    messaggio = "PING"
    print(f"[Client] Invio ping #{numero}")
    sock.sendto(messaggio.encode("utf-8"), (HOST, PORT))

    try:
        dati, indirizzo_server = sock.recvfrom(1024)
        risposta = dati.decode("utf-8")
        print(f"[Client] Risposta: {risposta}")
        ricevuti = ricevuti + 1
    except socket.timeout:
        # Il server non ha risposto entro 2 secondi.
        # Stampo un messaggio significativo e CONTINUO al ping successivo.
        # Senza il timeout, il programma si bloccherebbe qui per sempre.
        print(f"[Client] Timeout — nessuna risposta per il ping #{numero}")
        persi = persi + 1

    return ricevuti, persi


def avvia():
    sock = crea_socket_udp()
    ricevuti = 0
    persi = 0

    try:
        for i in range(1, NUMERO_PING + 1):
            ricevuti, persi = invia_un_ping(sock, i, ricevuti, persi)
            time.sleep(0.5)
    finally:
        print(f"\n[Client] Risultati: {ricevuti} ricevuti, {persi} persi su {NUMERO_PING} ping")
        sock.close()


if __name__ == "__main__":
    avvia()