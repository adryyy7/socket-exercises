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


HOST = "127.0.0.1"
PORT = 65433


def crea_socket_udp():
    """
    Crea il socket UDP e lo collega all'indirizzo e alla porta.
    In UDP non servono listen() e accept() perché non esiste il concetto
    di connessione: ogni datagramma arriva in modo indipendente.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((HOST, PORT))

    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def scegli_risposta(messaggio):
    """
    Restituisce la risposta corretta in base al messaggio ricevuto.
    """

    if messaggio == "PING":
        return "PONG"
    else:
        return f"Sconosciuto: {messaggio!r}"


def servi_sempre(sock):
    """
    Loop principale: riceve datagrammi e risponde a ciascuno all'infinito.
    Si ferma solo quando l'utente preme Ctrl+C.
    """

    while True:

        dati, indirizzo_client = sock.recvfrom(1024)

        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto {messaggio!r} da {indirizzo_client}")

        risposta = scegli_risposta(messaggio)

        # sendto() invia un datagramma a un indirizzo specifico.
        sock.sendto(risposta.encode("utf-8"), indirizzo_client)

        print(f"[Server] Inviato {risposta!r} a {indirizzo_client}\n")


def avvia():
    """
    Funzione principale: crea il socket e avvia il loop di ricezione.
    Cattura Ctrl+C per uscire in modo pulito senza stampare un traceback.
    """

    sock = crea_socket_udp()
    try:
        servi_sempre(sock)
    except KeyboardInterrupt:
        print("\n[Server] Fermato.")
    finally:
        sock.close()


if __name__ == "__main__":
    avvia()