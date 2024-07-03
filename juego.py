import pygame
import random
from configuraciones import *
from funciones import *

def main():
    velocidad_caida = mostrar_menu_principal()
    
    jugador = inicializar_jugador()
    all_sprites = [jugador]
    enemigos = []
    balas = []
    power_ups = []
    juego = {"vidas": 3, "puntuacion": 0}

    # Temporizador para el power-up
    tiempo_siguiente_power_up = pygame.time.get_ticks() + 15000  # 15 segundos

    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        actualizar_jugador(jugador, all_sprites, balas)

        for bala in list(balas):
            if not actualizar_bala(bala):
                balas.remove(bala)
                all_sprites.remove(bala)

        if random.random() < 0.02:
            enemigo = crear_enemigo()
            enemigo["velocidad"] = velocidad_caida
            enemigos.append(enemigo)
            all_sprites.append(enemigo)

        for enemigo in list(enemigos):
            if not actualizar_enemigo(enemigo, juego):
                enemigos.remove(enemigo)
                all_sprites.remove(enemigo)
                if juego["vidas"] <= 0:
                    corriendo = False
                    mostrar_pantalla_game_over(juego)

        # Comprobar si es momento de generar un nuevo power-up
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual >= tiempo_siguiente_power_up:
            power_up = crear_power_up()
            power_ups.append(power_up)
            all_sprites.append(power_up)
            tiempo_siguiente_power_up = tiempo_actual + 15000  # 15 segundos

        for power_up in list(power_ups):
            if not actualizar_power_up(power_up):
                power_ups.remove(power_up)
                all_sprites.remove(power_up)
            elif jugador["rect"].colliderect(power_up["rect"]):
                recoger_power_up(jugador, power_up)
                power_ups.remove(power_up)
                all_sprites.remove(power_up)

        for enemigo in list(enemigos):
            if jugador["rect"].colliderect(enemigo["rect"]):
                sonido_explosion.play()
                juego["vidas"] -= 1
                enemigos.remove(enemigo)
                all_sprites.remove(enemigo)
                if juego["vidas"] <= 0:
                    corriendo = False
                    mostrar_pantalla_game_over(juego)

        for bala in list(balas):
            for enemigo in list(enemigos):
                if bala["rect"].colliderect(enemigo["rect"]):
                    sonido_explosion.play()
                    juego["puntuacion"] += 100
                    balas.remove(bala)
                    enemigos.remove(enemigo)
                    all_sprites.remove(bala)
                    all_sprites.remove(enemigo)
                    break

        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, BLANCO, RECTANGULO_AREA_JUEGO, 2)
        for sprite in all_sprites:
            pantalla.blit(sprite["image"], sprite["rect"])

        mostrar_puntuacion(juego["puntuacion"])
        mostrar_vida(juego["vidas"])
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    guardar_puntuacion(juego["puntuacion"])

if __name__ == "__main__":
    main()
