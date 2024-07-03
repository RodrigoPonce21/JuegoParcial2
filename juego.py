import pygame
import sys
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
    tiempo_siguiente_power_up = pygame.time.get_ticks() + 15000  # 10 segundos

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
            tiempo_siguiente_power_up = tiempo_actual + 10000  # 10 segundos

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

def mostrar_menu_principal():
    pantalla.blit(fondo_menu_principal, (0, 0))
    fuente = pygame.font.SysFont(None, 62)
    texto = fuente.render("Seleccione la velocidad de caída", True, BLANCO)
    pantalla.blit(texto, (ANCHO_PANTALLA / 2 - texto.get_width() / 2, 100))
    
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
        pantalla.blit(texto, (ANCHO_PANTALLA / 2 - texto.get_width() / 2, 100))

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

if __name__ == "__main__":
    main()
