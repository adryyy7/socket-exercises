"""
UDP Client - Ping Pong con contatore messaggi (Esercizio 1)

Aggiorna il client dell'esercizio 0 per stampare la stringa di risposta
completa, in modo che il contatore incluso dal server sia visibile.

Nota: avviare udp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket   


HOST = "127.0.0.1"
PORT = 65433


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def scegli_risposta(messaggio, contatore):
    """
    Restituisce la risposta includendo il contatore nel PONG.
    Se il messaggio e' PING risponde "PONG #N", altrimenti segnala l'errore.
    """

    if messaggio == "PING":
        return f"PONG #{contatore}"
    else:
        return f"Sconosciuto: {messaggio!r}"


def servi_sempre(sock):
    """
    Loop principale con contatore dei PING ricevuti.
    Il contatore parte da 0 e aumenta di 1 ad ogni PING.
    """

    contatore_ping = 0

    while True:

        dati, indirizzo_client = sock.recvfrom(1024)
        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto {messaggio!r} da {indirizzo_client}")

        if messaggio == "PING":
            # Incremento il contatore di 1 ad ogni PING ricevuto
            contatore_ping = contatore_ping + 1

        risposta = scegli_risposta(messaggio, contatore_ping)

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