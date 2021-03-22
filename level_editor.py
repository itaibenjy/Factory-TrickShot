import pygame
import os
from world import World
from character import Character
from weapon import Weapons
from data import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BULLET_VEL, BLOCKS, BLOCKS_POS
import csv_handler


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH+100, SCREEN_HEIGHT))
pygame.display.set_caption('Factory Trick-Shot Level Editor')
clock = pygame.time.Clock()
world = World(screen)
character = Character(bottomleftpos=(200, 200))
weapons = Weapons()
delay = 20


def drawTiles():
    start_x = 1200
    block = 1
    for i in range(12):
        for j in range(2):
            try:
                if block <= 2:
                    screen.blit(BLOCKS[block], (start_x + j*50, i*50))
                elif block == 10 or block == 7:
                    screen.blit(BLOCKS[block], (start_x + j*50, i*50))
                elif block == 8:
                    screen.blit(BLOCKS[block][0], (start_x + j*50, i*50-50))
                else:
                    screen.blit(BLOCKS[block][0], (start_x + j*50, i*50))
            except:
                pass
            block += 1
    screen.blit(pygame.image.load(os.path.join('images', 'save.png')), (1250, 750))
    screen.blit(BLOCKS[100],(1200,750))


def draw_lines():
    for i in range(SCREEN_HEIGHT//50):
        pygame.draw.line(screen, (0, 0, 0), (0, i*50), (SCREEN_WIDTH, i*50), 1)
    for i in range(SCREEN_WIDTH//50):
        pygame.draw.line(screen, (0, 0, 0), (i*50, 0), (i*50, SCREEN_WIDTH), 1)


def select_block():
    global delay
    if delay > 0:
        delay -= 1
    keys = pygame.mouse.get_pressed(num_buttons=3)
    pos = pygame.mouse.get_pos()
    x = pos[0]//50
    y = pos[1]//50
    if keys[0]:
        if pos[0] > 1200:
            for key in BLOCKS_POS:
                if BLOCKS_POS[key][0] == x*50 and BLOCKS_POS[key][1] == y*50:
                    return key
    if x*50 == 1250 and y*50 == 750 and keys[0] and delay == 0:
        saveFile()
    if x * 50 == 1200 and y * 50 == 750 and keys[0] and delay == 0:
        return 100
    return 0


def saveFile():
    global delay
    delay = 20
    mat = world.level
    level = 0
    for i in range(100):
        try:
            open(os.path.join('levels', f"level_{i}.csv"))
        except FileNotFoundError:
            level = i
            break
    csv_handler.matrixToCsv(mat, level)


def main():
    block = 1
    bg_surface = pygame.image.load(os.path.join(
        'images', 'background_blue.png')).convert()
    bg_surface = pygame.transform.scale(bg_surface, (1200, 800))
    mode = 'build'

    # Main loop
    while True:
        screen.blit(bg_surface, (0, 0))
        
        if mode == 'build':
            drawTiles()
            draw_lines()

            temp = select_block()
            block = temp if temp != 0 else block

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                weapons.choose_weapon(keys_pressed, character)
                if event.key == pygame.K_SPACE:
                    mode = 'play'
                    world.updateTileRect()
                if event.key == pygame.K_ESCAPE:
                    mode = 'build'
        if mode == 'build':        
            select_block()
            world.add(screen, block)
        if mode == 'play':
            world.drawLevel(screen)
            character.display(screen, pygame.mouse.get_pos())
            keys_pressed = pygame.key.get_pressed()
            character.move(keys_pressed, world)
            weapons.displayAndUpdate(screen, world)
            weapons.toShoot(character, screen)
            world.animationController()

        world.update(screen, character, weapons)
        

        
        pygame.display.update()
        clock.tick(FPS)


main()
