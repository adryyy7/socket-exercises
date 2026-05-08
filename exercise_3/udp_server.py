"""
UDP Client - Gestione timeout su canale inaffidabile (Esercizio 3)

Aggiorna il client UDP dell'esercizio 0 per gestire i timeout in modo
significativo quando il server scarta le risposte e per continuare
al ping successivo invece di crashare.

Nota: avviare udp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket  
import random  


HOST = "127.0.0.1"
PORT = 65433
DROP_PROBABILITY = 0.3   # probabilita' di perdere una risposta (0.3 = 30%)


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto su {HOST}:{PORT}")
    print(f"[Server] Probabilita' di perdita: {int(DROP_PROBABILITY * 100)}%")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return f"Sconosciuto: {messaggio!r}"


def servi_sempre(sock):
    while True:

        dati, indirizzo_client = sock.recvfrom(1024)
        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto {messaggio!r} da {indirizzo_client}")

        risposta = scegli_risposta(messaggio)

        if random.random() < DROP_PROBABILITY:
            print("[Server] Dropped reply (simulated loss)")
        else:
            sock.sendto(risposta.encode("utf-8"), indirizzo_client)
            print(f"[Server] Inviato {risposta!r} a {indirizzo_client}\n")


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