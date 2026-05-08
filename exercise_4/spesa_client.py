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

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Nota: avviare spesa_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket   # modulo della libreria standard per la programmazione di rete


HOST = "127.0.0.1"
PORT = 65436


def crea_socket_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[Client] Connesso al server lista della spesa su {HOST}:{PORT}")
    print("[Client] Comandi disponibili:")
    print("         AGGIUNGI prodotto   = aggiunge un prodotto alla lista")
    print("         RIMUOVI  prodotto   = rimuove un prodotto dalla lista")
    print("         MOSTRA              = mostra tutta la lista")
    print("         QUIT                = esci\n")
    return sock


def avvia():
    sock = crea_socket_client()

    try:
        while True:

            # Leggo il comando dell'utente da tastiera
            comando = input("[Client] > ").strip()

            # Ignoro le righe vuote
            if not comando:
                continue

            # Invio il comando al server
            sock.sendall(comando.encode("utf-8"))

            # Aspetto la risposta del server
            dati = sock.recv(1024)

            if not dati:
                print("[Client] Il server ha chiuso la connessione.")
                break

            risposta = dati.decode("utf-8")
            print(f"[Client] {risposta}\n")

            # Se ho inviato QUIT esco dal loop
            if comando.upper() == "QUIT":
                break

    finally:
        sock.close()
        print("[Client] Disconnesso.")


if __name__ == "__main__":
    avvia()