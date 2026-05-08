"""
UDP Server - Simulazione canale inaffidabile (Esercizio 3)

Estende il server UDP dell'esercizio 0 simulando la perdita di pacchetti.
Prima di ogni risposta viene estratto un numero casuale: se e' inferiore
a DROP_PROBABILITY la risposta viene scartata e viene stampato un messaggio.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Modifiche rispetto all'esercizio 0:
    - Aggiunta la costante DROP_PROBABILITY (0.3 = 30% di perdita)
    - Aggiunto import random
    - Prima di ogni sendto() viene estratto un numero casuale
    - Se il numero e' sotto la soglia, la risposta viene scartata

Nota: avviare udp_server.py in un terminale prima di avviare udp_client.py
in un altro terminale.
"""

import socket   # modulo della libreria standard per la programmazione di rete
import random   # modulo della libreria standard per la generazione di numeri casuali


HOST             = "127.0.0.1"
PORT             = 65433
DROP_PROBABILITY = 0.3   # probabilita' di perdere una risposta (0.3 = 30%)


def crea_socket_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto su {HOST}:{PORT}")
    print(f"[Server] Probabilita' di perdita: {int(DROP_PROBABILITY * 100)}%")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return f"Sconosciuto: {messaggio!r}"


def servi_sempre(sock):
    while True:

        dati, indirizzo_client = sock.recvfrom(1024)
        messaggio = dati.decode("utf-8").strip()

        print(f"[Server] Ricevuto {messaggio!r} da {indirizzo_client}")

        risposta = scegli_risposta(messaggio)

        # Simulazione perdita pacchetto:
        # random.random() genera un numero decimale casuale tra 0.0 e 1.0.
        # Se e' inferiore a DROP_PROBABILITY (0.3), circa il 30% delle volte,
        # scarto la risposta senza chiamare sendto().
        if random.random() < DROP_PROBABILITY:
            # Non invio la risposta: il client non ricevera' nulla
            # e andra' in timeout dopo 2 secondi.
            print("[Server] Dropped reply (simulated loss)")
        else:
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