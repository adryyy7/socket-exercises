"""
Lista della Spesa Server — TCP
Exercise 4

=== Risposte alle domande del protocollo ===

PROTOCOLLO SCELTO: TCP
Motivo: il client modifica una lista condivisa sul server e deve sempre
ricevere una conferma. Con UDP un comando potrebbe perdersi in modo
silenzioso: il client penserebbe di aver aggiunto un prodotto, ma il
server non lo avrebbe mai ricevuto. TCP garantisce che ogni comando
venga consegnato e che ogni risposta torni al client.

FORMATO DEI MESSAGGI: testo semplice (plain text)
  Client → Server:  "AGGIUNGI latte"
  Server → Client:  "OK: 'latte' aggiunto alla lista"
  Client → Server:  "RIMUOVI latte"
  Server → Client:  "OK: 'latte' rimosso dalla lista"
  Client → Server:  "MOSTRA"
  Server → Client:  "Lista: latte, pane, uova"   oppure   "Lista vuota"
  Client → Server:  "ciao"  (comando sconosciuto)
  Server → Client:  "ERRORE: comando non riconosciuto"
  Client → Server:  "QUIT"
  Server → Client:  "CIAO" e chiude la connessione

MESSAGGIO NON VALIDO: se il comando non è AGGIUNGI, RIMUOVI, MOSTRA
o QUIT, il server risponde con un messaggio di errore che spiega
i comandi disponibili e continua a girare senza crashare.

TERMINAZIONE: il client invia "QUIT". Il server risponde "CIAO" e
chiude la connessione con quel client. È sempre il client a iniziare
la terminazione. Il server rimane poi in ascolto per altri client.

Basato sul codice dell'esercizio 0.
Modificato da: [Il tuo nome]
"""

import socket

HOST = "127.0.0.1"
PORT = 65436
MAX_CLIENTS = 10


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
    Interpreta il comando del client e aggiorna la lista.

    Comandi supportati:
      AGGIUNGI <prodotto>  → aggiunge il prodotto alla lista
      RIMUOVI <prodotto>   → rimuove il prodotto dalla lista
      MOSTRA               → mostra tutti i prodotti nella lista
      QUIT                 → chiude la connessione

    Restituisce la risposta da inviare al client.
    """
    # Divido il messaggio in parti: la prima è il comando, il resto è il prodotto
    # Es. "AGGIUNGI latte" → parti = ["AGGIUNGI", "latte"]
    parti = messaggio.strip().split(" ", 1)
    comando = parti[0].upper()

    if comando == "AGGIUNGI":
        # Controllo che ci sia un prodotto dopo il comando
        if len(parti) < 2 or parti[1].strip() == "":
            return "ERRORE: specifica il prodotto. Es: AGGIUNGI latte"
        prodotto = parti[1].strip().lower()
        if prodotto in lista_spesa:
            return f"'{prodotto}' è già nella lista"
        lista_spesa.append(prodotto)
        return f"OK: '{prodotto}' aggiunto alla lista"

    elif comando == "RIMUOVI":
        if len(parti) < 2 or parti[1].strip() == "":
            return "ERRORE: specifica il prodotto. Es: RIMUOVI latte"
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
    print(f"[Server] Client connesso: {indirizzo}")

    # La lista della spesa vive qui dentro: ogni client ricomincia
    # con una lista vuota. Se volessimo condividere la lista tra
    # più client dovremmo spostarla fuori da questa funzione.
    lista_spesa = []

    while True:
        dati = conn.recv(1024)

        if not dati:
            print(f"[Server] Client {indirizzo} disconnesso.")
            break

        messaggio = dati.decode("utf-8").strip()
        print(f"[Server] Comando ricevuto: '{messaggio}'")

        if messaggio.upper() == "QUIT":
            conn.sendall("CIAO".encode("utf-8"))
            print(f"[Server] Client {indirizzo} ha inviato QUIT.")
            break

        risposta = elabora_comando(messaggio, lista_spesa)
        conn.sendall(risposta.encode("utf-8"))
        print(f"[Server] Risposta inviata: '{risposta}'")

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