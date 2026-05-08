"""
UDP Server - Ping Pong (Esercizio 0: riscritto con le funzioni)

Attende datagrammi UDP e risponde "PONG" ad ogni "PING" ricevuto.
Rispetto al codice originale, la logica e' stata suddivisa in funzioni
separate per rendere il codice piu' leggibile e facile da modificare.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Differenze principali rispetto a TCP:
    - SOCK_DGRAM al posto di SOCK_STREAM  =  UDP, senza connessione
    - Nessun listen() o accept()          =  non si "stabilisce" mai una connessione
    - recvfrom() al posto di recv()       =  restituisce anche l'indirizzo del mittente
    - sendto()   al posto di sendall()    =  bisogna specificare la destinazione ogni volta
    - Nessun close() per singolo client   =  non esiste un socket per singolo client

Nota: avviare udp_server.py in un terminale prima di avviare udp_client.py
in un altro terminale.
"""

import socket   # modulo della libreria standard per la programmazione di rete


HOST = "127.0.0.1"  # indirizzo di loopback, accetta datagrammi solo da questa macchina
PORT = 65433        # porta su cui ascoltare (diversa dall'esempio TCP per evitare conflitti)


def crea_socket_udp():
    """
    Crea il socket UDP e lo collega all'indirizzo e alla porta.
    In UDP non servono listen() e accept() perche' non esiste il concetto
    di connessione: ogni datagramma arriva in modo indipendente.
    """

    # AF_INET    = IPv4
    # SOCK_DGRAM = UDP: senza connessione, senza garanzia di consegna, senza ordinamento.
    #              Ogni send() produce esattamente un datagramma indipendente.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Dico al sistema operativo di consegnare a questo socket
    # i datagrammi UDP in arrivo sulla PORT.
    # A differenza di TCP, non c'e' nessuna chiamata listen() dopo bind().
    sock.bind((HOST, PORT))

    print(f"[Server] In ascolto su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def scegli_risposta(messaggio):
    """
    Restituisce la risposta corretta in base al messaggio ricevuto.
    """

    if messaggio == "PING":
        return "PONG"
    else:
        return f"Sconosciuto: {messaggio!r}"


def servi_sempre(sock):
    """
    Loop principale: riceve datagrammi e risponde a ciascuno all'infinito.
    Si ferma solo quando l'utente preme Ctrl+C.
    """

    while True:

        # recvfrom() si blocca finche' arriva un datagramma.
        # Restituisce DUE valori (a differenza di recv() di TCP che restituisce solo byte):
        #   dati            = i byte grezzi del payload del datagramma
        #   indirizzo_client = tupla (ip, porta) che identifica chi ha inviato il datagramma
        # DOBBIAMO salvare questo indirizzo per sapere dove inviare la risposta.
        dati, indirizzo_client = sock.recvfrom(1024)

        # Decodifico i byte grezzi in una stringa Python (UTF-8)
        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto {messaggio!r} da {indirizzo_client}")

        risposta = scegli_risposta(messaggio)

        # sendto() invia un datagramma a un indirizzo specifico.
        # A differenza di sendall() di TCP, dobbiamo sempre fornire la destinazione
        # perche' UDP non ha una connessione corrente da usare.
        sock.sendto(risposta.encode("utf-8"), indirizzo_client)

        print(f"[Server] Inviato {risposta!r} a {indirizzo_client}\n")


def avvia():
    """
    Funzione principale: crea il socket e avvia il loop di ricezione.
    Cattura Ctrl+C per uscire in modo pulito senza stampare un traceback.
    """

    sock = crea_socket_udp()
    try:
        servi_sempre(sock)
    except KeyboardInterrupt:
        print("\n[Server] Fermato.")
    finally:
        sock.close()


if __name__ == "__main__":
    avvia()