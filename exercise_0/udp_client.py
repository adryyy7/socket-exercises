"""
UDP Server - Ping Pong (Esercizio 0)

Attende datagrammi UDP e risponde "PONG" ad ogni "PING" ricevuto.
Rispetto al codice originale, la logica e' stata suddivisa in funzioni
separate per rendere il codice piu' leggibile e facile da modificare.

Differenze principali rispetto a TCP:
    - SOCK_DGRAM al posto di SOCK_STREAM = UDP, senza connessione
    - Nessun listen() o accept() = non si "stabilisce" mai una connessione
    - recvfrom() al posto di recv() = restituisce anche l'indirizzo del mittente
    - sendto()   al posto di sendall() = bisogna specificare la destinazione ogni volta
    - Nessun close() per singolo client = non esiste un socket per singolo client

Nota: avviare udp_server.py in un terminale prima di avviare udp_client.py
in un altro terminale.
"""

import socket
import time


HOST        = "127.0.0.1"  
PORT        = 65433        
BUFFER_SIZE = 1024         
NUMERO_PING = 5          


def crea_socket_udp():
    """
    Crea il socket UDP e imposta il timeout.
    Il timeout e' necessario perche' UDP non garantisce la consegna:
    senza di esso recvfrom() si bloccherebbe per sempre se il server
    non risponde o il datagramma viene perso.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(2.0)

    print(f"[Client] Socket UDP pronto. Inviero' a {HOST}:{PORT}\n")
    return sock


def invia_ping(sock, numero):
    """
    Invia un singolo datagramma PING e aspetta la risposta.
    Gestisce il timeout nel caso in cui il server non risponda.
    """

    messaggio = "PING"

    print(f"[Client] Invio #{numero}: {messaggio!r}")

    sock.sendto(messaggio.encode("utf-8"), (HOST, PORT))

    try:
        # recvfrom() si blocca finche' arriva un datagramma o scade il timeout.
        # Restituisce:
        #   dati         = i byte della risposta
        #   indirizzo_server = (ip, porta) del mittente, utile per verificare
        #                      che la risposta venga davvero dal nostro server
        dati, indirizzo_server = sock.recvfrom(BUFFER_SIZE)

        risposta = dati.decode("utf-8")

        print(f"[Client] Risposta da {indirizzo_server}: {risposta!r}")

    except socket.timeout:
        print(f"[Client] Timeout, nessuna risposta per il ping #{numero}")


def avvia():
    """
    Funzione principale: crea il socket, invia i ping e chiude il socket.
    """

    sock = crea_socket_udp()
    try:
        for i in range(1, NUMERO_PING + 1):
            invia_ping(sock, i)
            # Piccola pausa tra un ping e l'altro per rendere l'output piu' leggibile
            time.sleep(0.5)
    finally:
        print("\n[Client] Fine. Chiudo il socket.")
        # Libero il descrittore di file del sistema operativo associato a questo socket.
        # Per UDP non c'e' scambio FIN/ACK: il socket semplicemente scompare localmente.
        sock.close()


if __name__ == "__main__":
    avvia()