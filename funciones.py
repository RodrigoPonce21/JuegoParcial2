import pygame
import random
import csv
from configuraciones import *

def inicializar_jugador():
    jugador = {
        "image": imagen_jugador,
        "rect": imagen_jugador.get_rect(),
        "velocidad": 5,
        "puede_disparar": True,
        "tiempo_disparo": 0,
        "doble_disparo": False,
        "tiempo_power_up": 0
    }
    jugador["rect"].centerx = RECTANGULO_AREA_JUEGO.centerx
    jugador["rect"].centery = RECTANGULO_AREA_JUEGO.bottom - 50
    return jugador

def crear_enemigo():
    enemigo = {
        "image": imagen_enemigo,
        "rect": imagen_enemigo.get_rect(),
        "velocidad": 1,
        "direccion": random.randint(-1, 1)  # 1 para moverse hacia la derecha, -1 para moverse hacia la izquierda
    }
    enemigo["rect"].x = random.randint(RECTANGULO_AREA_JUEGO.left, RECTANGULO_AREA_JUEGO.right - TAMANO_ENEMIGO)
    enemigo["rect"].y = RECTANGULO_AREA_JUEGO.top
    return enemigo

def mover_enemigo(enemigo):
    # Mover en la dirección actual
    enemigo["rect"].x += enemigo["velocidad"] * enemigo["direccion"]

    # Verificar si alcanza los límites izquierdo o derecho
    if enemigo["rect"].right >= RECTANGULO_AREA_JUEGO.right:
        enemigo["direccion"] = -1  # Cambiar dirección hacia la izquierda
    elif enemigo["rect"].left <= RECTANGULO_AREA_JUEGO.left:
        enemigo["direccion"] = 1  # Cambiar dirección hacia la derecha

def crear_bala(x, y):
    bala = {
        "image": imagen_bala,
        "rect": imagen_bala.get_rect(),
        "velocidad": 5
    }
    bala["rect"].x = x
    bala["rect"].y = y
    return bala

def crear_power_up():
    power_up = {
        "image": imagen_power_up,
        "rect": imagen_power_up.get_rect(),
        "velocidad": 2,
        "tipo": "doble_disparo",
        "duracion": 5000  # 5 segundos
    }
    power_up["rect"].x = random.randint(RECTANGULO_AREA_JUEGO.left, RECTANGULO_AREA_JUEGO.right - 20)
    power_up["rect"].y = RECTANGULO_AREA_JUEGO.top
    return power_up

def actualizar_jugador(jugador, all_sprites, balas):
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador["rect"].x -= jugador["velocidad"]
    if teclas[pygame.K_RIGHT]:
        jugador["rect"].x += jugador["velocidad"]
    if teclas[pygame.K_SPACE] and jugador["puede_disparar"]:
        disparar(jugador, all_sprites, balas)
        jugador["puede_disparar"] = False
        jugador["tiempo_disparo"] = pygame.time.get_ticks()

    if not RECTANGULO_AREA_JUEGO.contains(jugador["rect"]):
        jugador["rect"].clamp_ip(RECTANGULO_AREA_JUEGO)

    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - jugador["tiempo_disparo"] >= 500:
        jugador["puede_disparar"] = True

    if jugador["doble_disparo"] and tiempo_actual > jugador["tiempo_power_up"]:
        jugador["doble_disparo"] = False

def disparar(jugador, all_sprites, balas):
    if jugador["doble_disparo"]:
        bala1 = crear_bala(jugador["rect"].centerx - 15, jugador["rect"].top)
        bala2 = crear_bala(jugador["rect"].centerx + 15, jugador["rect"].top)
        all_sprites.append(bala1)
        all_sprites.append(bala2)
        balas.append(bala1)
        balas.append(bala2)
    else:
        bala = crear_bala(jugador["rect"].centerx, jugador["rect"].top)
        all_sprites.append(bala)
        balas.append(bala)
    sonido_disparo.play()

def actualizar_enemigo(enemigo, juego):
    enemigo["rect"].y += enemigo["velocidad"]
    if enemigo["rect"].y >= RECTANGULO_AREA_JUEGO.bottom - 40:
        juego["vidas"] -= 1
        return False
    if not RECTANGULO_AREA_JUEGO.contains(enemigo["rect"]):
        enemigo["rect"].clamp_ip(RECTANGULO_AREA_JUEGO)
    return True

