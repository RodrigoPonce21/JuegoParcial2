import csv
from configuraciones import *

class Jugador(pygame.sprite.Sprite):
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

    def recoger(self, power_up):
        if power_up.tipo == "doble_disparo":
            self.doble_disparo = True
            self.tiempo_power_up = pygame.time.get_ticks() + power_up.duracion

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, juego):
        super().__init__()
        self.image = imagen_enemigo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(RECTANGULO_AREA_JUEGO.left, RECTANGULO_AREA_JUEGO.right - TAMANO_ENEMIGO)
        self.rect.y = random.randint(-100, -10)
        self.velocidad = 1
        self.juego = juego

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y == (RECTANGULO_AREA_JUEGO.bottom - 40):
            self.juego.vidas -= 1  # Restar una vida al jugador
            self.kill() # Eliminar el enemigo

        # Verificar si el enemigo se sale del rectángulo de límite
        if not RECTANGULO_AREA_JUEGO.contains(self.rect):
            self.rect.clamp_ip(RECTANGULO_AREA_JUEGO)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = imagen_bala
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 5

    def update(self):
        self.rect.y -= self.velocidad
        if self.rect.y < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
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

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > RECTANGULO_AREA_JUEGO.bottom:
            self.kill()


def guardar_puntuacion(puntuacion):
    ruta_archivo = "./Juego Parcial 2/puntuacion.csv"
    datos = [{"Puntuación": puntuacion}]
    with open(ruta_archivo, "a", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=["Puntuación"])
        if archivo.tell() == 0:
            writer.writeheader()
        writer.writerows(datos)