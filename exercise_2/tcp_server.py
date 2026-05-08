"""
TCP Server - Multi-client sequenziale con bonus threading (Esercizio 2)

Modifica il server TCP dell'esercizio 0 per servire piu' client in sequenza.
Dopo che un client si disconnette, il server torna ad aspettare il prossimo.
Usa un flag server_running e una costante MAX_CLIENTS per fermarsi in modo pulito.

Autore   : [Il tuo nome]
Data     : Maggio 2026
Versione : 1.0

Modifiche rispetto all'esercizio 0:
    - accept() ora si trova dentro un loop while
    - Aggiunto flag server_running per controllare il loop
    - Aggiunta costante MAX_CLIENTS come secondo meccanismo di stop
    - Bonus: codice threading incluso come commento, pronto da attivare

Nota: avviare tcp_server.py in un terminale, poi avviare tcp_client.py
dell'esercizio 0 in un altro terminale. Ripetere per testare piu' client.
"""

import socket       # modulo della libreria standard per la programmazione di rete
import threading    # modulo della libreria standard per la gestione dei thread


HOST       = "127.0.0.1"
PORT       = 65432
MAX_CLIENTS = 5     # il server si ferma dopo aver servito questo numero di client

# Flag che controlla il loop principale del server.
# Quando diventa False, il server smette di accettare nuovi client.
server_running = True


def crea_socket_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    # Aumento il backlog a 5 perche' ora possono arrivare piu' client
    server_sock.listen(5)
    print(f"[Server] In ascolto su {HOST}:{PORT}")
    print(f"[Server] Accettero' al massimo {MAX_CLIENTS} client.\n")
    return server_sock


def scegli_risposta(messaggio):
    if messaggio == "PING":
        return "PONG"
    else:
        return f"Messaggio sconosciuto: {messaggio!r}"


def gestisci_client(conn, indirizzo):
    """
    Gestisce un singolo client dall'inizio alla fine.
    Questa funzione viene usata sia nella versione sequenziale
    che nella versione con threading.
    """

    print(f"[Server] Gestisco il client {indirizzo}")

    while True:
        dati = conn.recv(1024)

        if not dati:
            print(f"[Server] Client {indirizzo} disconnesso.")
            break

        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Da {indirizzo}: {messaggio!r}")

        risposta = scegli_risposta(messaggio)
        conn.sendall(risposta.encode("utf-8"))
        print(f"[Server] Inviato a {indirizzo}: {risposta!r}")

    conn.close()


def avvia():
    """
    Loop principale del server.
    Versione sequenziale: gestisce un client alla volta.
    Dopo che un client si disconnette, il loop torna ad accept()
    e aspetta il client successivo.
    Il server si ferma quando server_running diventa False
    oppure quando raggiunge MAX_CLIENTS.
    """

    global server_running
    server_sock = crea_socket_server()
    clients_serviti = 0

    try:
        while server_running and clients_serviti < MAX_CLIENTS:

            print(f"[Server] Aspetto il client #{clients_serviti + 1} ...")

            # accept() si blocca finche' un nuovo client si connette
            conn, indirizzo = server_sock.accept()
            clients_serviti = clients_serviti + 1

            # VERSIONE SEQUENZIALE: gestisco un client alla volta.
            # Il loop non torna ad accept() finche' questo client non si disconnette.
            gestisci_client(conn, indirizzo)

            # ----------------------------------------------------------------
            # BONUS THREADING: decommentare le tre righe sotto e commentare
            # la riga gestisci_client(conn, indirizzo) qui sopra per passare
            # alla gestione parallela.
            # Con threading ogni client ha il proprio thread e il server puo'
            # gestire piu' client contemporaneamente: il thread principale
            # torna subito ad accept() senza aspettare la disconnessione.
            # ----------------------------------------------------------------
            # t = threading.Thread(target=gestisci_client, args=(conn, indirizzo))
            # t.daemon = True
            # t.start()

        server_running = False
        print(f"\n[Server] Raggiunto il massimo di client ({MAX_CLIENTS}). Chiudo.")

    finally:
        server_sock.close()


if __name__ == "__main__":
    avvia()