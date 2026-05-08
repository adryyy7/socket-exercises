"""
UDP Server - Ping Pong
Exercise 0: riscritto con le funzioni

Codice originale: https://github.com/IsidurPaine/Socket
Modificato da: [Il tuo nome]
"""

import socket

HOST = "127.0.0.1"
PORT = 65433


def crea_socket_udp():
    """
    Crea il socket UDP e lo collega all'indirizzo e porta.
    In UDP non servono listen() e accept() perché non c'è connessione.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.")
    return sock


def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return "ERROR: messaggio sconosciuto"


def servi_sempre(sock):
    """
    Loop infinito: riceve datagrammi e risponde a ciascuno.
    recvfrom() restituisce anche l'indirizzo del mittente,
    che usiamo per sapere dove inviare la risposta con sendto().
    """
    while True:
        dati, indirizzo_client = sock.recvfrom(1024)
        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Ricevuto '{messaggio}' da {indirizzo_client}")

        risposta = scegli_risposta(messaggio)
        sock.sendto(risposta.encode("utf-8"), indirizzo_client)
        print(f"[Server] Inviato '{risposta}' a {indirizzo_client}")


def avvia():
    sock = crea_socket_udp()
    try:
        servi_sempre(sock)
    except KeyboardInterrupt:
        print("\n[Server] Fermato.")
    finally:
        sock.close()


if __name__ == "__main__":
    avvia()