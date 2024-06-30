import pygame
from configuraciones import *
from funciones import *

class Juego:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.vidas = 3
        self.puntuacion = 0
        self.tiempo_enemigo = 0
        self.tiempo_power_up = 0
        self.menu = True
        self.velocidad_enemigo = 1

    def start(self):
        self.jugador = Jugador(self)
        self.all_sprites.add(self.jugador)
        for _ in range(5):
            enemigo = Enemigo(self)
            enemigo.velocidad = self.velocidad_enemigo  # Actualizar velocidad de los enemigos
            self.all_sprites.add(enemigo)
            self.enemigos.add(enemigo)

    def update(self):
        self.all_sprites.update()
        golpes = pygame.sprite.groupcollide(self.enemigos, self.balas, True, True)
        for golpe in golpes:
            self.puntuacion += 1
            sonido_explosion.play()
        golpes = pygame.sprite.spritecollide(self.jugador, self.enemigos, True)
        for golpe in golpes:
            self.vidas -= 1
            sonido_explosion.play()
        golpes = pygame.sprite.spritecollide(self.jugador, self.power_ups, True)
        for golpe in golpes:
            self.jugador.recoger(golpe)

        if self.vidas <= 0:
            self.game_over()

        # Respawn enemigos
        self.tiempo_enemigo -= 1
        if self.tiempo_enemigo <= 0:
            self.tiempo_enemigo = 25  # Respawn every X frames
            if len(self.enemigos) < 7:  # Limit to X enemies on screen
                enemigo = Enemigo(self)
                enemigo.velocidad = self.velocidad_enemigo  # Actualizar velocidad de los enemigos
                self.all_sprites.add(enemigo)
                self.enemigos.add(enemigo)

        # Respawn power-ups
        self.tiempo_power_up -= 1
        if self.tiempo_power_up <= 0:
            self.tiempo_power_up = 200  # Respawn every X frames
            if len(self.power_ups) < 1:  # Limit to X power-ups on screen
                power_up = PowerUp(self)
                self.all_sprites.add(power_up)
                self.power_ups.add(power_up)

    def draw(self):
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, BLANCO, RECTANGULO_AREA_JUEGO, 1)
        self.all_sprites.draw(pantalla)
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Vidas: {self.vidas} ", True, BLANCO)
        texto2 = fuente.render(f"Puntuación: {self.puntuacion} ", True, BLANCO)
        pantalla.blit(texto, (10, 10))
        pantalla.blit(texto2, (10, 40))
        pygame.display.flip()

    def run(self):
        bandera = 0    
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.velocidad_enemigo = min(self.velocidad_enemigo + 0.5, 5)
                        for enemigo in self.enemigos:
                            enemigo.velocidad = self.velocidad_enemigo
                    elif event.key == pygame.K_DOWN:
                        self.velocidad_enemigo = max(self.velocidad_enemigo - 0.5, 0.5)
                        for enemigo in self.enemigos:
                            enemigo.velocidad = self.velocidad_enemigo
                    elif event.key == pygame.K_RETURN:
                        self.menu = False
                        self.start()

            if bandera == 0:
                sonido_menu.play()
                bandera = 1
            
            pantalla.blit(fondo_menu_principal, (0, 0))
            fuente = pygame.font.Font(None, 30)
            texto2 = fuente.render("Presiona Enter para empezar", True, BLANCO)
            pantalla.blit(texto2, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 3 - 50))
            texto3 = fuente.render("Usa las flechas arriba y abajo para ajustar la velocidad de los enemigos", True, BLANCO)
            pantalla.blit(texto3, (ANCHO_PANTALLA / 3 - 200, ALTO_PANTALLA / 3))
            texto = fuente.render(f"Velocidad de los enemigos: {int(self.velocidad_enemigo)}", True, BLANCO)
            pantalla.blit(texto, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 3 + 50))
            pygame.display.update()
            pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw()
            reloj.tick(60)

    def game_over(self):
        pantalla.fill(NEGRO)
        fuente = pygame.font.Font(None, 64)
        texto = fuente.render("JUEGO TERMINADO", True, BLANCO)
        pantalla.blit(texto, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 - 50))
        texto = fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        pantalla.blit(texto, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 + 50))
        pygame.display.flip()
        
        # Guardar puntuación en archivo
        guardar_puntuacion(self.puntuacion)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    juego = Juego()
    juego.run()