"""
TCP Client - Ping Pong (Esercizio 0: riscritto con le funzioni)

Si connette al server e invia "PING" cinque volte, stampando ogni risposta "PONG".
Rispetto al codice originale, la logica e' stata suddivisa in funzioni
separate per rendere il codice piu' leggibile e facile da modificare.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Passi principali del client TCP:
    1. Creare il socket (socket.socket)
    2. Connettersi al server (socket.connect)
    3. Inviare e ricevere dati (socket.sendall, socket.recv)
    4. Chiudere la connessione (socket.close)

Nota: avviare tcp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket   # modulo della libreria standard per la programmazione di rete
import time     # modulo della libreria standard; usiamo time.sleep() per aggiungere pause


HOST = "127.0.0.1"  # indirizzo del server a cui vogliamo connetterci (stessa macchina)
PORT = 65432        # porta su cui il server e' in ascolto, deve corrispondere a tcp_server.py
NUMERO_PING = 5     # numero di ping da inviare


def crea_socket_client():
    """
    Crea il socket TCP e si connette al server.
    Restituisce il socket pronto per inviare e ricevere dati.
    """

    # AF_INET     = IPv4
    # SOCK_STREAM = TCP (affidabile, ordinato, basato sulla connessione)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Avvio il three-way handshake TCP con il server:
    #   1. Il client invia SYN
    #   2. Il server risponde con SYN-ACK
    #   3. Il client invia ACK, la connessione e' stabilita
    # Questa chiamata si blocca finche' l'handshake e' completato.
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
    # Il livello di rete trasporta solo byte grezzi, mai stringhe Python.
    client_sock.sendall(messaggio.encode("utf-8"))

    # Aspetto la risposta del server.
    # recv(1024) si blocca finche' arrivano dati, leggendo al massimo 1024 byte.
    dati = client_sock.recv(1024)

    # Decodifico i byte ricevuti in una stringa leggibile
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
            # Pausa di mezzo secondo tra un ping e l'altro per rendere
            # l'output piu' leggibile e simulare un intervallo realistico.
            time.sleep(0.5)
    finally:
        print("\n[Client] Tutti i ping inviati. Chiudo la connessione.")
        # Chiudo il socket: invia un pacchetto FIN al server per segnalare
        # che abbiamo finito, poi libera le risorse del sistema operativo.
        client_sock.close()


if __name__ == "__main__":
    avvia()