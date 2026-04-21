import socket
import threading
import json

# Definició de qui pot connectar-se al servidor, per ara tothom
HOST = '0.0.0.0'

# Port de connexió al servidor
PORT = 65432

# Mida màxima del missatge, per ara més que suficient.
BUFFER_SIZE = 1024

jugadors = {}
clients = {}
IDaIP = {}
state_lock = threading.Lock()

# Gestionem la conversio de STR a format JSON i l'enviem
def send_json(conn, data:dict):
    messaje = json.dumps(data) + "\n"
    conn.sendall(messaje.encode('utf-8'))

# Gestionem la conversio de STR a format JSON i l'enviem a tots els clients,
# excepte el remitent de l'informació.
def broadcast_json(sender_conn, data:dict):
    with state_lock:
        targets = [conn for conn in clients if conn is not sender_conn]
    message = (json.dumps(data) + "\n").encode('utf-8')
    for target in targets:
        try:
            target.sendall(message)
        except OSError:
            print("Desconnexió detectada")
            remove_client(target)

# Si un client es desconnecta, el retirem de la llista de clients actius, 
# per a no intentar enviar-li informació i evitar errors.
def remove_client(conn):
    player_id = None
    with state_lock:
        clients.pop(conn, None)
        player_id = IDaIP.pop(conn, None)

    if player_id is not None:
        broadcast_json(conn, {"action": "desconnexio", "player_id": player_id})

# Assignació d'una ID única quan un jugador es connecta, s'envia al client.
# Es defineix el jugador i se l'assigna una puntuació (0)
# Aquesta ID es relaciona amb la IP + port del client, per a ser identificat en futures connexions.
def register_new_player(conn):
    with state_lock:
        player_id = len(jugadors) + 1
        IDaIP[conn] = player_id
        jugadors[player_id] = {"puntuacio": 0}
    send_json(conn, {"action": "nouJugador", "player_id": player_id})

# Si algú les demana, s'envien les puntuacions guardades en el moment en el fitxer del servidor.
def send_scores(conn):
    with open('puntuacions.json', 'r', encoding='utf-8') as file:
        puntuacions = json.load(file)
    conn.sendall(json.dumps(puntuacions).encode('utf-8'))

# S'encarrega de gestionar les connexions de cada client, resolent les peticions adequades.
# Pot retornar les posicions, registrar un nou jugador, o reenviar missatges a altres clients.
def handle_client(conn, addr):
    # Quan s'estableix una nova connexió (un nou client es connecta),
    #  es mostra un missatge per consola, indicant l'adreça.
    print(f"Connectat amb: {addr}")
    buffer = ""

    # La connexió es manté activa mentre el client no es desconnecti,
    # i es van processant les peticions que van arribant.
    while True:
        try:
            # Rep el missatge del client
            data = conn.recv(BUFFER_SIZE)

            # Si no arriba informació (s'ha desconnectat el client), s'indica la desconnexió i es tanca el bucle.
            # La gestió de la desconnexió es porta a terme al final de la funció.
            if not data:
                print("Client desconnectat.")
                break

            # Els missatges es van afegint a un buffer, i es processen quann hi ha un salt de línia, que indica el final del missatge.
            buffer += data.decode('utf-8')

            # Guarda la línea i el que queda al buffer, per a processar-la.
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)

                except json.JSONDecodeError:
                    print(f"JSON no vàlid rebut: {line}")
                    continue

                # Guarda l'acció que es vol realitzar, i farà les accions pertinents segons el cas.
                action = data.get("action")

                # Envia les puntuacions a l'usuari que les ha demanat.
                if action == "get_puntuacions":
                    send_scores(conn)

                # Crea un nou jugador, l'assigna una ID, i el relaciona amb la seva connexió (IP).
                elif action == "nouJugador":
                    register_new_player(conn)

                # Reenvia les posicions i d'altres informacions a la resta de clients, que la processaran individualment.
                elif action == "posicio":
                    player_id = IDaIP.get(conn)

                    # Si el jugador existeix, es reenvia la informació a la resta de clients, junt amb la ID.
                    if player_id:
                        broadcast_json(conn, {
                            "action": "posicio",
                            "player_id": player_id,
                            "x": data.get("x"),
                            "y": data.get("y"),
                            "speedx": data.get("speedx"),
                            "speedy": data.get("speedy"),
                            "angle": data.get("angle")
                        })

        # Si hi ha algun error de connexió, es tanca la connexió i es surt del bucle.
        except OSError:
            break

    # Informa de la desconnexió del client, tanca la connexió i es retira de la llista de clients.
    print("Removing client and closing connection.")
    remove_client(conn)
    conn.close()
    
# Inici del servidor, es queda a l'espera de connexions entrants.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Permet reutilitzar l'adreça immediatament després de tancar el servidor.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enllaça el socket al ordinador host i el port determinats. Comença a escoltar les connexions. 
    s.bind((HOST, PORT))
    s.listen()

    print(f"Esperant connexió al port {PORT}...")

    while True:
        # Queda esperant a d'altres connexions, i quan aquestes arriben les accepta.
        # Acceptades, se separen en un objecte de connexió (conn) i una adreça (addr), que s'afegeixen en una llista de clients.
        conn, addr = s.accept()
        with state_lock:
            clients[conn] = addr

        # Quan captura alguna d'aquestes noves peticions, envia la gestió d'aquest a través d'un nou fil.
        # Aquest fil cridarà una funció que s'encarregarà de processar-lo, fent les accions pertinents.
        client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        client_thread.start()