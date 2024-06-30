import pygame
import sys
import random

# Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TAMANO_JUGADOR = 25
TAMANO_ENEMIGO = 25
TAMANO_BALA = 5

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Galaga")
reloj = pygame.time.Clock()

# Cargar imágenes (reemplazar con imágenes reales)
imagen_jugador = pygame.image.load("./Juego Parcial 2/jugador.png")
imagen_jugador = pygame.transform.scale(imagen_jugador, (TAMANO_JUGADOR, TAMANO_JUGADOR))

imagen_enemigo = pygame.image.load("./Juego Parcial 2/enemigo.png")
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (TAMANO_ENEMIGO, TAMANO_ENEMIGO))

imagen_bala = pygame.Surface((TAMANO_BALA, TAMANO_BALA))
imagen_bala.fill(BLANCO)

imagen_power_up = pygame.Surface((20, 20))
imagen_power_up.fill(BLANCO)

fondo_menu_principal = pygame.image.load("./Juego Parcial 2/main_menu_background.png")
fondo_menu_principal = pygame.transform.scale(fondo_menu_principal, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Cargar sonidos (reemplazar con sonidos reales)
sonido_disparo = pygame.mixer.Sound("./Juego Parcial 2/disparo.mp3")
sonido_explosion = pygame.mixer.Sound("./Juego Parcial 2/explosion.mp3")
sonido_menu = pygame.mixer.Sound("./Juego Parcial 2/background_music.wav")

# Cargar música de fondo (reemplazar con música real)
#pygame.mixer.music.load("")
#pygame.mixer.music.play(-1)

# Definir el rectángulo de límite
ANCHO_AREA_JUEGO = 360
ALTO_AREA_JUEGO = 580
RECTANGULO_AREA_JUEGO = pygame.Rect(ANCHO_PANTALLA / 2 - ANCHO_AREA_JUEGO / 2, ALTO_PANTALLA / 2 - ALTO_AREA_JUEGO / 2, ANCHO_AREA_JUEGO, ALTO_AREA_JUEGO)