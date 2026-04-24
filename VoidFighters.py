    # Usadas para mostrar el propio juego
import pygame
import math
import random
import pathlib
from datetime import datetime

# Usadas para la conexión con el servidor
import threading
import requests
import json
import queue
import socket

pygame.init()
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# On es mostra tot el joc
screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.SCALED | pygame.FULLSCREEN)

# Les pantalles de cada jugador
playerScreen = pygame.Surface((WIDTH, HEIGHT))

# Minimapa 
minimapa = pygame.Surface((300, 200))

# Mapa del Joc
mapaW = 12000
mapaH = 8000
mapa = pygame.Surface((mapaW, mapaH))
rect_mapa = mapa.get_rect()
capaObjectes = pygame.Surface(mapa.get_size(), pygame.SRCALPHA)

capa_suport = pygame.Surface((500, 500), pygame.SRCALPHA)
capa_inicial = pygame.Surface(capa_suport.get_size(), pygame.SRCALPHA)


def cargadorSkins(sele = "roja"):
    p1 = [pygame.transform.scale(pygame.image.load("assets/skinsJugadores/" + sele + "/normal.png").convert_alpha(), (110,110)),
          pygame.transform.scale(pygame.image.load("assets/skinsJugadores/" + sele + "/turbo.png").convert_alpha(), (110,110))] 
    
    return p1

s = cargadorSkins()
player_skins = cargadorSkins("verde")

player_skin = player_skins[0]

podio = pygame.transform.scale(pygame.image.load("assets/elementosMenus/podio.png").convert_alpha(), (WIDTH//3, HEIGHT//3))
player1_fletxa = pygame.transform.scale(pygame.image.load("assets/elementosJugadores/flechaazul.png").convert_alpha(), (20, 20))
player2_fletxa = pygame.transform.scale(pygame.image.load("assets/elementosJugadores/flecharoja.png").convert_alpha(), (20,20))
fons = pygame.transform.scale(pygame.image.load("assets/elementosMapa/fons_pixelart.png").convert_alpha(), (12000, 8000))
fons_minimapa = pygame.transform.scale(pygame.image.load("assets/elementosMapa/fons_pixelart.png").convert_alpha(), (300, 200))
cohetImage = pygame.transform.scale(pygame.image.load("assets/elementosJugadores/cohet.png").convert_alpha(), (50, 50))
laser = pygame.transform.scale(pygame.image.load("assets/elementosJugadores/laser.png").convert_alpha(), (10,35))
desgraciado = pygame.transform.scale(pygame.image.load("assets/elementosMapa/desgraciado.png").convert_alpha(), (1000, 1000))
desgraciado_minimapa = pygame.transform.scale(pygame.image.load("assets/elementosMapa/desgraciado.png").convert_alpha(), (25, 25))
asteroid = pygame.image.load("assets/elementosMapa/asteroid.png").convert_alpha()
soporte = pygame.transform.scale(pygame.image.load("assets/elementosMapa/soporte.png").convert_alpha(), (500,500))
wormhole_image = pygame.transform.scale(pygame.image.load("assets/elementosMapa/warmhole.png").convert_alpha(), (300,300))

animacionJugar = [pygame.transform.scale(pygame.image.load("assets/animacionJugar/pixil-frame-" + str(x) + ".png"), (WIDTH,HEIGHT)) for x in range(0,48)]
animacionInicio = [pygame.transform.scale(pygame.image.load("assets/animacionInicio/frame_00" + str(x) + ".png"), (WIDTH,HEIGHT)) for x in range(1,64)]
planetasImatges = [
    pygame.image.load("assets/elementosMapa/marte.png").convert_alpha(),
    pygame.image.load("assets/elementosMapa/planetazul.png").convert_alpha(),
]
temporitzador = [
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/4_4.png").convert_alpha(), (130, 130)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/3_4.png").convert_alpha(), (130, 130)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/2_4.png").convert_alpha(), (130, 130)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/1_4.png").convert_alpha(), (130, 130)),
]
vidasImatges = [
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/vida1.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/vida2.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/vida3.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/vida4.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/vida5.png").convert_alpha(), (50, 50)),
]
letters = {
    "A": pygame.image.load("assets/caracteres/A.png").convert_alpha(),
    "B": pygame.image.load("assets/caracteres/B.png").convert_alpha(),
    "C": pygame.image.load("assets/caracteres/C.png").convert_alpha(),
    "D": pygame.image.load("assets/caracteres/D.png").convert_alpha(),
    "E": pygame.image.load("assets/caracteres/E.png").convert_alpha(),
    "F": pygame.image.load("assets/caracteres/F.png").convert_alpha(),
    "G": pygame.image.load("assets/caracteres/G.png").convert_alpha(),
    "H": pygame.image.load("assets/caracteres/H.png").convert_alpha(),
    "I": pygame.image.load("assets/caracteres/I.png").convert_alpha(),
    "J": pygame.image.load("assets/caracteres/J.png").convert_alpha(),
    "K": pygame.image.load("assets/caracteres/K.png").convert_alpha(),
    "L": pygame.image.load("assets/caracteres/L.png").convert_alpha(),
    "M": pygame.image.load("assets/caracteres/M.png").convert_alpha(),
    "N": pygame.image.load("assets/caracteres/N.png").convert_alpha(),
    "Ñ": pygame.image.load("assets/caracteres/Ñ.png").convert_alpha(),
    "O": pygame.image.load("assets/caracteres/O.png").convert_alpha(),
    "P": pygame.image.load("assets/caracteres/P.png").convert_alpha(),
    "Q": pygame.image.load("assets/caracteres/Q.png").convert_alpha(),
    "R": pygame.image.load("assets/caracteres/R.png").convert_alpha(),
    "S": pygame.image.load("assets/caracteres/S.png").convert_alpha(),
    "T": pygame.image.load("assets/caracteres/T.png").convert_alpha(),
    "U": pygame.image.load("assets/caracteres/U.png").convert_alpha(),
    "V": pygame.image.load("assets/caracteres/V.png").convert_alpha(),
    "W": pygame.image.load("assets/caracteres/W.png").convert_alpha(),
    "X": pygame.image.load("assets/caracteres/X.png").convert_alpha(),
    "Y": pygame.image.load("assets/caracteres/Y.png").convert_alpha(),
    "Z": pygame.image.load("assets/caracteres/Z.png").convert_alpha(),
    "-": pygame.image.load("assets/caracteres/-.png").convert_alpha(),
    "_": pygame.image.load("assets/caracteres/_.png").convert_alpha(),
    "~": pygame.image.load("assets/caracteres/~.png").convert_alpha(),
    "!": pygame.image.load("assets/caracteres/!.png").convert_alpha(),
    "?": pygame.image.load("assets/caracteres/question.png").convert_alpha(),
    "0": pygame.image.load("assets/caracteres/0.png").convert_alpha(),
    "1": pygame.image.load("assets/caracteres/1.png").convert_alpha(),
    "2": pygame.image.load("assets/caracteres/2.png").convert_alpha(),
    "3": pygame.image.load("assets/caracteres/3.png").convert_alpha(),
    "4": pygame.image.load("assets/caracteres/4.png").convert_alpha(),
    "5": pygame.image.load("assets/caracteres/5.png").convert_alpha(),
    "6": pygame.image.load("assets/caracteres/6.png").convert_alpha(),
    "7": pygame.image.load("assets/caracteres/7.png").convert_alpha(),
    "8": pygame.image.load("assets/caracteres/8.png").convert_alpha(),
    "9": pygame.image.load("assets/caracteres/9.png").convert_alpha(),
}
damage = {
    "left": pygame.transform.scale(pygame.image.load("assets/elementosMapa/damage/damage_side.png").convert_alpha(), (30, HEIGHT)),
    "right": pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/elementosMapa/damage/damage_side.png").convert_alpha(), (30, HEIGHT)), 180),
    "top": pygame.transform.scale(pygame.image.load("assets/elementosMapa/damage/damage_top.png").convert_alpha(), (WIDTH, 30)),
    "bottom": pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/elementosMapa/damage/damage_top.png").convert_alpha(),180),(WIDTH,30)),

}
explosion = [
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom1.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom2.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom3.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom4.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom5.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom6.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom7.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom8.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom9.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom10.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boom/boom11.png").convert_alpha(), (150, 150)),
]
explosionJugador = [
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom1.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom2.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom3.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom4.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom5.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom6.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom7.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom8.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom9.png").convert_alpha(), (150, 150)),
    pygame.transform.scale(pygame.image.load("assets/elementosJugadores/boomJugador/boom10.png").convert_alpha(), (150, 150)),
]


