import pygame
import random
import json

# Constantes
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 700
ANCHO_AREA_JUEGO = 360
ALTO_AREA_JUEGO = 580
TAMAÑO_JUGADOR = 25
TAMAÑO_ENEMIGO = 25
TAMAÑO_BALA = 5

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Galaga")
reloj = pygame.time.Clock()

# Leer el archivo JSON
with open('./Juego Parcial 2/archivos.json', 'r') as file:
    ubicacion = json.load(file)

# Cargar imágenes
imagen_jugador = pygame.image.load(ubicacion["imagenes"]["jugador"])
imagen_jugador = pygame.transform.scale(imagen_jugador, (TAMAÑO_JUGADOR, TAMAÑO_JUGADOR))

imagen_enemigo = pygame.image.load(ubicacion["imagenes"]["enemigo"])
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (TAMAÑO_ENEMIGO, TAMAÑO_ENEMIGO))

imagen_bala = pygame.Surface((TAMAÑO_BALA, TAMAÑO_BALA))
imagen_bala.fill(BLANCO)

imagen_power_up = pygame.Surface((20, 20))
imagen_power_up.fill(BLANCO)

fondo_menu_principal = pygame.image.load(ubicacion["imagenes"]["main_menu_background"])
fondo_menu_principal = pygame.transform.scale(fondo_menu_principal, (ANCHO_PANTALLA, ALTO_PANTALLA))

fondo_juego = pygame.image.load(ubicacion["imagenes"]["game_background"])
fondo_juego = pygame.transform.scale(fondo_juego, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Cargar sonidos
sonido_disparo = pygame.mixer.Sound(ubicacion["sonidos"]["disparo"])
sonido_explosion = pygame.mixer.Sound(ubicacion["sonidos"]["explosion"])
sonido_menu = pygame.mixer.Sound(ubicacion["sonidos"]["menu_background"])

# Definir el rectángulo de límite
RECTANGULO_AREA_JUEGO = pygame.Rect(ANCHO_PANTALLA / 2 - ANCHO_AREA_JUEGO / 2, ALTO_PANTALLA / 2 - ALTO_AREA_JUEGO / 2, ANCHO_AREA_JUEGO, ALTO_AREA_JUEGO)

# Resto del código del juego...
