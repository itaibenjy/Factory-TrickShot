import csv_handler
import pygame
import sys
import os
import random
from character import Character
from weapon import Weapons
from world import World
from data import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BULLET_VEL, BLOCKS, CURSOR, MENU_FONT
from animation import DoorTransition

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags= pygame.RESIZABLE)
clock = pygame.time.Clock()
world = World(screen)
pygame.mouse.set_visible(False)
doorAnimation = DoorTransition()
pygame.display.set_caption('Factory Trick-Shot')
icon = pygame.transform.scale(pygame.image.load(
    os.path.join('images', 'icon.png')), (32, 32))
pygame.display.set_icon(icon)


def cursorChange():
    cursor_rect = CURSOR.get_rect(center=pygame.mouse.get_pos())
    screen.blit(CURSOR, cursor_rect)


def draw_lines():
    for i in range(SCREEN_HEIGHT//50):
        pygame.draw.line(screen, (0, 0, 0), (0, i*50), (SCREEN_WIDTH, i*50), 1)
    for i in range(SCREEN_WIDTH//50):
        pygame.draw.line(screen, (0, 0, 0), (i*50, 0), (i*50, SCREEN_WIDTH), 1)


def main():
    world.updateLevel()
    bg_surface = pygame.image.load(os.path.join(
        'images', 'background_blue.png')).convert()
    bg_surface = pygame.transform.scale(bg_surface, (1200, 800))

    character = Character(bottomleftpos=(world.charpos))
    weapons = Weapons()

    # Main loop
    while True:
        screen.blit(bg_surface, (0, 0))
        world.drawLevel(screen)
        character.display(screen, pygame.mouse.get_pos())
        more_levels = world.update(screen, character, weapons)
        if not more_levels:
            world.current_level = 0
            world.updateLevel()
            menu()
        # draw_lines()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    weapons.change_weapon(character, event.button)
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                weapons.choose_weapon(keys_pressed, character)
                if event.key == pygame.K_ESCAPE:
                    
                    doorAnimation.activeOpen = True
                    
                    
        
        keys_pressed = pygame.key.get_pressed()
        character.move(keys_pressed, world)
        weapons.displayAndUpdate(screen, world)
        weapons.toShoot(character, screen)
        world.animationController()
        cursorChange()
        doorAnimation.doorClose(screen)


        middle = doorAnimation.doorOpen(screen)
        if middle:
            level = world.current_level
            world.current_level = -1
            world.updateLevel()
            menu(menu_type="resume",current_level= level)

            
        pygame.display.update()
        clock.tick(FPS)


def menu(menu_type = "menu", current_level = 0):
    animationType = 'start'
    multiplier = 0
    to_level = current_level
    bg_surface = pygame.image.load(os.path.join(
        'images', 'background_blue.png')).convert()
    bg_surface = pygame.transform.scale(bg_surface, (1200, 800))
    title = pygame.image.load(os.path.join(
        'images', 'title.png')).convert_alpha()
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
    new_game = pygame.image.load(os.path.join('images', 'new_game.png'))
    all_levels = pygame.image.load(os.path.join('images', 'all_levels.png'))
    exit_game = pygame.image.load(os.path.join('images', 'exit.png'))
    main_menu = pygame.image.load(os.path.join('images', 'main_menu.png'))
    resume = pygame.image.load(os.path.join('images', 'resume.png'))
    message_surface = MENU_FONT.render('Navigate the menu by shooting the option you choose.',True,(255,255,255))
    message_rect = message_surface.get_rect(center = (600,775))
    character1 = Character(bottomleftpos=(world.charpos))
    weapons1 = Weapons()

    # Menu loop
    while True:
        screen.blit(bg_surface, (0, 0))
        screen.blit(title, title_rect)
        character1.display(screen, pygame.mouse.get_pos())
        world.update(screen, character1, weapons1)
        screen.blit(message_surface,message_rect)
        if menu_type == "menu":
            screen.blit(new_game, (SCREEN_WIDTH//2-100, 400))
            screen.blit(all_levels, (SCREEN_WIDTH//2-100, 500))
            screen.blit(exit_game, (SCREEN_WIDTH//2-100, 600))
        elif menu_type == "levels":
            world.writeNumbers(screen, multiplier)
        elif menu_type == "resume":
            screen.blit(resume, (SCREEN_WIDTH//2-100, 400))
            screen.blit(main_menu, (SCREEN_WIDTH//2-100, 500))
        weapons1.display_projectiles(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    weapons1.change_weapon(character1, event.button)
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                weapons1.choose_weapon(keys_pressed, character1)
                

        keys_pressed = pygame.key.get_pressed()
        character1.move(keys_pressed, world)
        weapons1.displayAndUpdate(screen, world)
        weapons1.toShoot(character1, screen)
        world.animationController()

        if menu_type == "menu":
            if world.checkButtons('start', weapons1) and not doorAnimation.activeOpen and not doorAnimation.activeClose:
                animationType = 'start'
                doorAnimation.activeOpen = True
            middle = doorAnimation.doorOpen(screen)
            if middle and animationType == 'start':
                weapons1.cleenProjectiles()
                world.current_level = 1
                main()

            if world.checkButtons('levels', weapons1) and not doorAnimation.activeOpen and not doorAnimation.activeClose:
                doorAnimation.activeOpen = True
                animationType = 'levels'
            middle = doorAnimation.doorOpen(screen)
            if middle and animationType == 'levels':
                menu_type = "levels"
                weapons1.cleenProjectiles()
                world.current_level = 1000
                world.updateLevel()
            
            if world.checkButtons('exit', weapons1):
                pygame.quit()
                sys.exit()
                break

        if menu_type == "levels":
            if not doorAnimation.activeOpen and not doorAnimation.activeClose:
                returndata = world.checkButtonsLevels(multiplier, weapons1)
                if returndata == "next":
                    if multiplier <= 69:
                        animationType = 'next_page'
                        doorAnimation.activeOpen = True
                    else:
                        weapons1.cleenProjectiles()
                elif returndata == "back":
                    if multiplier > 0:
                        animationType = 'prev_page'
                        doorAnimation.activeOpen = True
                    else:
                        animationType = 'menu'
                        doorAnimation.activeOpen = True
                elif returndata != 0:
                    if world.checkExistLevel(returndata):
                        animationType = 'level_start'
                        doorAnimation.activeOpen = True
                        to_level = returndata
                    else:
                        weapons1.cleenProjectiles()
            middle = doorAnimation.doorOpen(screen)
            if middle and animationType == 'next_page':
                weapons1.cleenProjectiles()
                multiplier += 1
            if middle and animationType == 'prev_page':
                weapons1.cleenProjectiles()
                multiplier -= 1
            if middle and animationType == 'level_start':
                world.current_level = to_level
                main()
            if middle and animationType == 'menu':
                world.current_level = 0
                world.updateLevel()
                weapons1.cleenProjectiles()
                menu_type = 'menu'

        if menu_type == "resume":
            world.current_level = -1
            if world.checkButtons('resume', weapons1) and not doorAnimation.activeOpen and not doorAnimation.activeClose:
                animationType = 'resume'
                doorAnimation.activeOpen = True
            if world.checkButtons('main_menu', weapons1) and not doorAnimation.activeOpen and not doorAnimation.activeClose:
                animationType = 'menu'
                doorAnimation.activeOpen = True
            middle = doorAnimation.doorOpen(screen)
            if middle and animationType == 'resume':
                world.current_level = to_level
                world.updateLevel()
                weapons1.cleenProjectiles()
                main()

            if middle and animationType == 'menu':
                world.current_level = 0
                world.updateLevel()
                weapons1.cleenProjectiles()
                menu_type = 'menu'

        cursorChange()
        doorAnimation.doorClose(screen)
      
        pygame.display.update()
        clock.tick(FPS)


menu()
