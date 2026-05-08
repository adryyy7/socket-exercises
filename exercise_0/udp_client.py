"""
UDP Client - Ping Pong (Esercizio 0: riscritto con le funzioni)

Invia "PING" cinque volte come datagrammi indipendenti e stampa ogni risposta.
Rispetto al codice originale, la logica e' stata suddivisa in funzioni
separate per rendere il codice piu' leggibile e facile da modificare.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Differenze principali rispetto a TCP:
    - SOCK_DGRAM al posto di SOCK_STREAM  =  UDP, senza connessione
    - Nessun connect()                    =  non si "stabilisce" mai una connessione
    - sendto()   al posto di sendall()    =  indirizzo di destinazione fornito ogni volta
    - recvfrom() al posto di recv()       =  restituisce anche l'indirizzo del mittente
    - close() non e' strettamente necessario ma lo chiamiamo per rilasciare il descrittore

Nota: avviare udp_server.py in un terminale prima di avviare questo client
in un altro terminale.
"""

import socket   # modulo della libreria standard per la programmazione di rete
import time     # usiamo time.sleep() per scandire i ping


HOST        = "127.0.0.1"  # indirizzo del server a cui vogliamo inviare i datagrammi
PORT        = 65433        # porta a cui il server e' collegato, deve corrispondere a udp_server.py
BUFFER_SIZE = 1024         # numero massimo di byte che ci aspettiamo in un singolo datagramma
NUMERO_PING = 5            # quanti ping inviare


def crea_socket_udp():
    """
    Crea il socket UDP e imposta il timeout.
    Il timeout e' necessario perche' UDP non garantisce la consegna:
    senza di esso recvfrom() si bloccherebbe per sempre se il server
    non risponde o il datagramma viene perso.
    """

    # AF_INET    = IPv4
    # SOCK_DGRAM = UDP, senza connessione, senza garanzia di consegna
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Imposto un timeout di 2 secondi sulle operazioni bloccanti (recvfrom).
    # Allo scadere del timeout, recvfrom() lancia socket.timeout invece di bloccarsi.
    sock.settimeout(2.0)

    print(f"[Client] Socket UDP pronto. Inviero' a {HOST}:{PORT}\n")
    return sock


def invia_ping(sock, numero):
    """
    Invia un singolo datagramma PING e aspetta la risposta.
    Gestisce il timeout nel caso in cui il server non risponda.
    """

    messaggio = "PING"

    print(f"[Client] Invio #{numero}: {messaggio!r}")

    # sendto() trasmette un datagramma.
    # Argomenti:
    #   1. Il payload codificato in byte (la rete non trasporta stringhe Python).
    #   2. La destinazione come tupla (host, porta), obbligatoria ogni volta
    #      perche' UDP non ha una connessione persistente che ricorda la destinazione.
    sock.sendto(messaggio.encode("utf-8"), (HOST, PORT))

    try:
        # recvfrom() si blocca finche' arriva un datagramma o scade il timeout.
        # Restituisce:
        #   dati         = i byte della risposta
        #   indirizzo_server = (ip, porta) del mittente, utile per verificare
        #                      che la risposta venga davvero dal nostro server
        dati, indirizzo_server = sock.recvfrom(BUFFER_SIZE)

        risposta = dati.decode("utf-8")

        print(f"[Client] Risposta da {indirizzo_server}: {risposta!r}")

    except socket.timeout:
        # Il server non ha risposto entro 2 secondi.
        # Questo puo' accadere perche' UDP non garantisce la consegna:
        #   - il datagramma potrebbe essersi perso (improbabile su localhost)
        #   - il server potrebbe non essere in esecuzione
        print(f"[Client] Timeout, nessuna risposta per il ping #{numero}")


def avvia():
    """
    Funzione principale: crea il socket, invia i ping e chiude il socket.
    """

    sock = crea_socket_udp()
    try:
        for i in range(1, NUMERO_PING + 1):
            invia_ping(sock, i)
            # Piccola pausa tra un ping e l'altro per rendere l'output piu' leggibile
            time.sleep(0.5)
    finally:
        print("\n[Client] Fine. Chiudo il socket.")
        # Libero il descrittore di file del sistema operativo associato a questo socket.
        # Per UDP non c'e' scambio FIN/ACK: il socket semplicemente scompare localmente.
        sock.close()


if __name__ == "__main__":
    avvia()