def reiniciar_joc():
    global running, guanyador, player
    for grup in (planetas, players, wormholes, fletxas, asteroids, cohets, explosions, bullets):
        for item in grup:
            grup.remove(item)
            item.kill()

    planetas.add(
        Planeta("Saturn", posx=mapaW / 2 - 250, posy=mapaH / 2 - 250, imatges=planetasImatges,size=random.randint(800, 1000), mass=random.randint(20, 30))
    )

    player = Player("Player1", player_skins, mapaW // 6, mapaH // 2)  # 1000 3000
    players.add(player)

    porta1 = Wormhole("porta1")
    porta2 = Wormhole("porta2")
    wormholes.add(porta1, porta2)

    """
    fletxas.add(
        Fletxa(player1, player2, "Player1", player1_fletxa),
        Fletxa(player2, player1, "Player2", player2_fletxa),
    )
    """
    running = True
    mapa.blit(fons, (0, 0))
    parets_mapa()
    guanyador = "p1"

def spawn_asteroids(numb=8):
    if len(asteroids) < numb:
        asteroids.add(
            Asteroide(size=random.randint(10, 30)),
        )

def comprovar_guanyador():
    global guanyador, DONDE, seleccion, navePodioPerd
    if player.health <= 0:
        guanyador = p1name.upper()
        player.muriendo = True
        navePodioPerd = pygame.transform.rotate(pygame.transform.scale(player.images[0], (350, 350)), 90)

def colisionsPlayers(player1, player2):

    #comprovar si els jugadors estan colisionant 
    distanciaPlayers = math.hypot(player1.x-player2.x, player1.y-player2.y)

    if distanciaPlayers < 80 and player1.collide_time <1 and player2.collide_time < 1:
        player1.collide_time = 10
        player2.collide_time = 10

        vxP1 = player1.speedx
        vyP1 = player1.speedy
        vxP2 = player2.speedx
        vyP2 = player2.speedy

        player1.speedx = -vxP1/2 + vxP2/2
        player1.speedy = -vyP1/2 + vyP2/2
        player2.speedx = -vxP2/2 + vxP1/2
        player2.speedy = -vyP2/2 + vyP1/2

def misilsCooldown(player):

    pantalla = playerScreen
    pantalla.blit(pygame.transform.scale(letters["E"], (40,40)), (WIDTH - 90, HEIGHT - 80))
    pantalla.blit(pygame.transform.scale(letters["Q"], (40,40)), (WIDTH - 230, HEIGHT - 80))

    pantalla.blit(pygame.transform.rotate(pygame.transform.scale(cohetImage, (125, 125)), -45), (WIDTH-200, HEIGHT-200))
    pantalla.blit(pygame.transform.rotate(pygame.transform.scale(laser, (25, 87.5)), -45), (WIDTH-300, HEIGHT-150))

    if player.cohetCooldown / 60 > 3:
        pantalla.blit(temporitzador[0], (WIDTH-185, HEIGHT-170))
    elif player.cohetCooldown / 60 > 2:
        pantalla.blit(temporitzador[1], (WIDTH-185, HEIGHT-170))
    elif player.cohetCooldown / 60 > 1:
        pantalla.blit(temporitzador[2], (WIDTH-185, HEIGHT-170))
    elif player.cohetCooldown / 60 > 0:
        pantalla.blit(temporitzador[3], (WIDTH-185, HEIGHT-170))

def objectesMinimapa(grup, color, relacio_mida):
    for objecte in grup:    #pygame.image.load("assets/saturno.png").convert_alpha(),
        posX = (objecte.x+objecte.size/2) / mapaW * 300
        posY = (objecte.y+objecte.size/2) / mapaH * 200
        pygame.draw.circle(minimapa, color, (int(posX), int(posY)), max(1, int(objecte.size / relacio_mida)))

def parets_mapa():
    x = 1000
    for n in range(0, 12):
        mapa.blit(pygame.transform.rotate(desgraciado, 90), ((x*n), 0))
        mapa.blit(pygame.transform.rotate(desgraciado, 270), ((x*n), mapaH-1000))

    for n in range(0,8):
        mapa.blit(pygame.transform.rotate(desgraciado, 180), (0, (x*n)))
        mapa.blit(pygame.transform.rotate(desgraciado, 0), (mapaW-1000, (x*n)))

def mostrarTot(finestra):
    for asteroid in asteroids:
        if asteroid.rect.colliderect(finestra):
            capaObjectes.blit(asteroid.image, asteroid.rect)

""" Para modificar cuando haya varios jugadores
    def drawFletxas():
            for fletxa in fletxas:
                if fletxa.playername == "Player1" and camera_player.colliderect(fletxa.rect):
                    posicio = (fletxa.rect.x - camera_player.x, fletxa.rect.y - camera_player.y)
                    leftScreen.blit(fletxa.image, posicio)
                elif fletxa.playername == "Player2" and camera_player.colliderect(fletxa.rect):
                   posicio = (fletxa.rect.x - camera_player2.x, fletxa.rect.y - camera_player.y)
                    rightScreen.blit(fletxa.image, posicio)
"""

def minimapaDraw():

    minimapa.blit(fons_minimapa, (0,0))

    objectesMinimapa(asteroids, (255,255,255), 10)
    for planeta in planetas:
        posX = (planeta.x / mapaW) * 300
        posY = (planeta.y / mapaH) * 200

        minimapa.blit(pygame.transform.scale(planeta.image, (planeta.size*0.025, planeta.size*0.025)), (int(posX), int(posY)))

    for wormhole in wormholes:
        posX = (wormhole.x-wormhole.size/2) / mapaW * 300
        posY = (wormhole.y-wormhole.size/2) / mapaH * 200

        minimapa.blit(pygame.transform.scale(wormhole.image, (wormhole.size*0.05, wormhole.size*0.05)), (int(posX), int(posY)))


    for player in players:
        posX = player.x / mapaW * 300
        posY = player.y / mapaH * 200
        rect = pygame.transform.rotate(relacio_colors[player.color], math.degrees(player.angle)-90).get_rect(center=(int(posX), int(posY)))
        minimapa.blit(pygame.transform.rotate(relacio_colors[player.color], math.degrees(player.angle)-90), rect)

    for player in other_players_group:
        posX = player.x / mapaW * 300
        posY = player.y / mapaH * 200
        rect = pygame.transform.rotate(relacio_colors["roja"], math.degrees(player.angle)-90).get_rect(center=(int(posX), int(posY)))
        minimapa.blit(pygame.transform.rotate(relacio_colors["roja"], math.degrees(player.angle)-90), rect)

    pygame.draw.line(minimapa, (255,255,255), (0,0), (300,0), 2)
    pygame.draw.line(minimapa, (255,255,255), (0,198), (300,198), 2)
    pygame.draw.line(minimapa, (255,255,255), (298,0), (298,200), 2)
    pygame.draw.line(minimapa, (255,255,255), (0,0), (0,200), 2)

    screen.blit(minimapa, (WIDTH//2 - minimapa.get_width()//2, 10))

def crearPalabras(palabra,tamaño,posy,posx="centrado"):
    if posx == "centrado":
        totalWidth = len(palabra) * tamaño
        startX = (WIDTH//2 - totalWidth // 2)
        for i,x in enumerate(palabra.upper()):
            if x != " ":
                screen.blit(pygame.transform.scale(letters[x],(tamaño,tamaño)),(startX + (i*(tamaño))-5,posy))
                if x in "ñÑ":
                    screen.blit(pygame.transform.scale(letters["~"], (tamaño,tamaño)),(startX + (i*(tamaño))-5,posy - 0.9*tamaño))
            else:
                pass
    else:
        for i,x in enumerate(palabra):
            if x != " ":
                screen.blit(pygame.transform.scale(letters[x],(tamaño,tamaño)),(posx - (tamaño*len(palabra))//2 + (i*(tamaño))-5,posy))
                if x in "ñÑ":
                    screen.blit(pygame.transform.scale(letters["~"], (tamaño,tamaño)),(posx - (tamaño*len(palabra))//2 + (i*(tamaño))-5,posy - 0.9*tamaño))
            else:
                pass
    return s
 
def drawVidas(player):

    if player.health >= 0:
        for vida in range (0, player.health//5):
            posicio = (vida * 60) + 25
            playerScreen.blit(vidasImatges[4], (posicio, 25))

        if player.health % 5 != 0:
            try: posicio
            except:playerScreen.blit(vidasImatges[player.health%5-1], (25, 25))
            else:playerScreen.blit(vidasImatges[player.health%5-1], (posicio+60, 25))

def cargarSkins():
    skins = []
    for carpeta in pathSkins.iterdir():
        if carpeta.is_dir():
            archivo1 = carpeta / "normal.png"
            archivo2 = carpeta / "turbo.png"

            if archivo1.exists() and archivo2.exists():
                skins.append(pathlib.Path(pathSkins / carpeta.name))
    return skins

def moverFondo():
    global y1, y2
    y1 += velocidad
    y2 += velocidad
    if y1 >= HEIGHT:
        y1 = -HEIGHT
    if y2 >= HEIGHT:
        y2 = -HEIGHT
    screen.blit(fondo, (0, y1))
    screen.blit(fondo, (0, y2))

def control_musica(cual):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    pygame.mixer.music.load(musicas[cual])
    if cual == "menu":
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1,0,5000)

def anti_camperos(ernesto):
    for player in ernesto:
        if player.x > 11000:
            player.speedx -= 0.2
        elif player.x < 1000:
            player.speedx += 0.2
        if player.y > 7000:
            player.speedy -= 0.2
        elif player.y < 1000:
            player.speedy += 0.2

# ===== FUNCIONES DE RED =====

def send_json_to_server(client_socket, data: dict):
    """Envía un diccionario JSON al servidor."""
    if client_socket is None:
        return None
    try:
        message = json.dumps(data) + "\n"
        client_socket.sendall(message.encode('utf-8'))
        return client_socket
    except OSError:
        client_socket.close()
        return None


def connect_to_server(server_ip, port):
    """Conecta al servidor y retorna el socket."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print("Connexió establerta!")
        return client_socket
    except OSError as error:
        print(f"No s'ha pogut connectar amb el servidor: {error}")
        client_socket.close()
        return None


def request_player_id(client_socket):
    """Solicita un ID de jugador al servidor."""
    if client_socket is None:
        return None

    try:
        send_json_to_server(client_socket, {"action": "nouJugador"})

        raw = b""
        while b"\n" not in raw:
            chunk = client_socket.recv(1024)
            if not chunk:
                return None
            raw += chunk

        response = json.loads(raw.split(b"\n", 1)[0].decode('utf-8'))
        return response.get("player_id")
    except (OSError, json.JSONDecodeError):
        return None


def send_player_position(client_socket, player):
    """Envía la posición del jugador al servidor."""
    return send_json_to_server(client_socket, {
        "action": "posicio",
        "player_id": player.id,
        "x": round(player.x, 2),
        "y": round(player.y, 2),
        "angle": player.angle,
        "speedx": round(player.speedx, 2),
        "speedy": round(player.speedy, 2),
    })


def receive_broadcasts(client_socket, stop_event, broadcast_queue):
    """Recibe broadcasts del servidor en un thread separado."""
    buffer = ""

    while not stop_event.is_set() and client_socket is not None:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            
            buffer += data.decode('utf-8')

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    broadcast_queue.put(data)
                except json.JSONDecodeError:
                    pass
            
        except OSError:
            break


# ===== FIN FUNCIONES DE RED =====

class Player(pygame.sprite.Sprite):

    def __init__(self, id, images, posx=100, posy=100):
        super().__init__()
        self.collide_time = 10
        self.pushable = True
        self.timetopushable = 0
        self.id = id
        self.health = 15
        self.x = posx
        self.y = posy
        self.speedtotal = 0
        self.acceleration = 0.25
        self.speedx = 0
        self.speedy = 0
        self.images = images
        self.image = images[0]
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.muerto = False
        self.muriendo = False
        self.explosionImages = explosionJugador
        self.anim_speed = 10
        self.anim_index = 0
        self.hit = False
        self.hit_opacity = 0
        self.cohetCooldown = 0
        self.shotCooldown = 20
        self.color = ""
        self.tp_cooldown = 0
        self.angle = math.radians(0)
        self.direccio = 0

    def update(self):
        if self.muriendo:
            self.explosion()
            if self.muerto:
                self.muriendo = False

        else:
            self.collide_time -= 1
            if self.tp_cooldown > 0:
                self.tp_cooldown -= 1

            self.draw_damage()
            self.direccio = math.degrees(math.atan2(((self.y+self.speedy)-self.y), ((self.x+self.speedx)-self.x)))


            if not self.pushable:
                self.timetopushable -= 1
                if self.timetopushable == 0:
                    self.pushable = True
            self.shotCooldown -= 1
            self.cohetCooldown -= 1
            if 20 < self.speedx or -20 > self.speedx:
                self.speedx *= 0.95
            if 20 < self.speedy or -20 > self.speedy:
                self.speedy *= 0.95

            self.colisionsAsteroides()

            keys = pygame.key.get_pressed()
            self.speedtotal = math.hypot(self.speedx, self.speedy)

            if keys[pygame.K_w]:
                self.speedx += self.acceleration * math.cos(self.angle)
                self.speedy -= self.acceleration * math.sin(self.angle)
                self.original_image = self.images[1]
            else:
                self.original_image = self.images[0]
            if keys[pygame.K_s]:
                self.speedx *= 0.95
                self.speedy *= 0.95
            if keys[pygame.K_a]:
                self.angle += math.radians(4)
            if keys[pygame.K_d]:
                self.angle -= math.radians(4)
            if keys[pygame.K_e] and self.cohetCooldown < 1:
                cohets.add(
                    cohet(image=cohetImage, owner=self)
                )
                self.cohetCooldown = 240
            if keys[pygame.K_q] and self.shotCooldown < 1:
                bullets.add(
                    bala(image=laser, owner=self)
                )
                self.shotCooldown = 20

            self.x += self.speedx
            self.y += self.speedy


            if self.x > mapaW-(WIDTH//4): self.speedx *= 0.98; self.speedy *= 0.98
            elif self.x < WIDTH//4: self.speedx *= 0.98; self.speedy *= 0.98
            if self.y > mapaH-(HEIGHT//2): self.speedx *= 0.98; self.speedy *= 0.98
            elif self.y < (HEIGHT//2): self.speedx *= 0.98; self.speedy *= 0.98

            if self.x > mapaW: self.x = 0
            elif self.x < 0: self.x = mapaW
            if self.y > mapaH: self.y = 0
            elif self.y < 0: self.y = mapaH


            self.rect.center = (self.x, self.y)
            self.image = pygame.transform.rotate(self.original_image, math.degrees(self.angle))
            self.rect = self.image.get_rect(center=self.rect.center)  # Update rect to new image size

            # Normalització de valors (posicions a INT, angle a 2 decimals)
            #self.x = self.x - (self.x % 1)
            #self.y = self.y - (self.y % 1)
            self.angle = math.floor(self.angle * 100) / 100

            capaObjectes.blit(self.image, self.rect)

    def draw_damage(self):

        if self.hit:
            self.hit_opacity = 255
            self.hit = False

        self.hit_opacity -= 8.5

        if self.hit_opacity > 0:
            damage["left"].set_alpha(self.hit_opacity)
            damage["top"].set_alpha(self.hit_opacity)
            damage["right"].set_alpha(self.hit_opacity)
            damage["bottom"].set_alpha(self.hit_opacity)

            playerScreen.blit(damage["left"], (0,0))
            playerScreen.blit(damage["top"], (0,0))
            playerScreen.blit(damage["right"], (WIDTH-30,0))
            playerScreen.blit(damage["bottom"], (0,HEIGHT-30))

    def colisionsAsteroides(self):
        for asteroide in asteroids:
            distance = math.hypot(self.x-asteroide.x, self.y-asteroide.y)

            if distance < 60:
                self.speedx += asteroide.speedX//2
                self.speedy += asteroide.speedY//2
                asteroids.remove(asteroide)
                del asteroide
                self.health -=3
                self.hit = True

    def explosion(self):
        if self.anim_speed > 0:
            if self.anim_index < 10:
                capaObjectes.blit(
                    self.explosionImages[self.anim_index], (self.x - 75, self.y - 75)
                )
                self.anim_speed -= 1
        else:
            capaObjectes.blit(
                self.explosionImages[self.anim_index], (self.x - 75, self.y - 75)
            )
            self.anim_speed = 4
            self.anim_index += 1

        if self.anim_index > 9:
            self.muerto = True

class otherPlayer(Player):
    def __init__(self, id, images, posx=100, posy=100, angle=0):
        super().__init__(id, images, posx, posy)
        self.moving_forward = False
        self.angle = 0
        self.new_angle = None
        self.canvi_angle = 0
        self.angle_index = 0


    def update(self):
        if self.muriendo:
            pass
            """self.explosion()
            if self.muerto:
                self.muriendo = False
            """

        else:
            self.collide_time -= 1
            if self.tp_cooldown > 0:
                self.tp_cooldown -= 1

#           self.draw_damage()
            self.direccio = math.degrees(math.atan2(((self.y+self.speedy)-self.y), ((self.x+self.speedx)-self.x)))


            if not self.pushable:
                self.timetopushable -= 1
                if self.timetopushable == 0:
                    self.pushable = True
#            self.shotCooldown -= 1
#            self.cohetCooldown -= 1
#            if 20 < self.speedx or -20 > self.speedx:
#                self.speedx *= 0.95
#            if 20 < self.speedy or -20 > self.speedy:
#                self.speedy *= 0.95

            self.speedtotal = math.hypot(self.speedx, self.speedy)

            if self.moving_forward:
                self.speedx += self.acceleration * math.cos(self.angle)
                self.speedy -= self.acceleration * math.sin(self.angle)
                self.original_image = self.images[1]
            else:
                self.original_image = self.images[0]

# Per jugador local, no usat pel remot
#            if keys[pygame.K_s]:
#                self.speedx *= 0.95
#                self.speedy *= 0.95
#            if keys[pygame.K_a]:
#                self.angle += math.radians(4)  # Rotate left
#            if keys[pygame.K_d]:
#                self.angle -= math.radians(4)  # Rotate right
#

            self.x += self.speedx
            self.y += self.speedy


            if self.x > mapaW-(WIDTH//4): self.speedx *= 0.98; self.speedy *= 0.98
            elif self.x < WIDTH//4: self.speedx *= 0.98; self.speedy *= 0.98
            if self.y > mapaH-(HEIGHT//2): self.speedx *= 0.98; self.speedy *= 0.98
            elif self.y < (HEIGHT//2): self.speedx *= 0.98; self.speedy *= 0.98

            if self.x > mapaW: self.x = 0
            elif self.x < 0: self.x = mapaW
            if self.y > mapaH: self.y = 0
            elif self.y < 0: self.y = mapaH

            if self.new_angle:
                self.canvi_angle = (self.new_angle - self.angle) / 10
                self.new_angle = None

            self.rect.center = (self.x, self.y)
            if self.angle_index < 10:
                self.image = pygame.transform.rotate(self.original_image, math.degrees((self.angle + (self.canvi_angle * self.angle_index))))
                self.angle_index += 1
            else:
                self.angle = self.angle + (self.canvi_angle * self.angle_index)
                self.canvi_angle = 0
                self.angle_index = 0

            self.rect = self.image.get_rect(center=self.rect.center)  # Update rect to new image size

            capaObjectes.blit(self.image, self.rect)

    def rebre_info(self, json_data):
        self.x = json_data["x"]
        self.y = json_data["y"]
        self.speedx = json_data["speedx"]
        self.speedy = json_data["speedy"]
        self.new_angle = json_data["angle"]
        self.rect.center = (self.x, self.y)

class Planeta(pygame.sprite.Sprite):
    def __init__(self, name, posx, posy, imatges, size, mass):
        super().__init__()
        self.size = size
        self.mass = mass
        self.name = name
        self.image = random.choice(imatges)
        self.rect = self.image.get_rect()
        self.speedx= 0
        self.speedy= 0
        self.x = posx
        self.y = posy
        self.rect.center = (self.x, self.y)
        self.OriginalPull = (size * mass) ** 0.015 - 1
        self.range = (size * mass) ** 1.1

    def update(self):

        capaObjectes.blit(self.image, (self.x, self.y))
        
        self.gravityPlayers(players)
        self.gravityAsteroids(asteroids)
        self.x = (mapaW-self.size)/2
        self.y = (mapaH-self.size)/2

        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.rect=self.image.get_rect(center = (self.x, self.y))

        self.OriginalPull = (self.size * self.mass) ** 0.010 - 1
        self.range = (self.size * self.mass) ** 0.75


    def gravityPlayers(self, players):

        for player in players:
            # Planet visual center (kept with existing offset for compatibility)
            cx = self.x + self.size/2
            cy = self.y + self.size/2

            # Vector from player to planet center
            dx = cx - player.x
            dy = cy - player.y
            dist = math.hypot(dx, dy) #+ 1e-6

            # gravitational pull (preserve original scaling intent)
            playerPull = (self.OriginalPull) * (self.range / (dist))
            if dist < self.range:
                angle = math.atan2(dy, dx)
                player.speedx += playerPull * math.cos(angle)
                player.speedy += playerPull * math.sin(angle)



            # NO TINC NI IDEA DE COM PERO FUNCIONA
            # NO TOCAR MAI

            # Collision / bounce: reflect player's velocity across the collision normal
            collision_radius = self.size/2
            if dist < collision_radius and player.pushable:
                # Normal from planet center to player (unit vector)
                nx = (player.x - cx) / dist
                ny = (player.y - cy) / dist

                # Incoming velocity
                vx = player.speedx
                vy = player.speedy

                # Reflect v around normal: v' = v - 2*(v·n)*n
                dot = vx * nx + vy * ny
                rx = vx - 2 * dot * nx
                ry = vy - 2 * dot * ny

                # Apply slight restitution so player bounces off a bit
                restitution = 1.05
                player.speedx = rx * restitution
                player.speedy = ry * restitution

                # Damage and temporary immunity to repeated pushes
                player.health -= 1
                player.hit = True
                player.pushable = False
                player.timetopushable = 10


    def gravityAsteroids(self, asteroids):
        for asteroid in asteroids:
            # Planet visual center (kept with existing offset for compatibility)
            cx = self.x + self.size/2
            cy = self.y + self.size/2

            # Vector from player to planet center
            dx = cx - asteroid.x
            dy = cy - asteroid.y
            dist = math.hypot(dx, dy)

            # gravitational pull (preserve original scaling intent)
            asteroidPull = (self.OriginalPull/1.5) * (self.range / (dist))
            angle = math.atan2(dy, dx)
            asteroid.speedX += asteroidPull * math.cos(angle)
            asteroid.speedY += asteroidPull * math.sin(angle)

            # NO TINC NI IDEA DE COM PERO FUNCIONA
            # NO TOCAR MAI

            # Collision / bounce: reflect player's velocity across the collision normal
            collision_radius = self.size/2
            if dist < collision_radius:
                # Normal from planet center to player (unit vector)
                nx = (asteroid.x - cx) / dist
                ny = (asteroid.y - cy) / dist

                # Incoming velocity
                vx = asteroid.speedX
                vy = asteroid.speedY

                # Reflect v around normal: v' = v - 2*(v·n)*n
                dot = vx * nx + vy * ny
                rx = vx - 2 * dot * nx
                ry = vy - 2 * dot * ny

                # Apply slight restitution so player bounces off a bit
                restitution = 1.05
                asteroid.speedX = rx * restitution
                asteroid.speedY = ry * restitution

                if asteroid.health == 1:
                    if self.size < 1100: self.size += asteroid.size // 2
                    self.mass += asteroid.mass / 20
                    asteroids.remove(asteroid)
                    asteroid.kill()
                    del asteroid
                else:
                    # Damage and temporary immunity to repeated pushes
                    asteroid.health -= 1
                    asteroid.timetopushable = 10

class Asteroide(pygame.sprite.Sprite):
    def __init__(self, size=10):
        super().__init__()
        startPos = random.choice([0,1,2,3])
        self.health = 3
        self.size = size
        self.mass = size/4
        self.image = asteroid
        self.originalImage = asteroid
        self.rect = self.image.get_rect()
        self.angle = 0
        self.tp_cooldown = 10
        # 0 Left 1 Right 2 Top 3 Bottom

        match startPos:
            case 0:
                self.x = random.randint(0, WIDTH//4)
                self.y = random.randint(0, mapaH)
            case 1:
                self.x = random.randint(mapaW-WIDTH//4, mapaW)
                self.y = random.randint(0, mapaH)
            case 2:
                self.x = random.randint(0, mapaW)
                self.y = random.randint(0, HEIGHT//2)
            case 3:
                self.x = random.randint(0, mapaW)
                self.y = random.randint(mapaH-HEIGHT//2, mapaH)
        self.rect.center = (self.x, self.y)
        self.speedX=random.uniform(-10, 10)
        self.speedY=random.uniform(-10, 10)
        self.timetopushable = 10

    def update(self):

        if self.tp_cooldown > 0:
            self.tp_cooldown -= 1

        if self.timetopushable > 0:
            self.timetopushable -= 1
        self.x += self.speedX
        self.y += self.speedY
        self.rect.center = (self.x, self.y)

        if 15 < self.speedX or -15 > self.speedX:
            self.speedX *= 0.95
        if 15 < self.speedY or -15 > self.speedY:
            self.speedY *= 0.95
        self.angle += 1

        self.image = pygame.transform.scale(pygame.transform.rotate(self.originalImage, self.angle), (self.size*4, self.size*4))
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.x > mapaW: self.x = 0
        elif self.x < 0: self.x = mapaW
        if self.y > mapaH: self.y = 0
        elif self.y < 0: self.y = mapaH

class Fletxa(pygame.sprite.Sprite):
    def __init__(self, player, enemy, name, image):
        super().__init__()
        self.OriginalImage = pygame.transform.rotate(image, 90)
        self.image = self.OriginalImage.copy()
        self.rect = self.image.get_rect()
        self.angle = 0
        self.rect = self.image.get_rect()
        self.player = player
        self.playername = name
        self.enemy = enemy
        self.x = player.x
        self.y = player.y
        self.rect.center = (self.x, self.y)

    def update(self):
        
        self.angle = math.atan2((self.enemy.y - self.player.y), (self.player.x - self.enemy.x))

        self.x = self.player.x + (math.cos(self.angle)*-120)
        self.y = self.player.y - (math.sin(self.angle)*-120)
        self.rect.center = (self.x, self.y)

        self.image = pygame.transform.rotate(self.OriginalImage, math.degrees(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

class cohet(pygame.sprite.Sprite):
    def __init__(self, image, owner):
        super().__init__()
        self.owner = owner

        self.originalImage = image
        self.x = self.owner.x + math.sin(owner.angle+1.55)*70
        self.y = self.owner.y + math.cos(owner.angle+1.55)*70
        self.thrust = 0.6
        self.speedx = self.owner.speedx + math.cos(owner.angle)*10
        self.speedy = self.owner.speedy + math.sin(owner.angle)*-10
        self.angle = math.atan2(-self.speedy, self.speedx)
        self.image = pygame.transform.rotate(self.originalImage, math.degrees(self.angle)-90)
        self.rect=self.image.get_rect()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = (self.x, self.y)

        self.timer = 300
        self.angleOwner = 0

    def follow_asteroids(self):
        self.rect.center = (self.x, self.y)
        for asteroid in asteroids:
            dist = math.hypot(
                self.x - asteroid.x,
                self.y - asteroid.y
            )

            if dist < 150:
                angle = math.atan2(
                    asteroid.y-self.y,
                    asteroid.x-self.x
                )
                self.speedx *= 0.95
                self.speedy *= 0.95
                self.speedx += self.thrust * math.cos(angle)
                self.speedy += self.thrust * math.sin(angle)
                if dist < 50:
                    explosions.add(explosion_animation(self.x, self.y))
                    asteroids.remove(asteroid)
                    del asteroid
                    cohets.remove(self)
                    self.kill()


    def update(self):

        self.follow_asteroids()

        self.angleOwner = math.atan2((self.owner.y-self.y), (self.owner.x-self.x))
        self.angle = math.atan2(-self.speedy, self.speedx)
        if self.rect.colliderect(camera_player):capaObjectes.blit(self.image, self.rect)
        self.timer -= 1
        self.x += self.speedx
        self.y += self.speedy
        self.rect.center = (self.x, self.y)
        distanciaOwner = math.hypot((self.x-self.owner.x), (self.y-self.owner.y))

        self.image = pygame.transform.rotate(self.originalImage, math.degrees(self.angle)-90)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.timer < 290:
            """
            if distancia < 800:
                self.speedx *= 0.95
                self.speedy *= 0.95
                self.speedx += self.thrust * math.cos(self.angleEnemic)
                self.speedy += self.thrust * math.sin(self.angleEnemic)
            """
            if distanciaOwner < 300:
                self.speedx -= self.thrust * math.cos(self.angleOwner)*0.6
                self.speedy -= self.thrust * math.sin(self.angleOwner)*0.6


        if self.timer == 0:
            explosions.add(explosion_animation(self.x, self.y))
            cohets.remove(self)
            self.kill()
        """
        elif distancia < 50:
            explosions.add(explosion_animation(self.x, self.y))
            self.enemy.health -= 3
            self.enemy.hit = True
            cohets.remove(self)
            self.kill()
        """

        if self.x > mapaW: self.x = 0
        elif self.x < 0: self.x = mapaW
        if self.y > mapaH: self.y = 0
        elif self.y < 0: self.y = mapaH

class bala(pygame.sprite.Sprite):
    def __init__(self, image, owner):
        super().__init__()
        self.owner = owner
        self.angle = self.owner.angle
        self.image = pygame.transform.rotate(image, math.degrees(self.angle) - 90)
        self.x = self.owner.x + math.sin(owner.angle + 1.55) * 50
        self.y = self.owner.y + math.cos(owner.angle + 1.55) * 50
        self.speedx = self.owner.speedx + math.cos(owner.angle) * 20
        self.speedy = self.owner.speedy + math.sin(owner.angle) * -20
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = (self.x, self.y)
        self.timer = 200

    def update(self):
        self.x += self.speedx
        self.y += self.speedy
        self.rect.center = (self.x, self.y)
        self.timer -= 1
        distanciaOwner = math.hypot(self.x - self.owner.x, self.y - self.owner.y)

        """
        if distanciaEnemy < 80:
            self.enemy.health -= 1
            self.enemy.hit = True
            self.kill()
        """
        if distanciaOwner < 60 and self.timer < 170:
            self.owner.health -= 1
            self.owner.hit = True
            self.kill()

        if self.timer < 1:
            self.kill()

        if self.rect.colliderect(camera_player):
            capaObjectes.blit(self.image, self.rect)

        if self.x > mapaW:
            self.x = 0
        elif self.x < 0:
            self.x = mapaW
        if self.y > mapaH:
            self.y = 0
        elif self.y < 0:
            self.y = mapaH

class explosion_animation(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.images = explosion
        self.x = posx-75
        self.y = posy-75
        self.anim_speed = 3
        self.anim_index = 0
        self.rect=self.images[0].get_rect()

    def update(self):
        self.rect.center = (self.x, self.y)
        if self.rect.colliderect(camera_player):
            if self.anim_speed > 0:
                if self.anim_index < 12:
                    capaObjectes.blit(
                        self.images[self.anim_index], (self.x, self.y)
                    )
                    self.anim_speed -= 1
            else:
                capaObjectes.blit(
                    self.images[self.anim_index], (self.x, self.y)
                )
                self.anim_speed = 3
                self.anim_index += 1

        if self.anim_index >10:
            self.kill()

class Zapato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Keep an unmodified original image to avoid repeated-rotation blur
        self.original_image = pygame.transform.scale(pygame.image.load("assets/elementosMenus/zapato.png").convert_alpha(), (WIDTH//14, WIDTH//14))
        self.image = self.original_image.copy()
        self.velocityx = 5
        self.velocityy = 5
        # Position inside the screen bounds (use image size to avoid spawning partly off-screen)
        # Use x,y as the CENTER of the sprite (not top-left)
        self.rect = self.image.get_rect()
        half_w, half_h = self.rect.width // 2, self.rect.height // 2
        self.x = random.randint(half_w, max(half_w, WIDTH - half_w))
        self.y = random.randint(half_h, max(half_h, HEIGHT - half_h))
        self.angle = 0
        # Angular velocity in degrees per frame (constant rotation)
        self.angular_velocity = 3
    
    def update(self): #Que vaya rebotando en las qesuinas menu principal
        # Update rotation (keep using original_image to avoid quality loss)
        self.angle = (self.angle + self.angular_velocity) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Move (x,y are the center of the sprite)
        self.x += self.velocityx
        self.y += self.velocityy

        # Use rotated image size for bounds checks
        img_w, img_h = self.image.get_width(), self.image.get_height()
        half_w, half_h = img_w / 2, img_h / 2

        # Bounce against screen edges while keeping center semantics
        if self.x - half_w <= 0:
            self.x = half_w
            self.velocityx = -self.velocityx
        elif self.x + half_w >= WIDTH:
            self.x = WIDTH - half_w
            self.velocityx = -self.velocityx

        if self.y - half_h <= 0:
            self.y = half_h
            self.velocityy = -self.velocityy
        elif self.y + half_h >= HEIGHT:
            self.y = HEIGHT - half_h
            self.velocityy = -self.velocityy

        # Update rect centered on (x,y) and blit
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, self.rect.topleft)

class Wormhole(pygame.sprite.Sprite):
    def __init__(self, porta):
        global wormholes
        super().__init__()
        self.original_image = wormhole_image
        self.image = self.original_image
        match porta:
            case "porta1":
                self.y = mapaH//8
                self.speedx = -8
            case "porta2":
                self.y = mapaH//8 * 6.5
                self.speedx = 8
        self.x = mapaW//2
        self.speedy = 0
        self.rect = self.image.get_rect()
        self.punt_forca_x = mapaW//2
        self.punt_forca_y = mapaH//2
        self.forca_centre = 0.02
        self.pull = 200
        self.size = 250
        self.angle = 0

    def update(self):
        self.angle = (self.angle+1)%360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        if 10 < self.speedx or -10 > self.speedx:
            self.speedx *= 0.99
        if 10 < self.speedy or -10 > self.speedy:
            self.speedy *= 0.99

        self.gravetat_players()
        self.gravetat_wormhole()
        self.gravetat_asteroids()

        self.x += self.speedx
        self.y += self.speedy
        self.rect.center = (self.x, self.y)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.colliderect(areaGran):
            capaObjectes.blit(self.image, self.rect)

    def gravetat_wormhole(self):

        for wormhole in wormholes:
            if wormhole != self:
                angle = math.atan2(
                    wormhole.y-self.y, wormhole.x-self.x
                )

                self.speedx += self.forca_centre * math.cos(angle)
                self.speedy += self.forca_centre * math.sin(angle)

    def gravetat_players(self):

        for player in players:

            dx = self.x-player.x
            dy = self.y-player.y
            dist = math.hypot(dx, dy)

            str = self.pull /(max(dist,  150))

            if dist < 800:
                angle = math.atan2(dy, dx)
                if player.tp_cooldown < 1:
                    player.speedx += str * math.cos(angle)
                    player.speedy += str * math.sin(angle)
                    player.speedx *= 0.98
                    player.speedy *= 0.98

                else:
                    player.speedx -= str/5 * math.cos(angle)
                    player.speedy -= str/5 * math.sin(angle)

            if dist < 100 and player.tp_cooldown < 1:
                player.tp_cooldown = 30
                for wormhole in wormholes:
                    if wormhole != self:
                        player.x = wormhole.x
                        player.y = wormhole.y


    def gravetat_asteroids(self):

        for asteroid in asteroids:

            dx = self.x-asteroid.x
            dy = self.y-asteroid.y
            dist = math.hypot(dx, dy)

            str = self.pull /(max(dist,  150))

            if dist < 400:
                angle = math.atan2(dy, dx)
                if asteroid.tp_cooldown < 1:
                    asteroid.speedX += str * math.cos(angle)
                    asteroid.speedY += str * math.sin(angle)
                else:
                    asteroid.speedX -= str/5 * math.cos(angle)
                    asteroid.speedY -= str/5 * math.sin(angle)

            if dist < 50 and asteroid.tp_cooldown < 1:
                asteroid.tp_cooldown = 30
                for wormhole in wormholes:
                    if wormhole != self:
                        asteroid.x = wormhole.x
                        asteroid.y = wormhole.y

def send_json(conn, data:dict):
    message = json.dumps(data) + "\n"
    conn.sendall(message.encode('utf-8'))

# Grupo planetas y planeta original
planetas = pygame.sprite.Group()

# Grupo jugadores i iniciado de jugadores
players = pygame.sprite.Group()
other_players_group = pygame.sprite.Group()

wormholes = pygame.sprite.Group()

# Grupo flechas e inicializacion
fletxas = pygame.sprite.Group()

# Creación grupo,asteroide se añaden en el juego
asteroids = pygame.sprite.Group()

# Creación grupo cohetes, seañaden en el juego
cohets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
bullets = pygame.sprite.Group()

camera_player = pygame.Rect(0, 0, WIDTH, HEIGHT)
areaGran = camera_player.inflate(200, 200)


# Cargar música y sonidos
pygame.mixer.init()
musicas = {
    "menu": "assets/elementosMenus/banda_sonora.mp3",
    "pelea": "assets/elementosMapa/banda_sonora_pelea.mp3",
    "seleccionar": "assets/elementosMenus/seleccionar.mp3"
}


seleccionar = pygame.mixer.Sound(musicas["seleccionar"]) # Seleccionar opción
pygame.mixer.Sound.set_volume(seleccionar, 5)
pygame.mixer.music.set_volume(0.5)


# Cargar imágenes
fondo = pygame.image.load("assets/elementosMenus/fondo.png").convert_alpha()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

titulo = pygame.image.load("assets/elementosMenus/titulo.png").convert_alpha()
boton_jugar = pygame.image.load("assets/elementosMenus/boton_jugar.png").convert_alpha()
boton_salir = pygame.image.load("assets/elementosMenus/boton_salir.png").convert_alpha()
flecha_roja = pygame.image.load("assets/elementosMenus/flecharoja.png").convert_alpha()
pausa = pygame.image.load("assets/elementosMenus/pausa.png").convert_alpha()
boton_reanudar = pygame.image.load("assets/elementosMenus/reanudar.png").convert_alpha()
boton_iralmenu = pygame.image.load("assets/elementosMenus/iralmenu.png").convert_alpha()

# Escalar imágenes
escala_titulo = 0.5
escala_boton = 0.45
escala_flecha = 0.6

titulo = pygame.transform.scale(titulo, (WIDTH//2.5, HEIGHT//2.5))
pausa = pygame.transform.scale(pausa, (617, 159))
boton_reanudar = pygame.transform.scale(boton_reanudar, (int(732 * escala_boton), int(166 * escala_boton)))
boton_iralmenu = pygame.transform.scale(boton_iralmenu, (int(1091 * escala_boton), int(166 * escala_boton)))
boton_jugar = pygame.transform.scale(boton_jugar, (WIDTH//8,HEIGHT//12))
boton_salir = pygame.transform.scale(boton_salir,(WIDTH//8,HEIGHT//12))
flecha_roja = pygame.transform.scale(flecha_roja, (int(122 * escala_flecha), WIDTH//30))
boton_reanudar_sel = pygame.transform.scale(boton_reanudar, (int(boton_reanudar.get_width() * 1.1), int(boton_reanudar.get_height() * 1.1)))
boton_iralmenu_sel = pygame.transform.scale(boton_iralmenu, (int(boton_iralmenu.get_width() * 1.1), int(boton_iralmenu.get_height() * 1.1)))
boton_salir_sel = pygame.transform.scale(boton_salir, (int(boton_salir.get_width() * 1.1), int(boton_salir.get_height() * 1.1)))
boton_jugar_sel = pygame.transform.scale(boton_jugar, (int(boton_jugar.get_width() * 1.1), int(boton_jugar.get_height() * 1.1)))

# Flechas giradas
flecha_izq = pygame.transform.rotate(flecha_roja, -90)
flecha_der = pygame.transform.rotate(flecha_roja, 90)
flecha_der_seleccion = pygame.transform.scale(flecha_izq, (WIDTH//12, WIDTH//12))
flecha_izq_seleccion = pygame.transform.scale(flecha_der, (WIDTH//12, WIDTH//12))
flecha_der_scaled = pygame.transform.scale(flecha_der_seleccion, (WIDTH//10, WIDTH//10))
flecha_izq_scaled = pygame.transform.scale(flecha_izq_seleccion, (WIDTH//10, WIDTH//10))

#imagenes menú controles
nave_azul_controles = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/skinsJugadores/azul/normal.png").convert_alpha(),(531//3,586//3)), 90)
nave_azul_turbo_controles = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/skinsJugadores/azul/turbo.png").convert_alpha(),(531//3,586//3)), 90)
nave_verde_controles = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/skinsJugadores/verde/normal.png").convert_alpha(),(470//3,611//3)), 90)
nave_verde_turbo_controles = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/skinsJugadores/verde/turbo.png").convert_alpha(),(470//3,611//3)), 90)
laser_controles = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/elementosJugadores/laser.png").convert_alpha(),(100//2,200//2)), 90)
cohet_controles = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/elementosJugadores/cohet.png").convert_alpha(),(4736//30,4736//30)),45)

# Posiciones base
pos_titulo = (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 6 - titulo.get_height() // 4)
pos_jugar = (WIDTH // 2 - boton_jugar.get_width() // 2, HEIGHT // 2 - boton_jugar.get_height() // 2)
pos_salir = (WIDTH // 2 - boton_salir.get_width() // 2, pos_jugar[1] + boton_jugar.get_height() + 60)
pos_boton_jugar_sel = (WIDTH // 2 - boton_jugar_sel.get_width() // 2, HEIGHT // 2 - boton_jugar_sel.get_height() // 2)
pos_boton_salir_sel = (WIDTH // 2 - boton_salir_sel.get_width() // 2, pos_jugar[1] + boton_jugar_sel.get_height() + 60)
pos_pausa = (WIDTH // 2 - pausa.get_width() // 2, HEIGHT // 6 - pausa.get_height() // 4)
pos_boton_reanudar = (WIDTH // 2 - boton_reanudar.get_width() // 2, HEIGHT // 2 - boton_reanudar.get_height() // 2)
pos_boton_iralmenu = (WIDTH // 2 - boton_iralmenu.get_width() // 2, pos_boton_reanudar[1] + boton_reanudar.get_height() + 60)
pos_salir = (WIDTH // 2 - boton_salir.get_width() // 2, pos_boton_iralmenu[1] + boton_iralmenu.get_height() + 60)
pos_boton_reanudar_sel = (WIDTH // 2 - boton_reanudar_sel.get_width() // 2, HEIGHT // 2 - boton_reanudar_sel.get_height() // 2)
pos_boton_iralmenu_sel = (WIDTH // 2 - boton_iralmenu_sel.get_width() // 2, pos_boton_reanudar[1] + boton_reanudar_sel.get_height() + 60)
pos_boton_salir_sel = (WIDTH // 2 - boton_salir_sel.get_width() // 2, pos_boton_iralmenu[1] + boton_iralmenu_sel.get_height() + 60)
pos_boton_salir_victoria = (WIDTH // 1.4 - boton_salir.get_width() // 2, HEIGHT // 2.1 - boton_salir.get_height() // 4)
pos_boton_iralmenu_victoria = (WIDTH // 1.4 - boton_iralmenu.get_width() // 2, pos_boton_salir_victoria[1] + boton_salir.get_height() + 60)
pos_boton_salir_sel_victoria = (WIDTH // 1.4 - boton_salir_sel.get_width() // 2, HEIGHT // 2.1 - boton_salir_sel.get_height() // 4)
pos_boton_iralmenu_sel_victoria = (WIDTH // 1.4 - boton_iralmenu_sel.get_width() // 2, pos_boton_salir_victoria[1] + boton_salir_sel.get_height() + 60)

boton_iralmenu_sel = pygame.transform.scale(boton_iralmenu, (int(boton_iralmenu.get_width() * 1.1), int(boton_iralmenu.get_height() * 1.1)))
boton_salir_sel = pygame.transform.scale(boton_salir, (int(boton_salir.get_width() * 1.1), int(boton_salir.get_height() * 1.1)))

#posiciones
pos_podio = (WIDTH // 4 - podio.get_width() // 2, HEIGHT // 1.65 - podio.get_height() // 4)
pos_boton_iralmenu_acaba = (WIDTH // 1.4 - boton_iralmenu.get_width() // 2, HEIGHT // 2.1 - boton_iralmenu.get_height() // 4)
pos_boton_salir = (WIDTH // 1.4 - boton_salir.get_width() // 2, pos_boton_iralmenu[1] + boton_iralmenu.get_height() + 60)
pos_boton_iralmenu_sel_acaba = (WIDTH // 1.4 - boton_iralmenu_sel.get_width() // 2, HEIGHT // 2.1 - boton_iralmenu_sel.get_height() // 4)
pos_boton_salir_sel_acaba = (WIDTH // 1.4 - boton_salir_sel.get_width() // 2, pos_boton_iralmenu[1] + boton_iralmenu_sel.get_height() + 60)

# Fondo animado
y1 = 0
y2 = -HEIGHT
velocidad = 2
cooldown = 0
queskin = 0

background = pygame.transform.scale(pygame.image.load("assets/elementosMapa/fons_pixelart.png").convert_alpha(), (WIDTH, HEIGHT))
pathSkins = pathlib.Path("assets/skinsJugadores")
skinsDisponibles = []

skinsDisponibles = cargarSkins()
enterPresionado = False

relacio_colors = {
    "azul": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-azul.png").convert_alpha(), (15,15)),
    "lila": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-lila.png").convert_alpha(), (15,15)),
    "marron": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-marron.png").convert_alpha(), (15,15)),
    "roja": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-roja.png").convert_alpha(), (15,15)),
    "turquesa": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-turquesa.png").convert_alpha(), (15,15)),
    "verde": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-verde.png").convert_alpha(), (15,15)),
    "platano": pygame.transform.scale(pygame.image.load("assets/elementosMapa/minimapa-platano.png").convert_alpha(), (15,15)),
}

# Control de selección
seleccion = True  # índice: 0 = jugar, 1 = salir
nomJugador = ""
# Rotación automática de naves en menú de controles
nave_rotation_p1 = 0
nave_rotation_p2 = 0
# Control tiempo y funcionalidad
clock = pygame.time.Clock()
running = True

# ===== INICIALIZAR RED =====
SERVER_IP = ''
PORT = 65432
client_socket = None
my_player_id = None
stop_event = threading.Event()
broadcast_queue = queue.Queue()
receiver_thread = None
other_players_dict = {}
send_position_cooldown = 0

# Solicitar IP del servidor si no está definida
if not SERVER_IP:
    SERVER_IP = input("Introdueix la IP del servidor (o deixa buida per saltar): ").strip()

# Conectar al servidor si se proporciona IP
if SERVER_IP:
    client_socket = connect_to_server(SERVER_IP, PORT)
    if client_socket is not None:
        my_player_id = request_player_id(client_socket)
        if my_player_id is not None:
            print(f"Player ID obtingut: {my_player_id}")
            # Iniciar thread para recibir broadcasts
            receiver_thread = threading.Thread(
                target=receive_broadcasts,
                args=(client_socket, stop_event, broadcast_queue),
                daemon=True
            )
            receiver_thread.start()
        else:
            print("No s'ha pogut obtenir el Player ID")
            if client_socket:
                client_socket.close()
                client_socket = None
# ===== FI INICIALIZAR RED =====


anim_speed = 4
zapato = Zapato()
anim_index = 0
DONDE = "AnimacionInicio"

control_musica("menu")

guanyador = "p1"

while running:
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN and DONDE == "seleccionNombre": 
            if event.key == pygame.K_BACKSPACE:  
                nomJugador = nomJugador[:-1]
            else:  
                if len(nomJugador) <= 12:
                    if event.unicode in "ABCDEFGHIJKLMNOPQRSTUVWXYZÑabcdefghijklmnopqrstuvwxyzñ-_!~ 0123456789":
                        nomJugador += event.unicode

    match DONDE:
        case "AnimacionInicio":
            if anim_speed > 0:
                if anim_index < 64:
                    screen.blit(
                        animacionInicio[anim_index], (0, 0)
                    )
                    anim_speed -= 1
            else:
                screen.blit(
                    animacionInicio[anim_index], (0, 0)
                )
                anim_speed = 3
                anim_index += 1

            if anim_index >= 63:
                DONDE = "INICIO"
                anim_index = 0

        case "INICIO":
            if cooldown <= 0:
                if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
                    seleccionar.play()
                    seleccion = not seleccion
                    cooldown = 300
            
            cooldown -= clock.get_time()

            if keys[pygame.K_RETURN] and not enterPresionado:
                enterPresionado = True
                seleccionar.play()
                if seleccion:
                    DONDE = "seleccionNombre"
                    reiniciar_joc()

                else:
                    running = False
                    continue         
            else:
                if not keys[pygame.K_RETURN]:
                    enterPresionado = False
            

            # Mover fondo
            moverFondo()

            screen.blit(fondo, (0, y1))
            screen.blit(fondo, (0, y2))
            
            zapato.update()
            # Dibujar título
            screen.blit(titulo, pos_titulo)

            # Dibujar botones
            if seleccion:
                boton_sel, pos_sel = boton_jugar_sel, pos_boton_jugar_sel
                screen.blit(boton_sel, pos_sel)
                screen.blit(boton_salir, pos_salir)
            else:
                boton_sel, pos_sel = boton_salir_sel, pos_boton_salir_sel
                screen.blit(boton_sel, pos_sel)
                screen.blit(boton_jugar, pos_jugar)

            crearPalabras("C", 60,HEIGHT*0.926,WIDTH*0.9583)

            if keys[pygame.K_c]:
                seleccionar.play()
                DONDE = "controles"

            # Dibujar flechas
            screen.blit(flecha_izq, (pos_sel[0] - flecha_izq.get_width() - 30, pos_sel[1] + boton_sel.get_height() // 2 - flecha_izq.get_height() // 2))
            screen.blit(flecha_der, (pos_sel[0] + boton_sel.get_width() + 30, pos_sel[1] + boton_sel.get_height() // 2 - flecha_der.get_height() // 2))

        case "controles":
            moverFondo()
            crearPalabras("PLAYER CONTROLS",WIDTH*0.046875,HEIGHT*0.04629)
            
            # Rotación de la nave cuando presionas A o D
            if keys[pygame.K_a]:
                nave_rotation_p1 += 3
            if keys[pygame.K_d]:
                nave_rotation_p1 -= 3
            
            # Mantener ángulo entre 0 y 360
            nave_rotation_p1 = nave_rotation_p1 % 360
            
            # Mostrar nave con turbo si presionas W, sino mostrar normal
            if keys[pygame.K_w]:
                nave_rotada = pygame.transform.rotate(nave_azul_turbo_controles, nave_rotation_p1)
            else:
                nave_rotada = pygame.transform.rotate(nave_azul_controles, nave_rotation_p1)
            
            rect_nave = nave_rotada.get_rect(center=(WIDTH*0.3515, HEIGHT*0.2962))
            screen.blit(nave_rotada, rect_nave)
            
            crearPalabras("W",WIDTH*0.05,WIDTH*0.1171,HEIGHT*0.2935)
            crearPalabras("ASD",WIDTH*0.05,WIDTH*0.166,HEIGHT*0.2935)
            crearPalabras("MOVEMENT",WIDTH*0.05,HEIGHT*0.22,WIDTH*0.65)

            crearPalabras("Q",WIDTH*0.05,HEIGHT*0.50,HEIGHT*0.29)
            screen.blit(laser_controles,(WIDTH*0.26, HEIGHT*0.5185))
            crearPalabras("LASER SHOOTING",WIDTH*0.04,HEIGHT*0.50,WIDTH*0.65)

            crearPalabras("E",WIDTH*0.05,HEIGHT*0.78, HEIGHT*0.29)
            screen.blit(cohet_controles,(WIDTH*0.23, HEIGHT*0.74))
            crearPalabras("ROCKET SHOOTING",WIDTH*0.04,HEIGHT*0.78,WIDTH*0.65)

            if keys[pygame.K_ESCAPE]:
                seleccionar.play()
                DONDE = "INICIO"
                
        case "seleccionNombre":
            moverFondo()
            crearPalabras("PLAYER NAME",WIDTH*0.052,WIDTH*0.026)
            crearPalabras(nomJugador.upper(),WIDTH*0.052,WIDTH*0.15625)
            if keys[pygame.K_RETURN] and not enterPresionado and len(nomJugador) > 0:
                queskin = 0
                seleccionar.play()
                p1name = nomJugador.upper()

                DONDE = "seleccionNaves"
                enterPresionado = True
            else:
                if not keys[pygame.K_RETURN]:
                    enterPresionado = False

        case "seleccionNaves":
            moverFondo()
            if cooldown <= 0:
                if keys[pygame.K_LEFT]:
                    queskin += 1
                    if queskin >= len(skinsDisponibles):
                        queskin = 0
                    cooldown = 300
                    dada="izquierda"
                

                elif keys[pygame.K_RIGHT]:
                    queskin -= 1
                    if queskin < 0:
                        queskin = len(skinsDisponibles) - 1
                    cooldown = 300
                    dada="dreta"

                else:
                    dada="cap"
                
            if cooldown > 0:
                cooldown -= clock.get_time()
            if len(p1name) > 10:
                crearPalabras(p1name.upper(),(WIDTH - WIDTH//3)//len(p1name),HEIGHT//24)
            else: 
                crearPalabras(p1name.upper(),WIDTH*0.078,HEIGHT*0.0416)
            
            crearPalabras("PRESS ENTER TO CONFIRM",WIDTH//24,HEIGHT - HEIGHT//8)

            nave = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(skinsDisponibles[queskin] / "normal.png").convert_alpha(),(WIDTH//3,WIDTH//3)), 90)
            screen.blit(nave, (WIDTH//2 - nave.get_width()//2, HEIGHT//2 + HEIGHT//24 - nave.get_height()//2))
            
            # Flechas derecha i izquierda en proporcion a la nave
            if dada=="izquierda":
                screen.blit(flecha_der_seleccion, (WIDTH - nave.get_width() + WIDTH//24 , HEIGHT//2 - flecha_der_seleccion.get_height()//2))
                screen.blit(flecha_izq_scaled, (WIDTH//2 - WIDTH//8 - WIDTH//96 - nave.get_width()//2, HEIGHT//2 - flecha_izq_scaled.get_height()//2))
            elif dada=="dreta":
                screen.blit(flecha_der_scaled, (WIDTH - nave.get_width() + WIDTH//24 , HEIGHT//2 - flecha_der_scaled.get_height()//2))
                screen.blit(flecha_izq_seleccion, (WIDTH//2 - WIDTH//8 - nave.get_width()//2, HEIGHT//2 - flecha_izq_seleccion.get_height()//2))
            else:
                screen.blit(flecha_der_seleccion, (WIDTH - nave.get_width() + WIDTH//24 , HEIGHT//2 - flecha_der_seleccion.get_height()//2))
                screen.blit(flecha_izq_seleccion, (WIDTH//2 - WIDTH//8 - nave.get_width()//2, HEIGHT//2 - flecha_izq_seleccion.get_height()//2))
            
            if keys[pygame.K_RETURN] and not enterPresionado:
                seleccionar.play()
                player.images = cargadorSkins(skinsDisponibles[queskin].name)
                player.color = skinsDisponibles[queskin].name

                DONDE = "JUEGO"
                enterPresionado = True

            else:
                if not keys[pygame.K_RETURN]:
                    enterPresionado = False

        case "JUEGO":

            # ===== PROCESAR RED =====
            # Procesar broadcasts recibidos del servidor
            try:
                while True:
                    data = broadcast_queue.get_nowait()
                    if data.get("action") == "posicio":
                        print(f"Posició rebuda: {data}")
                        pid = str(data.get("player_id"))
                        if pid != str(my_player_id):  # No procesar nuestra propia posición
                            if pid not in other_players_dict:
                                print(f"Nuevo jugador conectado: {pid}")
                                # Crear nuevo jugador si no existe
                                other_players_dict[pid] = otherPlayer(pid, cargadorSkins("marron"), data.get("x", 0), data.get("y", 0), data.get("angle", 0))
                                other_players_group.add(other_players_dict[pid])
                                other_players_dict[pid].rebre_info(data)
                            else:

                                # Actualizar posición de jugador existente
                                other_players_dict[pid].rebre_info(data)

                    elif data.get("action") == "desconnexio":
                        pid = str(data.get("player_id"))
                        if pid in other_players_dict:
                            other_players_group.remove(other_players_dict[pid])
                            del other_players_dict[pid]

            except queue.Empty:
                pass
            
            # Enviar posición del jugador actual (con cooldown)
            send_position_cooldown -= 1
            if send_position_cooldown <= 0 and client_socket is not None:
                client_socket = send_player_position(client_socket, player)
                send_position_cooldown = 10  # Enviar cada 10 frames (~166ms a 60 FPS)
            # ===== FI PROCESAR RED =====

            capaObjectes.fill((0, 0, 0, 0), camera_player)

            spawn_asteroids(8)
            anti_camperos(ernesto=players)
            wormholes.update()
            planetas.update()
            asteroids.update()
            #explosions.update()
            #bullets.update()
            players.update()
            if player.muerto:
                DONDE = "JUEGOACABADO"
            other_players_group.update()

            #fletxas.update()
            #cohets.update()

            mostrarTot(camera_player)

            drawVidas(player)

            comprovar_guanyador()
            #drawFletxas(camera_player1, camera_player2)
            misilsCooldown(player)

            screen.blit(playerScreen, (0, 0))
            minimapaDraw()

            # Update all sprites (reads keyboard state inside Players.update)

            camera_player.center = player.rect.center
            areaGran.center = camera_player.center

            camera_player.clamp_ip(rect_mapa)
            areaGran.clamp_ip(rect_mapa)

            playerScreen.blit(mapa.subsurface(camera_player), (0, 0))
            playerScreen.blit(capaObjectes.subsurface(camera_player), (0, 0))

        case "JUEGOACABADO":

            if cooldown <= 0:
                if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    seleccion = not seleccion
                    seleccionar.play()
                    cooldown = 500

            cooldown -= clock.get_time()

            if keys[pygame.K_RETURN] and not enterPresionado:
                #puntuacionFinal.join()
                if seleccion:
                    DONDE = "INICIO"
                    pygame.mixer.music.fadeout(2000)
                    control_musica("menu")
                    enterPresionado = True

                else:
                    running = False
                    continue
            else:
                if not keys[pygame.K_RETURN]:
                    enterPresionado = False

            # Mover fondo
            moverFondo()

            screen.blit(podio, pos_podio)

            # Scale player ships for the podium
            screen.blit(navePodioPerd, (pos_podio[0] + podio.get_width() // 4 , pos_podio[1] - podio.get_height() // 2 - 55))


            if len(guanyador) < 8:
                crearPalabras(guanyador + " WINS!",WIDTH//20,WIDTH//24)
            else:
                crearPalabras(guanyador + " WINS!",(11/12*WIDTH)// (len(guanyador) + 8),WIDTH//24)
            # Dibujar botones
            if seleccion == 1:
                boton_sel, pos_sel = boton_iralmenu_sel, pos_boton_iralmenu_sel_victoria
                screen.blit(boton_sel, pos_sel)
                screen.blit(boton_salir, pos_boton_salir_victoria)
            else:
                boton_sel, pos_sel = boton_salir_sel, pos_boton_salir_sel_victoria
                screen.blit(boton_sel, pos_sel)
                screen.blit(boton_iralmenu, pos_boton_iralmenu_victoria)

            # Dibujar flechas
            screen.blit(flecha_izq, (pos_sel[0] - flecha_izq.get_width() - 30, pos_sel[1] + boton_sel.get_height() // 2 - flecha_izq.get_height() // 2))
            screen.blit(flecha_der, (pos_sel[0] + boton_sel.get_width() + 30, pos_sel[1] + boton_sel.get_height() // 2 - flecha_der.get_height() // 2))

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()

# ===== LIMPIAR RED =====
if client_socket is not None:
    stop_event.set()
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    client_socket.close()
# ===== FI LIMPIAR RED =====
