# -*- coding: utf-8 -*-

# 32 20 41 / 39 20 41
# main: Contient loop

# Ecrivez une description de ce que vous codez
# avec votre pseudo pour qu'on puisse vous demander plus d'infos -tremisabdoul

# Importe les fichier Classes Functions pygame et time -tremisabdoul
from Scripts.Functions import *
from Scripts.Classes import *
import time
'''==================================='''

pygame.init()


# Execute les Classes -tremisabdoul
Game = Game()
Game.init_suite()
Music_Init()

# Valeurs qui vont servir plus tard
# (faites gaffe les valeurs peuvent faire crash le jeu si vous en supprimez certeines) -tremisabdoul
x = 0
frame = 0
nbframe = 0

# L'écran est stockée dans une variable -tremisabdoul
Screen = Display()

# Définit les polices -tremisabdoul
police1 = pygame.font.Font("Assets/Font/Retro Gaming.ttf", 10)

police2 = pygame.font.Font("Assets/Font/Retro Gaming.ttf", 20)

Paterns(Game)

# Random Plateform
for _ in range(100):
    from random import randint

    x = randint(0, 100)
    y = randint(1, 5)
    NewPlatform(Game, x, y - 1)
    NewWall(Game, x, y)

    del randint

'''==================================='''

# Contient tout ce qui est fait pendant que le jeu est run -tremisabdoul
while Game.Running:
    """ ===== Loop ===== """
    # Loop du Lobby
    if Game.Lobby:
        Lobby(Game, Screen, time, police1)

    # Loop de pause [Escape]
    if Game.Pause:
        pause(Game, Screen, time, police1)

    # Loop de jeu
    if Game.InGame:
        MusicTime = pygame.mixer.music.get_pos() / 1000
        pygame.mixer.music.load("Assets/Audio/Music/DANOARKI.mp3")
        pygame.mixer.music.rewind()
        pygame.mixer.music.play(-1, MusicTime)
        inGame(Game, time, Screen, police1)

    MusicTime = pygame.mixer.music.get_pos() / 1000
    pygame.mixer.music.load("Assets/Audio/Music/DANOARKI.mp3")
    pygame.mixer.music.rewind()
    pygame.mixer.music.play(-1, MusicTime)

    if Game.Option:
        Option(Game, Screen, time, police1, police2)
