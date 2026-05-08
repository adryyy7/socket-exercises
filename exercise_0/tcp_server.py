"""
TCP Server - Ping Pong
Exercise 0: riscritto con le funzioni

Codice originale: https://github.com/IsidurPaine/Socket
Modificato da: [Il tuo nome]
"""

import socket

HOST = "127.0.0.1"
PORT = 65432


def crea_socket_server():
    """
    Crea il socket TCP e lo prepara ad accettare connessioni.
    Uso SO_REUSEADDR per evitare l'errore 'Address already in use'
    se riavvio il server subito dopo averlo fermato.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    return server_sock


def aspetta_client(server_sock):
    """
    Blocca il programma finché un client non si connette.
    Restituisce il socket della connessione e l'indirizzo del client.
    """
    conn, indirizzo = server_sock.accept()
    print(f"[Server] Client connesso da {indirizzo}")
    return conn, indirizzo


def scegli_risposta(messaggio):
    """
    Restituisce la risposta giusta in base al messaggio ricevuto.
    Separare questa logica in una funzione rende facile aggiungere
    nuovi messaggi in futuro senza toccare il codice di rete.
    """
    if messaggio == "PING":
        return "PONG"
    else:
        return "ERROR: messaggio sconosciuto"


def gestisci_client(conn):
    """
    Riceve messaggi dal client in un loop e risponde,
    finché il client non chiude la connessione.
    """
    while True:
        dati = conn.recv(1024)

        # recv() restituisce bytes vuoti quando il client si disconnette
        if not dati:
            print("[Server] Client disconnesso.")
            break

        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Ricevuto: {messaggio}")

        risposta = scegli_risposta(messaggio)
        conn.sendall(risposta.encode("utf-8"))
        print(f"[Server] Inviato: {risposta}")

    conn.close()


def avvia():
    """
    Funzione principale: crea il server, accetta un client, lo gestisce.
    Il blocco try/finally garantisce che il socket venga sempre chiuso,
    anche se si verifica un errore inaspettato.
    """
    server_sock = crea_socket_server()
    try:
        conn, indirizzo = aspetta_client(server_sock)
        gestisci_client(conn)
    finally:
        server_sock.close()
        print("[Server] Server fermato.")


if __name__ == "__main__":
    avvia()