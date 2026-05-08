"""
Lista della Spesa Client - TCP (Esercizio 4)

Protocollo: TCP
Motivo: ogni comando modifica una lista sul server e il client deve sempre
ricevere una conferma. Con UDP un comando potrebbe perdersi silenziosamente
e il client non saprebbe mai se il prodotto e' stato aggiunto o no.
TCP garantisce la consegna in entrambe le direzioni.

Formato dei messaggi: testo semplice
    Client invia:    "AGGIUNGI latte"   Server risponde: "OK: 'latte' aggiunto"
    Client invia:    "RIMUOVI latte"    Server risponde: "OK: 'latte' rimosso"
    Client invia:    "MOSTRA"           Server risponde: "Lista: latte, pane"
    Client invia:    "QUIT"             Server risponde: "CIAO"

Messaggio non valido: il server risponde con un messaggio di errore che
spiega i comandi disponibili. La sessione continua normalmente.

Terminazione: il client invia "QUIT". Il server risponde "CIAO" e chiude
la connessione. E' sempre il client a iniziare la terminazione.

Nota: avviare spesa_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket 


HOST = "127.0.0.1"
PORT = 65436
MAX_CLIENTS = 10   # il server si ferma dopo aver servito questo numero di client


def crea_socket_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"[Server] Server lista della spesa in ascolto su {HOST}:{PORT}")
    print("[Server] In attesa di client...\n")
    return server_sock


def elabora_comando(messaggio, lista_spesa):
    """
    Interpreta il comando del client e aggiorna la lista della spesa.

    Comandi supportati:
        AGGIUNGI prodotto  = aggiunge il prodotto alla lista
        RIMUOVI  prodotto  = rimuove il prodotto dalla lista
        MOSTRA             = mostra tutti i prodotti nella lista
        QUIT               = chiude la connessione 

    Restituisce la risposta da inviare al client.
    """

    parti   = messaggio.strip().split(" ", 1)
    comando = parti[0].upper()

    if comando == "AGGIUNGI":

        # Controllo che ci sia un nome prodotto dopo il comando
        if len(parti) < 2 or parti[1].strip() == "":
            return "ERRORE: specifica il prodotto. Esempio: AGGIUNGI latte"

        # Converto in minuscolo per non distinguere tra "Latte" e "latte"
        prodotto = parti[1].strip().lower()

        if prodotto in lista_spesa:
            return f"'{prodotto}' è già nella lista"

        lista_spesa.append(prodotto)
        return f"OK: '{prodotto}' aggiunto alla lista"

    elif comando == "RIMUOVI":

        if len(parti) < 2 or parti[1].strip() == "":
            return "ERRORE: specifica il prodotto. Esempio: RIMUOVI latte"

        prodotto = parti[1].strip().lower()

        if prodotto not in lista_spesa:
            return f"ERRORE: '{prodotto}' non è nella lista"

        lista_spesa.remove(prodotto)
        return f"OK: '{prodotto}' rimosso dalla lista"

    elif comando == "MOSTRA":

        if len(lista_spesa) == 0:
            return "Lista vuota"

        return "Lista: " + ", ".join(lista_spesa)

    else:
        return "ERRORE: comando non riconosciuto. Usa: AGGIUNGI, RIMUOVI, MOSTRA, QUIT"


def gestisci_client(conn, indirizzo):
    """
    Gestisce una sessione completa con un client.
    La lista della spesa e' locale a questa funzione: ogni nuovo client
    inizia con una lista vuota.
    """

    print(f"[Server] Client connesso: {indirizzo}")

    # La lista vive qui: persiste per tutta la connessione di questo client.
    # Se il client si disconnette e si riconnette, la lista riparte vuota.
    lista_spesa = []

    while True:

        dati = conn.recv(1024)

        if not dati:
            print(f"[Server] Client {indirizzo} disconnesso.")
            break

        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Comando ricevuto: {messaggio!r}")

        # Gestisco QUIT separatamente perche' richiede la chiusura della connessione
        if messaggio.upper() == "QUIT":
            conn.sendall("CIAO".encode("utf-8"))
            print(f"[Server] Client {indirizzo} ha inviato QUIT.")
            break

        risposta = elabora_comando(messaggio, lista_spesa)
        conn.sendall(risposta.encode("utf-8"))
        print(f"[Server] Risposta inviata: {risposta!r}")

    conn.close()
    print(f"[Server] Connessione con {indirizzo} chiusa.\n")


def avvia():
    server_sock = crea_socket_server()
    clients_serviti = 0
    try:
        while clients_serviti < MAX_CLIENTS:
            conn, indirizzo = server_sock.accept()
            clients_serviti = clients_serviti + 1
            gestisci_client(conn, indirizzo)
    finally:
        server_sock.close()


if __name__ == "__main__":
    avvia()