def actualizar_bala(bala):
    bala["rect"].y -= bala["velocidad"]
    if bala["rect"].y < 0:
        return False
    return True

def actualizar_power_up(power_up):
    power_up["rect"].y += power_up["velocidad"]
    if power_up["rect"].y > RECTANGULO_AREA_JUEGO.bottom:
        return False
    return True

def recoger_power_up(jugador, power_up):
    if power_up["tipo"] == "doble_disparo":
        jugador["doble_disparo"] = True
        jugador["tiempo_power_up"] = pygame.time.get_ticks() + power_up["duracion"]
        
def mostrar_puntuacion(puntuacion):
    fuente = pygame.font.SysFont(None, 30)
    texto = fuente.render(f"Puntuación", True, ROJO)
    texto2 = fuente.render(str(puntuacion), True, BLANCO)
    pantalla.blit(texto, (250, 10))
    pantalla.blit(texto2, (300, 35))
    
def mostrar_vida(vida):
    fuente = pygame.font.SysFont(None, 30)
    texto = fuente.render(f"Vidas", True, ROJO)
    texto2 = fuente.render(str(vida), True, BLANCO)
    pantalla.blit(texto, (10, 10))
    pantalla.blit(texto2, (10, 35))
    
def mostrar_menu_principal():
    pantalla.blit(fondo_menu_principal, (0, 0))
    fuente = pygame.font.SysFont(None, 32)
    texto = fuente.render("Seleccione la velocidad de caída", True, BLANCO)
    
    fuente_pequena = pygame.font.SysFont(None, 36)
    opciones = ["1", "2", "3", "4", "5"]
    seleccion = 0
    espacio_entre_opciones = 50

    bandera_musica = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_RIGHT:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    return int(opciones[seleccion])

        pantalla.blit(fondo_menu_principal, (0, 0))
        pantalla.blit(texto, (ANCHO_PANTALLA / 2 - texto.get_width() / 2, 150))

        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else NEGRO
            texto_opcion = fuente_pequena.render(opcion, True, color)
            x_pos = ANCHO_PANTALLA / 2 - (len(opciones) * espacio_entre_opciones) / 2 + i * espacio_entre_opciones
            pantalla.blit(texto_opcion, (x_pos, 200))
            
        if bandera_musica == 0:
            bandera_musica = 1
            sonido_menu.play()
            
        pygame.display.flip()
        reloj.tick(60)

def mostrar_pantalla_game_over(juego):
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("GAME OVER", True, BLANCO)
    pantalla.blit(texto, (ANCHO_PANTALLA / 2 - texto.get_width() / 2, ALTO_PANTALLA / 2 - texto.get_height() / 2))
    fuente_pequena = pygame.font.SysFont(None, 36)
    texto_puntuacion = fuente_pequena.render(f"Puntuacion: {juego['puntuacion']}", True, BLANCO)
    pantalla.blit(texto_puntuacion, (ANCHO_PANTALLA / 2 - texto_puntuacion.get_width() / 2, ALTO_PANTALLA / 2 + texto.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def guardar_puntuacion(puntuacion):
    if puntuacion != 0:
        ruta_archivo = "./Juego Parcial 2/puntuacion.csv"
        datos = [{"Puntuacion": puntuacion}]
        
        # Guardar la nueva puntuación
        with open(ruta_archivo, "a", newline="") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=["Puntuacion"])
            if archivo.tell() == 0:
                writer.writeheader()
            writer.writerows(datos)

        # Leer todas las puntuaciones del archivo
        with open(ruta_archivo, "r") as archivo:
            reader = csv.DictReader(archivo)
            datos = [row for row in reader]

        # Ordenar las puntuaciones de mayor a menor
        datos.sort(key=lambda x: int(x["Puntuacion"]), reverse=True)

        # Sobreescribir el archivo CSV con los datos ordenados
        with open(ruta_archivo, "w", newline="") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=["Puntuacion"])
            writer.writeheader()
            writer.writerows(datos)
