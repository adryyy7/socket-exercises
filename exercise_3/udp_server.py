"""
UDP Server - Simulazione canale inaffidabile
Exercise 3

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket
import random

HOST = "127.0.0.1"
PORT = 65433

# Probabilità di perdere una risposta (0.3 = 30%)
DROP_PROBABILITY = 0.3


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto su {HOST}:{PORT}")
    print(f"[Server] Probabilità di perdita: {int(DROP_PROBABILITY * 100)}%")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return "ERROR: messaggio sconosciuto"


def servi_sempre(sock):
    while True:
        dati, indirizzo_client = sock.recvfrom(1024)
        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Ricevuto '{messaggio}' da {indirizzo_client}")

        risposta = scegli_risposta(messaggio)

        # Simulazione perdita pacchetto:
        # random.random() genera un numero tra 0.0 e 1.0
        # Se è minore di DROP_PROBABILITY, scarto la risposta
        if random.random() < DROP_PROBABILITY:
            print("[Server] Dropped reply (simulated loss)")
        else:
            sock.sendto(risposta.encode("utf-8"), indirizzo_client)
            print(f"[Server] Inviato '{risposta}' a {indirizzo_client}\n")


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