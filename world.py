import pygame
from data import BLOCKS, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, DOOR, LEVEL, LEVELS, LEVELS_MENU, NUMBERS, LOCKED, NAVIGATION, MESSAGES, GAME_FONT
from csv_handler import csvMatrixReader
from animation import DoorTransition
import os
pygame.init()
pygame.mixer.init()


class World():

    def __init__(self, screen):
        self.doorAnimation = DoorTransition()
        self.charpos = (0, 0)
        self.current_level = 0
        self.tile_rect = []
        self.level = self.getLevel()
        self.level_animations = self.getLevelAnimations()
        self.draw(screen)
        self.animation_delay = 10
        self.isNextLevel_animation = False
        self.nextLevel_animation = 0
        self.animationHitMiddle = False

    def updateLevel(self):
        self.level = self.getLevel()
        self.level_animations = self.getLevelAnimations()

    def getLevel(self):
        self.tile_rect = []
        mat = csvMatrixReader(self.current_level)
        y = 0
        for i in range(len(mat)):
            x = 0
            for j in range(len(mat[i])):
                if mat[i][j] == 100:
                    mat[i][j] = 0
                    self.charpos = (j*50, i*50 + 50)
                elif mat[i][j] != 0:
                    self.tile_rect.append(pygame.Rect(x*50, y*50, 50, 50))
                x += 1
            y += 1
        return mat

    def getLevelAnimations(self):
        animation_mat = []
        for i in range(len(self.level)):
            animation_mat.append([])
            for j in range(len(self.level[i])):
                # delay, stage, active
                animation_mat[i].append([5, 0, False])
        return animation_mat

    def draw(self, screen):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] in BLOCKS.keys():
                    if self.level[i][j] == 100:
                        block = BLOCKS[self.level[i][j]] 
                    elif self.level[i][j] > 2 and self.level[i][j] != 10 and self.level[i][j] != 7:
                        block = BLOCKS[self.level[i][j]
                                       ][self.level_animations[i][j][1]]
                    else:
                        block = BLOCKS[self.level[i][j]]
                    rect = block.get_rect(x=j*50, y=i*50)
                    if self.level[i][j] == 8:
                        rect.y -=50
                    screen.blit(block, rect)
        self.drawMessage(screen)

    def drawMessage(self, screen):
        try :
            sentence = MESSAGES[self.current_level].split('\n')
            y = 350
            if len(sentence) > 1:
                y = 150
            for line in sentence:
                message_surface = GAME_FONT.render(line, True, (255,255,255))
                message_rect = message_surface.get_rect(center = (600, y))
                screen.blit(message_surface, message_rect)
                y+=50
        except KeyError:
            pass

    def door_animate(self, character, screen, weapons):
        if self.doorAnimation.activeOpen:
            middle = self.doorAnimation.doorOpen(screen)
            if middle:
                self.current_level += 1
                try:
                    self.level = self.getLevel()
                except FileNotFoundError:
                    return False
                self.level_animations = self.getLevelAnimations()
                character.rect[0].bottomleft = self.charpos
                weapons.cleenProjectiles()
        if self.doorAnimation.activeClose:
            self.doorAnimation.doorClose(screen)
        return True

    def update(self, screen, character, weapons):
        self.draw(screen)
        weapons.display_projectiles(screen)
        weapons.displayWeapons(screen)
        if weapons.cur_weapon.toCharge:
            weapons.cur_weapon.displayPowerBar(screen, character)
        more_levels = self.door_animate(character, screen, weapons)
        return more_levels

    def add(self, screen, block):
        keys = pygame.mouse.get_pressed(num_buttons=3)
        if keys[0] or keys[1] or keys[2]:
            pos = pygame.mouse.get_pos()
            x = pos[0]//50
            y = pos[1]//50
            if pos[0] < 1200:
                if keys[0]:
                    self.level[y][x] = block
                if keys[2]:
                    self.level[y][x] = 0


    def getTile(self, x, y):
        y = int(y//50)
        x = int(x//50)
        if y < 0 or x < 0:
            return 0
        try:
            return self.level[y][x]
        except IndexError:
            return 0

    def activeBlock(self, x, y):
        if self.getTile(x, y) == 10:
            self.nextLevel()
        elif self.getTile(x, y) == 8:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound('audio/launcher.wav'))
        try:
            if x > 0 and y > 0:
                self.level_animations[y//50][x//50][2] = True
        except IndexError:
            pass

    def animationController(self):
        for row in self.level_animations:
            for block in row:
                if block[2] == True:  # is active?
                    if block[0] > 0:
                        block[0] -= 1
                    else:
                        block[0] = 5
                        if block[1] < 6:
                            block[1] += 1
                        else:
                            block[2] = False
                            block[1] = 0

    def nextLevel(self):
        self.doorAnimation.activeOpen = True

    def drawLevel(self, screen):
        level_rect = LEVEL.get_rect(center=(SCREEN_WIDTH//2, 23))
        screen.blit(LEVEL, level_rect)
        if self.current_level != 200 and self.current_level != 0:
            screen.blit(LEVELS[self.current_level//100],
                        (level_rect.left + 140,  level_rect.y + 4))
            screen.blit(LEVELS[self.current_level//10 % 10],
                        (level_rect.left + 165,  level_rect.y + 4))
            screen.blit(LEVELS[self.current_level % 10],
                        (level_rect.left + 190,  level_rect.y + 4))

    def checkButtons(self, kind, weapons):
        for weapon in weapons.weapons:
            for projectile in weapon.hit_projectiles:
                x = projectile.rect.centerx//50
                y = projectile.rect.centery//50
                if x >= 10 and x < 14:
                    if y == 8 and (kind == 'start' or kind =='resume'):
                        return True
                    if y == 10 and (kind == 'levels' or kind == 'main_menu'):
                        return True
                    if y == 12 and kind == 'exit':
                        return True
        return False
        
    def checkButtonsLevels(self, multiplier, weapons):
        for weapon in weapons.weapons:
            for projectile in weapon.hit_projectiles:
                x = projectile.rect.centerx//50
                y = projectile.rect.centery//50
                for key in LEVELS_MENU.keys():
                    if LEVELS_MENU[key] == (x, y):
                        if key == 'next' or key == 'back':
                            return key
                        return key + multiplier*14
        return 0

    def writeNumbers(self, screen, multiplier):

        for key in LEVELS_MENU.keys():
            nums_surface = pygame.surface.Surface(
                (50, 50)).convert_alpha()
            if key != 'next' and key != 'back':
                new_key = key + multiplier*14
                if new_key < 10:
                    num_rect = NUMBERS[new_key].get_rect(center=(25, 25))
                    nums_surface.blit(pygame.transform.scale2x(pygame.image.load(
                        os.path.join('images', 'blocks', 'blue_dirt.png'))), (0, 0))
                    nums_surface.blit(NUMBERS[new_key], num_rect)
                    screen.blit(
                        nums_surface, (LEVELS_MENU[key][0]*50, LEVELS_MENU[key][1]*50))
                elif new_key > 9 and new_key < 100:
                    num_rect1 = NUMBERS[new_key//10].get_rect(center=(16, 25))
                    num_rect2 = NUMBERS[new_key % 10].get_rect(center=(34, 25))
                    nums_surface.blit(pygame.transform.scale2x(pygame.image.load(
                        os.path.join('images', 'blocks', 'blue_dirt.png'))), (0, 0))
                    nums_surface.blit(NUMBERS[new_key//10], num_rect1)
                    nums_surface.blit(NUMBERS[new_key % 10], num_rect2)
                    if not self.checkExistLevel(new_key):
                        nums_surface.blit(LOCKED, (0, 0))
                    screen.blit(
                        nums_surface, (LEVELS_MENU[key][0]*50, LEVELS_MENU[key][1]*50))
                elif new_key > 99:
                    num_rect1 = NUMBERS[new_key//100].get_rect(center=(11, 25))
                    num_rect2 = NUMBERS[new_key // 10 %
                                        10].get_rect(center=(25, 25))
                    num_rect3 = NUMBERS[new_key % 10].get_rect(center=(39, 25))
                    nums_surface.blit(pygame.transform.scale2x(pygame.image.load(
                        os.path.join('images', 'blocks', 'blue_dirt.png'))), (0, 0))
                    nums_surface.blit(NUMBERS[new_key//100], num_rect1)
                    nums_surface.blit(NUMBERS[new_key // 10 % 10], num_rect2)
                    nums_surface.blit(NUMBERS[new_key % 10], num_rect3)
                    if not self.checkExistLevel(new_key):
                        nums_surface.blit(LOCKED, (0, 0))
                    screen.blit(
                        nums_surface, (LEVELS_MENU[key][0]*50, LEVELS_MENU[key][1]*50))
            else:
                if key == 'next':
                    screen.blit(
                        NAVIGATION[0], (LEVELS_MENU[key][0]*50, LEVELS_MENU[key][1]*50))
                if key == 'back':
                    screen.blit(
                        NAVIGATION[1], (LEVELS_MENU[key][0]*50, LEVELS_MENU[key][1]*50))

    def checkExistLevel(self, level):
        try:
            with open(os.path.join('levels', f'level_{level}.csv')) as file:
                return True
        except FileNotFoundError:
            return False

    def updateTileRect(self):
        self.tile_rect = []
        mat = self.level
        y = 0
        for i in range(len(mat)):
            x = 0
            for j in range(len(mat[i])):
                if mat[i][j] == 100:
                    mat[i][j] = 0
                    self.charpos = (j*50, i*50 + 50)
                elif mat[i][j] != 0:
                    self.tile_rect.append(pygame.Rect(x*50, y*50, 50, 50))
                x += 1
            y += 1
        