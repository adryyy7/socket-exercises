"""
UDP Server - Ping Pong con contatore messaggi
Exercise 1

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket

HOST = "127.0.0.1"
PORT = 65433


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.")
    return sock


def scegli_risposta(messaggio, contatore):
    """
    Restituisce la risposta includendo il contatore nel PONG.
    Esempio: "PONG #3"
    """
    if messaggio == "PING":
        return f"PONG #{contatore}"
    else:
        return "ERROR: messaggio sconosciuto"


def servi_sempre(sock):
    # Il contatore parte da 0 prima del loop.
    # Ogni PING ricevuto lo incrementa di 1.
    contatore_ping = 0

    while True:
        dati, indirizzo_client = sock.recvfrom(1024)
        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Ricevuto '{messaggio}' da {indirizzo_client}")

        if messaggio == "PING":
            contatore_ping = contatore_ping + 1

        risposta = scegli_risposta(messaggio, contatore_ping)
        sock.sendto(risposta.encode("utf-8"), indirizzo_client)
        print(f"[Server] Inviato: {risposta}")


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