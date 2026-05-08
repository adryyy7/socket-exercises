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


HOST = "127.0.0.1" 
PORT = 65432       


def crea_socket_server():
    """
    Crea il socket TCP, imposta le opzioni necessarie,
    lo collega all'indirizzo e lo mette in ascolto.
    Restituisce il socket pronto ad accettare connessioni.
    """

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((HOST, PORT))

    server_sock.listen(1)

    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    return server_sock


def aspetta_client(server_sock):
    """
    Blocca il programma finche' un client non completa il three-way handshake TCP.
    Restituisce la coppia (conn, indirizzo) dove:
        conn      = socket dedicato a questo singolo client
        indirizzo = tupla (ip, porta) che identifica il client remoto
    """

    # accept() si blocca qui finche' un client si connette completando la sequenza SYN / SYN-ACK / ACK del three-way handshake TCP.
    conn, indirizzo = server_sock.accept()

    print(f"[Server] Connessione accettata da {indirizzo}")
    return conn, indirizzo


def scegli_risposta(messaggio):
    """
    Restituisce la risposta corretta in base al messaggio ricevuto.
    Tenere questa logica separata rende facile aggiungere nuovi messaggi
    in futuro senza toccare il codice di rete.
    """

    if messaggio == "PING":
        return "PONG"
    else:
        # Qualsiasi altro messaggio riceve una risposta di errore informativa
        return f"Messaggio sconosciuto: {messaggio!r}"


def gestisci_client(conn):
    """
    Riceve messaggi dal client in un loop e risponde a ciascuno,
    finche' il client non chiude la connessione.
    """

    while True:

        # Leggo fino a 1024 byte dal client.
        # recv() si blocca finche' arrivano dati o la connessione viene chiusa.
        dati = conn.recv(1024)

        # recv() restituisce un oggetto bytes vuoto b"" quando il client
        # chiude la connessione: e' il segnale per uscire dal loop.
        if not dati:
            print("[Server] Il client ha chiuso la connessione.")
            break

        # Converto i byte grezzi in una stringa Python usando la codifica UTF-8.
        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto: {messaggio!r}")

        risposta = scegli_risposta(messaggio)

        # Riconverto la risposta in byte e la invio al client.
        conn.sendall(risposta.encode("utf-8"))

        print(f"[Server] Inviato: {risposta!r}")

    conn.close()


def avvia():
    """
    Funzione principale: crea il server, accetta un client, lo gestisce,
    poi si chiude in modo pulito.
    Il blocco try/finally garantisce che il socket del server venga sempre
    chiuso, anche se si verifica un errore inaspettato.
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