import pygame
from configuraciones import *  # Importa las configuraciones del juego
from funciones import *  # Importa las funciones del juego

# Define la clase Juego
class Juego:
    # Inicializa el objeto Juego
    def __init__(self):
        # Inicializa los grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        # Inicializa las variables del juego
        self.vidas = 3
        self.puntuacion = 0
        self.tiempo_enemigo = 0  # Temporizador para el respawn de enemigos
        self.tiempo_power_up = 0  # Temporizador para el respawn de power-ups
        self.menu = True  # Bandera para mostrar el menú
        self.velocidad_enemigo = 1  # Velocidad inicial de los enemigos

    # Inicia el juego
    def start(self):
        # Crea el jugador
        self.jugador = Jugador(self)
        # Añade el jugador al grupo de sprites
        self.all_sprites.add(self.jugador)

        # Crea enemigos iniciales
        for _ in range(5):
            enemigo = Enemigo(self)
            # Actualiza la velocidad de los enemigos
            enemigo.velocidad = self.velocidad_enemigo 
            # Añade los enemigos al grupo de sprites
            self.all_sprites.add(enemigo)
            self.enemigos.add(enemigo)

    # Actualiza el juego
    def update(self):
        # Actualiza los sprites
        self.all_sprites.update()

        # Comprueba colisiones entre balas y enemigos
        golpes = pygame.sprite.groupcollide(self.enemigos, self.balas, True, True)
        # Si hay colisiones, aumenta la puntuación y reproduce un sonido
        for golpe in golpes:
            self.puntuacion += 1
            sonido_explosion.play()

        # Comprueba colisiones entre el jugador y enemigos
        golpes = pygame.sprite.spritecollide(self.jugador, self.enemigos, True)
        # Si hay colisiones, resta una vida y reproduce un sonido
        for golpe in golpes:
            self.vidas -= 1
            sonido_explosion.play()

        # Comprueba colisiones entre el jugador y power-ups
        golpes = pygame.sprite.spritecollide(self.jugador, self.power_ups, True)
        # Si hay colisiones, el jugador recoge el power-up
        for golpe in golpes:
            self.jugador.recoger(golpe)

        # Game Over si el jugador se queda sin vidas
        if self.vidas <= 0:
            self.game_over()

        # Respawn de enemigos
        self.tiempo_enemigo -= 1
        if self.tiempo_enemigo <= 0:
            # Respawn cada X frames
            self.tiempo_enemigo = 25
            # Limita la cantidad de enemigos en pantalla
            if len(self.enemigos) < 7: 
                enemigo = Enemigo(self)
                # Actualiza la velocidad de los enemigos
                enemigo.velocidad = self.velocidad_enemigo 
                # Añade el nuevo enemigo al grupo de sprites
                self.all_sprites.add(enemigo)
                self.enemigos.add(enemigo)

        # Respawn de power-ups
        self.tiempo_power_up -= 1
        if self.tiempo_power_up <= 0:
            # Respawn cada X frames
            self.tiempo_power_up = 200
            # Limita la cantidad de power-ups en pantalla
            if len(self.power_ups) < 1:
                power_up = PowerUp(self)
                # Añade el nuevo power-up al grupo de sprites
                self.all_sprites.add(power_up)
                self.power_ups.add(power_up)

    # Dibuja el juego
    def draw(self):
        # Rellena la pantalla con negro
        pantalla.fill(NEGRO)
        # Dibuja el rectángulo del área de juego
        pygame.draw.rect(pantalla, BLANCO, RECTANGULO_AREA_JUEGO, 1)
        # Dibuja los sprites
        self.all_sprites.draw(pantalla)

        # Dibuja las vidas y la puntuación
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Vidas: {self.vidas} ", True, BLANCO)
        texto2 = fuente.render(f"Puntuación: {self.puntuacion} ", True, BLANCO)
        pantalla.blit(texto, (10, 10))
        pantalla.blit(texto2, (10, 40))

        # Actualiza la pantalla
        pygame.display.flip()

    # Ejecuta el juego
    def run(self):
        # Bandera para el sonido del menú
        bandera = 0    
        # Bucle del menú principal
        while self.menu:
            # Maneja los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Ajusta la velocidad de los enemigos con las flechas
                    if event.key == pygame.K_UP:
                        self.velocidad_enemigo = min(self.velocidad_enemigo + 0.5, 5)
                        for enemigo in self.enemigos:
                            enemigo.velocidad = self.velocidad_enemigo
                    elif event.key == pygame.K_DOWN:
                        self.velocidad_enemigo = max(self.velocidad_enemigo - 0.5, 0.5)
                        for enemigo in self.enemigos:
                            enemigo.velocidad = self.velocidad_enemigo
                    # Inicia el juego si se presiona Enter
                    elif event.key == pygame.K_RETURN:
                        self.menu = False
                        self.start()

            # Reproduce el sonido del menú una vez
            if bandera == 0:
                sonido_menu.play()
                bandera = 1
            
            # Dibuja el menú principal
            pantalla.blit(fondo_menu_principal, (0, 0))
            fuente = pygame.font.Font(None, 30)
            texto2 = fuente.render("Presiona Enter para empezar", True, BLANCO)
            pantalla.blit(texto2, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 3 - 50))
            texto3 = fuente.render("Usa las flechas arriba y abajo para ajustar la velocidad de los enemigos", True, BLANCO)
            pantalla.blit(texto3, (ANCHO_PANTALLA / 3 - 200, ALTO_PANTALLA / 3))
            texto = fuente.render(f"Velocidad de los enemigos: {int(self.velocidad_enemigo)}", True, BLANCO)
            pantalla.blit(texto, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 3 + 50))
            # Actualiza la pantalla
            pygame.display.update()
            pygame.display.flip()
        
        # Bucle del juego principal
        while True:
            # Maneja los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Actualiza y dibuja el juego
            self.update()
            self.draw()

            # Limita la frecuencia de fotogramas
            reloj.tick(60)

    # Game Over
    def game_over(self):
        # Dibuja la pantalla de Game Over
        pantalla.fill(NEGRO)
        fuente = pygame.font.Font(None, 64)
        texto = fuente.render("JUEGO TERMINADO", True, BLANCO)
        pantalla.blit(texto, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 - 50))
        texto = fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        pantalla.blit(texto, (ANCHO_PANTALLA / 2 - 150, ALTO_PANTALLA / 2 + 50))
        pygame.display.flip()
        
        # Guarda la puntuación en un archivo
        guardar_puntuacion(self.puntuacion)
        
        # Bucle de la pantalla de Game Over
        while True:
            # Maneja los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# Ejecuta el juego si el script se ejecuta directamente
if __name__ == "__main__":
    juego = Juego()
    juego.run()