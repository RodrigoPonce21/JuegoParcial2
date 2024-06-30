import csv
import operator
from configuraciones import *

# Define la clase Jugador que hereda de pygame.sprite.Sprite
class Jugador(pygame.sprite.Sprite):
    # Inicializa el jugador con la imagen, posición, velocidad y otras propiedades
    def __init__(self, juego):
        super().__init__()
        self.image = imagen_jugador
        self.rect = self.image.get_rect()
        self.rect.centerx = RECTANGULO_AREA_JUEGO.centerx
        self.rect.centery = RECTANGULO_AREA_JUEGO.bottom - 50
        self.velocidad = 5
        self.juego = juego
        self.puede_disparar = True
        self.tiempo_disparo = 0
        self.doble_disparo = False
        self.tiempo_power_up = 0

    # Actualiza la posición del jugador y maneja el disparo y los power-ups
    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_SPACE] and self.puede_disparar:
            self.disparar()
            self.puede_disparar = False
            self.tiempo_disparo = pygame.time.get_ticks()

        # Verificar si el jugador se sale del rectángulo de límite
        if not RECTANGULO_AREA_JUEGO.contains(self.rect):
            self.rect.clamp_ip(RECTANGULO_AREA_JUEGO)

        # Verificar si ha pasado el tiempo de disparo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_disparo >= 500:  # 500 ms = 0.5 seg
            self.puede_disparar = True

        # Verificar si ha pasado el tiempo del power up
        if self.doble_disparo:
            if tiempo_actual > self.tiempo_power_up:
                self.doble_disparo = False

    # Dispara una bala o dos si tiene el power-up de doble disparo
    def disparar(self):
        if self.doble_disparo:
            bala1 = Bala(self.rect.centerx - 15, self.rect.top)
            bala2 = Bala(self.rect.centerx + 15, self.rect.top)
            self.juego.all_sprites.add(bala1)
            self.juego.all_sprites.add(bala2)
            self.juego.balas.add(bala1)
            self.juego.balas.add(bala2)
        else:
            bala = Bala(self.rect.centerx, self.rect.top)
            self.juego.all_sprites.add(bala)
            self.juego.balas.add(bala)
        sonido_disparo.play()

    # Recoge un power-up y activa su efecto
    def recoger(self, power_up):
        if power_up.tipo == "doble_disparo":
            self.doble_disparo = True
            self.tiempo_power_up = pygame.time.get_ticks() + power_up.duracion

# Define la clase Enemigo que hereda de pygame.sprite.Sprite
class Enemigo(pygame.sprite.Sprite):
    # Inicializa el enemigo con la imagen, posición, velocidad y juego
    def __init__(self, juego):
        super().__init__()
        self.image = imagen_enemigo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(RECTANGULO_AREA_JUEGO.left, RECTANGULO_AREA_JUEGO.right - TAMANO_ENEMIGO)
        self.rect.y = random.randint(-100, -10)
        self.velocidad = 1
        self.juego = juego

    # Actualiza la posición del enemigo y resta una vida al jugador si llega al fondo
    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y == (RECTANGULO_AREA_JUEGO.bottom - 40):
            self.juego.vidas -= 1  # Restar una vida al jugador
            self.kill() # Eliminar el enemigo

        # Verificar si el enemigo se sale del rectángulo de límite
        if not RECTANGULO_AREA_JUEGO.contains(self.rect):
            self.rect.clamp_ip(RECTANGULO_AREA_JUEGO)

# Define la clase Bala que hereda de pygame.sprite.Sprite
class Bala(pygame.sprite.Sprite):
    # Inicializa la bala con la imagen, posición y velocidad
    def __init__(self, x, y):
        super().__init__()
        self.image = imagen_bala
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 5

    # Actualiza la posición de la bala y la elimina si sale de la pantalla
    def update(self):
        self.rect.y -= self.velocidad
        if self.rect.y < 0:
            self.kill()

# Define la clase PowerUp que hereda de pygame.sprite.Sprite
class PowerUp(pygame.sprite.Sprite):
    # Inicializa el power-up con la imagen, posición, velocidad, tipo y duración
    def __init__(self, juego):
        super().__init__()
        self.image = imagen_power_up
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(RECTANGULO_AREA_JUEGO.left, RECTANGULO_AREA_JUEGO.right - 20)
        self.rect.y = random.randint(-100, -10)
        self.velocidad = 2
        self.juego = juego
        self.tipo = "doble_disparo"
        self.duracion = 5000  # 5 segundos

    # Actualiza la posición del power-up y lo elimina si sale de la pantalla
    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > RECTANGULO_AREA_JUEGO.bottom:
            self.kill()

# Define la función para guardar la puntuación en un archivo CSV
def guardar_puntuacion(puntuacion):
    ruta_archivo = "./Juego Parcial 2/puntuacion.csv"
    datos = [{"Puntuación": puntuacion}]
    with open(ruta_archivo, "a", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["Puntuación"])
        if archivo.tell() == 0:
            writer.writeheader()
        writer.writerows(datos)

    # Leer y ordenar el archivo CSV
    with open(ruta_archivo, "r") as archivo:
        reader = csv.DictReader(archivo)
        datos = [row for row in reader]
        datos.sort(key=operator.itemgetter("Puntuación"), reverse=True)

    # Sobreescribir el archivo CSV con los datos ordenados
    with open(ruta_archivo, "w", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["Puntuación"])
        writer.writeheader()
        writer.writerows(datos)