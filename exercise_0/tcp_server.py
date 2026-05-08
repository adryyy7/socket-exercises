"""
TCP Server - Ping Pong (Esercizio 0: riscritto con le funzioni)

Attende la connessione di un client e risponde "PONG" ad ogni "PING" ricevuto.
Rispetto al codice originale, la logica e' stata suddivisa in funzioni
separate per rendere il codice piu' leggibile e facile da modificare.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Passi principali del server TCP:
    1. Creare il socket (socket.socket)
    2. Collegarlo a indirizzo e porta (socket.bind)
    3. Metterlo in ascolto (socket.listen)
    4. Accettare la connessione (socket.accept)
    5. Inviare e ricevere dati (socket.sendall, socket.recv)
    6. Chiudere la connessione (socket.close)

Nota: avviare tcp_server.py in un terminale prima di avviare tcp_client.py
in un altro terminale.
"""

import socket   # modulo della libreria standard per la programmazione di rete


HOST = "127.0.0.1"  # indirizzo di loopback, accetta connessioni solo da questa macchina
PORT = 65432        # porta su cui ascoltare; valori > 1024 non richiedono permessi di root


def crea_socket_server():
    """
    Crea il socket TCP, imposta le opzioni necessarie,
    lo collega all'indirizzo e lo mette in ascolto.
    Restituisce il socket pronto ad accettare connessioni.
    """

    # Creo il socket TCP
    # AF_INET     = usa indirizzi IPv4
    # SOCK_STREAM = usa TCP, che e' orientato alla connessione e garantisce la consegna
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permetto il riuso immediato della porta dopo la chiusura del programma.
    # Senza questa opzione, un riavvio rapido del server darebbe "Address already in use"
    # perche' il sistema operativo tiene la porta in stato TIME_WAIT per circa 60 secondi.
    # SOL_SOCKET   = l'opzione si applica al livello socket
    # SO_REUSEADDR = permette il riuso di indirizzo e porta ancora in TIME_WAIT
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Collego il socket a indirizzo e porta specifici.
    # Dopo questa chiamata il sistema operativo sa che i pacchetti in arrivo
    # sulla PORT devono essere consegnati a questo socket.
    server_sock.bind((HOST, PORT))

    # Porto il socket in modalita' passiva per poter accettare connessioni in entrata.
    # Il valore 1 e' il backlog, cioe' il numero massimo di connessioni in attesa
    # nella coda del kernel prima che le nuove vengano rifiutate.
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

    # accept() si blocca qui finche' un client si connette completando
    # la sequenza SYN / SYN-ACK / ACK del three-way handshake TCP.
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
        # strip() rimuove eventuali spazi o caratteri newline iniziali e finali.
        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto: {messaggio!r}")

        # Costruisco la risposta da inviare
        risposta = scegli_risposta(messaggio)

        # Riconverto la risposta in byte e la invio al client.
        # sendall() si assicura che tutti i byte vengano inviati anche se
        # il sistema operativo li accetta in piu' blocchi separati.
        conn.sendall(risposta.encode("utf-8"))

        print(f"[Server] Inviato: {risposta!r}")

    # Chiudo il socket del client: invia un pacchetto FIN e libera le risorse
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
        # Chiudo il socket principale: il server non accettera' piu' connessioni
        server_sock.close()
        print("[Server] Server fermato.")


# Eseguo avvia() solo quando il file viene avviato direttamente.
# Se un altro script importa questo file, avvia() non viene chiamata.
if __name__ == "__main__":
    avvia()