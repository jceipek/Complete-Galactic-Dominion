import pygame

pygame.mixer.init()
testSound = pygame.mixer.Sound('Borealis.ogg')

testSound.play(loops=-1)

while True:
    pass
