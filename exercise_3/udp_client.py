"""
UDP Client - Gestione timeout su canale inaffidabile (Esercizio 3)

Aggiorna il client UDP dell'esercizio 0 per gestire i timeout in modo
significativo quando il server scarta le risposte e per continuare
al ping successivo invece di crashare.

Nota: avviare udp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket
import time


HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024
NUMERO_PING = 10   # uso 10 ping per osservare meglio l'effetto della perdita


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(2.0)

    print(f"[Client] Inviero' {NUMERO_PING} ping a {HOST}:{PORT}. Aspettati delle perdite!\n")
    return sock


def invia_ping(sock, numero, ricevuti, persi):
    """
    Invia un ping e aggiorna i contatori di ricevuti e persi.
    Restituisce i contatori aggiornati.
    """

    messaggio = "PING"
    print(f"[Client] Invio #{numero}: {messaggio!r}")

    sock.sendto(messaggio.encode("utf-8"), (HOST, PORT))

    try:
        dati, indirizzo_server = sock.recvfrom(BUFFER_SIZE)
        risposta = dati.decode("utf-8")
        print(f"[Client] Risposta da {indirizzo_server}: {risposta!r}")
        ricevuti = ricevuti + 1

    except socket.timeout:
        print(f"[Client] Timeout, nessuna risposta per il ping #{numero}")
        persi = persi + 1

    return ricevuti, persi


def avvia():
    sock = crea_socket_udp()
    ricevuti = 0
    persi    = 0

    try:
        for i in range(1, NUMERO_PING + 1):
            ricevuti, persi = invia_ping(sock, i, ricevuti, persi)
            time.sleep(0.5)
    finally:
        # Stampo un riepilogo finale delle statistiche
        print(f"\n[Client] Risultati: {ricevuti} ricevuti, {persi} persi su {NUMERO_PING} ping")
        sock.close()


if __name__ == "__main__":
    avvia()