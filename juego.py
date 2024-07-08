import pygame
from funciones import *
from ejecucion import *

def main():
    while True:
        # Mostrar el menú principal y obtener la velocidad de caída seleccionada
        velocidad_caida = mostrar_menu_principal()
        
        # Ejecutar el juego pasando la velocidad de caída seleccionada
        ejecutar_juego(velocidad_caida)

if __name__ == "__main__":
    main()
