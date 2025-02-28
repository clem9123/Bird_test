import pygame
import os

def jouer_son(fichier):
    chemin_complet = os.path.join("data", fichier)
    if os.path.exists(chemin_complet):
        pygame.mixer.init()
        pygame.mixer.music.load(chemin_complet)
        pygame.mixer.music.play()

def arreter_son():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
