"""
TCP Client - Ping Pong
Exercise 0: riscritto con le funzioni

Codice originale: https://github.com/IsidurPaine/Socket
Modificato da: [Il tuo nome]
"""

import socket
import time

HOST = "127.0.0.1"
PORT = 65432
NUMERO_PING = 5


def crea_socket_client():
    """
    Crea il socket TCP e si connette al server.
    connect() esegue il three-way handshake TCP.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[Client] Connesso a {HOST}:{PORT}")
    return sock


def invia_un_ping(sock, numero):
    """
    Invia un PING e stampa la risposta ricevuta dal server.
    """
    messaggio = "PING"
    print(f"\n[Client] Invio ping #{numero}: {messaggio}")
    sock.sendall(messaggio.encode("utf-8"))

    dati = sock.recv(1024)
    risposta = dati.decode("utf-8")
    print(f"[Client] Risposta: {risposta}")


def avvia():
    sock = crea_socket_client()
    try:
        for i in range(1, NUMERO_PING + 1):
            invia_un_ping(sock, i)
            time.sleep(0.5)
    finally:
        print("\n[Client] Fine. Chiudo la connessione.")
        sock.close()


if __name__ == "__main__":
    avvia()