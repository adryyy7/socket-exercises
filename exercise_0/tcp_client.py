"""
TCP Client - Ping Pong (Esercizio 0)

Si connette al server e invia "PING" cinque volte, stampando ogni risposta "PONG".
Rispetto al codice originale, la logica è stata suddivisa in funzioni
separate per rendere il codice più leggibile e facile da modificare.

Passi principali del client TCP:
    1. Creare il socket (socket.socket)
    2. Connettersi al server (socket.connect)
    3. Inviare e ricevere dati (socket.sendall, socket.recv)
    4. Chiudere la connessione (socket.close)

Nota: avviare tcp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket
import time


HOST = "127.0.0.1"
PORT = 65432
NUMERO_PING = 5


def crea_socket_client():
    """
    Crea il socket TCP e si connette al server.
    Restituisce il socket pronto per inviare e ricevere dati.
    """

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_sock.connect((HOST, PORT))

    print(f"[Client] Connesso a {HOST}:{PORT}")
    return client_sock


def invia_ping(client_sock, numero):
    """
    Invia un singolo PING al server e stampa la risposta ricevuta.
    """

    messaggio = "PING"

    print(f"\n[Client] Invio #{numero}: {messaggio!r}")

    # Codifico la stringa in byte (UTF-8) e li invio tutti.
    client_sock.sendall(messaggio.encode("utf-8"))

    # recv(1024) si blocca finché arrivano dati, leggendo al massimo 1024 byte.
    dati = client_sock.recv(1024)

    risposta = dati.decode("utf-8")

    print(f"[Client] Risposta: {risposta!r}")


def avvia():
    """
    Funzione principale: crea il socket, invia i ping e chiude la connessione.
    Il blocco try/finally garantisce la chiusura del socket anche in caso di errore.
    """

    client_sock = crea_socket_client()
    try:
        for i in range(1, NUMERO_PING + 1):
            invia_ping(client_sock, i)
            time.sleep(0.5)
    finally:
        print("\n[Client] Tutti i ping inviati. Chiudo la connessione.")
        client_sock.close()

if __name__ == "__main__":
    avvia()