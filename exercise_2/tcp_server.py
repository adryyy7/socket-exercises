"""
TCP Server - Multi-client sequenziale + bonus threading
Exercise 2

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

# Flag per controllare il loop principale del server.
# Quando server_running è False, il server smette di accettare nuovi client.
server_running = True

# Numero massimo di client da servire prima di fermarsi
MAX_CLIENTS = 5


def crea_socket_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"[Server] In ascolto su {HOST}:{PORT}")
    print(f"[Server] Accetterò al massimo {MAX_CLIENTS} client.")
    return server_sock


def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return "ERROR: messaggio sconosciuto"


def gestisci_client(conn, indirizzo):
    """
    Gestisce un singolo client dall'inizio alla fine.
    Questa funzione viene chiamata sia nella versione sequenziale
    che in quella con threading.
    """
    print(f"[Server] Gestisco il client {indirizzo}")

    while True:
        dati = conn.recv(1024)

        if not dati:
            print(f"[Server] Client {indirizzo} disconnesso.")
            break

        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Da {indirizzo}: {messaggio}")

        risposta = scegli_risposta(messaggio)
        conn.sendall(risposta.encode("utf-8"))
        print(f"[Server] Inviato a {indirizzo}: {risposta}")

    conn.close()


def avvia():
    global server_running
    server_sock = crea_socket_server()
    clients_serviti = 0

    try:
        # VERSIONE SEQUENZIALE con server_running flag:
        # dopo che un client si disconnette, il loop torna ad accept()
        # e aspetta il client successivo.
        # Il server si ferma quando server_running diventa False
        # oppure quando raggiunge MAX_CLIENTS.
        while server_running and clients_serviti < MAX_CLIENTS:
            print(f"\n[Server] Aspetto il client #{clients_serviti + 1} ...")
            conn, indirizzo = server_sock.accept()
            clients_serviti = clients_serviti + 1

            # ------------------------------------------------------------------
            # BONUS THREADING:
            # Decommentare le righe sotto e commentare gestisci_client(conn, indirizzo)
            # per passare alla versione con thread paralleli.
            # Con threading ogni client ha il proprio thread e il server può
            # gestire più client contemporaneamente senza aspettare che
            # il precedente si disconnetta.
            # ------------------------------------------------------------------
            # t = threading.Thread(target=gestisci_client, args=(conn, indirizzo))
            # t.daemon = True
            # t.start()

            # Versione sequenziale: gestisco un client alla volta
            gestisci_client(conn, indirizzo)

        server_running = False
        print(f"\n[Server] Raggiunto il massimo di client ({MAX_CLIENTS}). Chiudo.")

    finally:
        server_sock.close()


if __name__ == "__main__":
    avvia()