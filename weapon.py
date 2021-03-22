import pygame
import random
import math
import os
from data import BULLET_VEL, ARROW_VEL, SCREEN_WIDTH, SCREEN_HEIGHT, POWER_BAR, BOW, WEAPONS, BOOMERANG

pygame.init()
screen = pygame.display.set_mode((0, 0))
pygame.mixer.init()
projectile_vel = {
    'bullet': BULLET_VEL,
    'arrow': ARROW_VEL,
    'boomerang': ARROW_VEL,
}

projectile_img = {
    'bullet': pygame.transform.scale(pygame.image.load(os.path.join('images', 'bullet.png')), (4, 10)).convert_alpha(),
    'arrow': pygame.transform.scale(pygame.image.load(os.path.join('images', 'arrow.png')), (8, 25)).convert_alpha(),
    'boomerang': pygame.image.load(os.path.join('images', 'boomerang.png')).convert_alpha(),
}

projectile_gravity = {
    'bullet': 0,
    'arrow': 0.1,
    'boomerang': 0.1,
}

projectile_cooldown = {
    'bullet': 4,
    'arrow': 0,
    'boomerang': 0,
}


class Weapons():
    def __init__(self):
        self.weapons = [Weapon('bullet'), Weapon('arrow', ammo=1), Weapon('boomerang', ammo=1)]
        self.cur_weapon = self.weapons[0]

    def displayAndUpdate(self, screen, world):
        self.move_projectiles()
        self.delete_projectiles()
        self.hit_projectiles(world)
        # self.displayWeapons(screen)

    def move_projectiles(self):
        for weapon in self.weapons:
            for projectile in weapon.projectiles:
                projectile.nextPos()
                projectile.rect.x = projectile.real_x
                projectile.rect.y = projectile.real_y

    def display_projectiles(self, screen):
        for weapon in self.weapons:
            for projectile in weapon.projectiles:
                projectile.display(screen)
            for projectile in weapon.hit_projectiles:
                projectile.display(screen)

    def delete_projectiles(self):
        for weapon in self.weapons:
            for projectile in weapon.projectiles:
                if (projectile.rect.x < -20 or projectile.rect.y < -20 or projectile.rect.x > SCREEN_WIDTH +20) and projectile.kind == 'bullet':
                    weapon.projectiles.remove(projectile)
                    print("bullet delete")
                elif (projectile.rect.x < -20 or projectile.rect.x > SCREEN_WIDTH + 20) and projectile.kind == 'arrow': 
                    weapon.projectiles.remove(projectile)
                    print("arrow delete")
                elif projectile.rect.y > SCREEN_HEIGHT + 20:
                    print("boomerang delete")
                    weapon.projectiles.remove(projectile)

    def hit_projectiles(self, world):
        for weapon in self.weapons:
            for projectile in weapon.projectiles:
                block = world.getTile(
                    projectile.rect.centerx, projectile.rect.centery)
                world.activeBlock(projectile.rect.centerx,
                                  projectile.rect.centery)
                if block == 3:
                    if projectile.canHit:
                        pygame.mixer.Channel(4).play(pygame.mixer.Sound('audio/bounce.wav'))
                        projectile.canHit = False
                        projectile.direction = self.calcTrampoline3(
                            projectile.direction)
                elif block == 4:
                    if projectile.canHit:
                        pygame.mixer.Channel(4).play(pygame.mixer.Sound('audio/bounce.wav'))
                        projectile.canHit = False
                        projectile.direction = self.calcTrampoline4(
                            projectile.direction)
                elif block == 5:
                    if projectile.canHit:
                        pygame.mixer.Channel(4).play(pygame.mixer.Sound('audio/bounce.wav'))
                        projectile.canHit = False
                        projectile.direction = self.calcTrampoline5(
                            projectile.direction)
                elif block == 6:
                    if projectile.canHit:
                        pygame.mixer.Channel(4).play(pygame.mixer.Sound('audio/bounce.wav'))
                        projectile.canHit = False
                        projectile.direction = self.calcTrampoline6(
                            projectile.direction)
                elif block >= 11 and block <= 18:
                    if projectile.canHit:
                        pygame.mixer.Channel(4).play(pygame.mixer.Sound('audio/bounce.wav'))
                        projectile.canHit = False
                        projectile.direction = self.calcTrampolineRegular(
                            projectile.direction, block)
                elif block == 19 or block == 20:
                    if projectile.canHit:
                        pygame.mixer.Channel(8).play(pygame.mixer.Sound('audio/portal.wav'))
                        projectile.canHit = False
                        self.setPortalPosition(projectile, block, world)
                elif block == 7:
                    if projectile.kind == 'bullet':
                        pygame.mixer.Channel(3).play(pygame.mixer.Sound('audio/hit.wav'))
                        weapon.hit_projectiles.append(projectile)
                        if len(weapon.hit_projectiles) >= 20:
                            weapon.hit_projectiles.pop(0)
                        weapon.projectiles.remove(projectile)
                elif block != 0:
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('audio/hit.wav'))
                    weapon.hit_projectiles.append(projectile)
                    if len(weapon.hit_projectiles) >= 20:
                        weapon.hit_projectiles.pop(0)
                    if projectile.kind == 'boomerang' and len(weapon.hit_projectiles) >= 6:
                        weapon.hit_projectiles.pop(0)
                    weapon.projectiles.remove(projectile)
                else:
                    projectile.canHit = True

    def cleenProjectiles(self):
        for weapon in self.weapons:
            weapon.hit_projectiles = []

    def choose_weapon(self, keys, character):
        if keys[pygame.K_1]:
            self.cur_weapon = self.weapons[0]
            character.weapon_hold("tommy")
        if keys[pygame.K_2]:
            self.cur_weapon = self.weapons[1]
            character.weapon_hold("bow")
        if keys[pygame.K_3]:
            self.cur_weapon = self.weapons[2]
            character.weapon_hold("boomerang")

    def change_weapon(self, character, button):
        if button == 4:
            if self.cur_weapon.kind != 'bullet':
                if self.cur_weapon.kind != 'arrow':
                    self.cur_weapon = self.weapons[1]
                else:
                    self.cur_weapon = self.weapons[0]
            else: 
                self.cur_weapon = self.weapons[2]
        
        elif button == 5:
            if self.cur_weapon.kind != 'boomerang':
                if self.cur_weapon.kind != 'arrow':
                    self.cur_weapon = self.weapons[1]
                else:
                    self.cur_weapon = self.weapons[2]
            else:
                self.cur_weapon= self.weapons[0]
                

        if self.cur_weapon.kind == 'bullet':
            character.weapon_hold("tommy")
        elif self.cur_weapon.kind == 'arrow':
            character.weapon_hold("bow")
        elif self.cur_weapon.kind == 'boomerang':
            character.weapon_hold("boomerang")

    def toShoot(self, character, screen):
        self.cur_weapon.toShoot(character, screen)

    def shoot(self, character):
        self.cur_weapon.shoot(character)

    def displayWeapons(self, screen):
        if self.cur_weapon.kind == 'bullet':
            bow = WEAPONS['bow'][1]
            tommy = WEAPONS['tommy'][0]
            boomerang = WEAPONS['boomerang'][1]
        elif self.cur_weapon.kind == 'arrow':
            bow = WEAPONS['bow'][0]
            tommy = WEAPONS['tommy'][1]
            boomerang = WEAPONS['boomerang'][1]
        else:
            bow = WEAPONS['bow'][1]
            tommy = WEAPONS['tommy'][1]
            boomerang = WEAPONS['boomerang'][0]

        bow = pygame.transform.flip(bow, True, False)
        tommy = pygame.transform.flip(tommy, True, False)
        boomerang = pygame.transform.flip(boomerang, True, False)
        bow = pygame.transform.rotozoom(bow, 45, 1)
        tommy = pygame.transform.rotozoom(tommy, 45, 1)
        boomerang = pygame.transform.rotozoom(boomerang, 45,1)
        bow_rect = bow.get_rect(center=(75, SCREEN_HEIGHT-25))
        tommy_rect = tommy.get_rect(center=(25, SCREEN_HEIGHT-25))
        boomerang_rect = boomerang.get_rect(center=(125, SCREEN_HEIGHT-25))
        screen.blit(tommy, tommy_rect)
        screen.blit(bow, bow_rect)
        screen.blit(boomerang, boomerang_rect)

    def setPortalPosition(self, projectile, block, world):
        search_block = 19 if block == 20 else 20
        for i in range(len(world.level)):
            for j in range(len(world.level[i])):
                if world.level[i][j] == search_block:
                    projectile.real_x = j*50 +25
                    projectile.real_y = i*50 +25

    def calcTrampolineRegular(self, direction, block):
        x = direction[0]
        y = direction[1]
        if block == 11 or block == 13:
            new_x = x
            new_y = -y
        elif block == 12 or block == 14:
            new_x = -x
            new_y = y
        elif block == 15 or block == 17:
            new_x = 1.5*x
            new_y = -1.5 * y
        elif block == 16 or block == 18:
            new_x = -1.5 * x
            new_y = y * 1.5
        return (new_x, new_y)

    def calcTrampoline3(self, direction):
        x = direction[0]
        y = direction[1]
        try:
            angle = math.atan(abs(y)/abs(x))
        except ZeroDivisionError:
            angle = math.pi/2

        if y <= 0 and x <= 0:
            new_y = -max(abs(x), abs(y))
            new_x = new_y * math.tan(angle)
            return (new_x, new_y)

        elif y >= 0 and x >= 0:
            new_x = max(abs(x), abs(y))
            try:
                new_y = new_x / math.tan(angle)
            except ZeroDivisionError:
                new_y = new_x
            return (new_x, new_y)

        elif y > 0 and x < 0:
            new_angle = (math.pi/2) - angle
            if abs(x) < abs(y):
                new_x = max(abs(x), abs(y))
                try:
                    new_y = -new_x * math.tan(new_angle)
                except ZeroDivisionError:
                    new_y = -new_x
            else:
                new_y = -max(abs(x), abs(y))
                new_x = abs(new_y / math.tan(new_angle))
            return (new_x, new_y)

        return (-direction[0], direction[1])

    def calcTrampoline4(self, direction):
        x = direction[0]
        y = direction[1]
        try:
            angle = math.atan(abs(y)/abs(x))
        except ZeroDivisionError:
            angle = math.pi/2

        if y <= 0 and x >= 0:
            new_y = -max(abs(x), abs(y))
            new_x = -new_y * math.tan(angle)
            return (new_x, new_y)

        elif y >= 0 and x <= 0:
            new_x = -max(abs(x), abs(y))
            try:
                new_y = -new_x / math.tan(angle)
            except ZeroDivisionError:
                new_y = -new_x
            return (new_x, new_y)

        elif y >= 0 and x >= 0:
            new_angle = (math.pi/2) - angle
            if abs(x) < abs(y):
                new_x = -max(abs(x), abs(y))
                try:
                    new_y = new_x * math.tan(new_angle)
                except ZeroDivisionError:
                    new_y = new_x
            else:
                new_y = -max(abs(x), abs(y))
                new_x = new_y / math.tan(new_angle)
            return (new_x, new_y)

        return (-direction[0], direction[1])

    def calcTrampoline5(self, direction):
        x = direction[0]
        y = direction[1]
        try:
            angle = math.atan(abs(y)/abs(x))
        except ZeroDivisionError:
            angle = math.pi/2

        if y <= 0 and x >= 0:
            new_x = max(abs(x), abs(y))
            new_y = -new_x / math.tan(angle)
            return (new_x, new_y)

        elif y >= 0 and x <= 0:
            new_y = max(abs(x), abs(y))
            try:
                new_x = -new_y * math.tan(angle)
            except ZeroDivisionError:
                new_x = new_y
            return (new_x, new_y)

        elif y <= 0 and x <= 0:
            new_angle = (math.pi/2) - angle
            if abs(x) < abs(y):
                new_x = max(abs(x), abs(y))
                try:
                    new_y = new_x * math.tan(new_angle)
                except ZeroDivisionError:
                    new_y = new_x
            else:
                new_y = max(abs(x), abs(y))
                new_x = abs(new_y / math.tan(new_angle))

            return (new_x, new_y)

        return (-direction[0], direction[1])

    def calcTrampoline6(self, direction):
        x = direction[0]
        y = direction[1]
        try:
            angle = math.atan(abs(y)/abs(x))
        except ZeroDivisionError:
            angle = math.pi/2

        if y <= 0 and x <= 0:
            new_x = -max(abs(x), abs(y))
            new_y = new_x / math.tan(angle)
            return (new_x, new_y)

        elif y >= 0 and x >= 0:
            new_y = max(abs(x), abs(y))
            try:
                new_x = new_y * math.tan(angle)
            except ZeroDivisionError:
                new_x = new_y
            return (new_x, new_y)

        elif y <= 0 and x >= 0:
            new_angle = (math.pi/2) - angle
            if abs(x) < abs(y):
                new_x = -max(abs(x), abs(y))
                try:
                    new_y = -new_x * math.tan(new_angle)
                except ZeroDivisionError:
                    new_y = -new_x
            else:
                new_y = max(abs(x), abs(y))
                new_x = -new_y / math.tan(new_angle)
            return (new_x, new_y)

        return (-direction[0], direction[1])


class Weapon():

    def __init__(self, kind='bullet', ammo=30):
        self.projectiles = []
        self.hit_projectiles = []
        self.kind = kind
        self.vel = projectile_vel[kind]
        self.toCharge = False if kind == 'bullet' else True
        self.cooldown = projectile_cooldown[kind]
        self.cur_cooldown = self.cooldown
        self.chargeMeter = 0
        self.vel = projectile_vel[kind]

    def toShoot(self, character, screen):
        keys = pygame.mouse.get_pressed()
        if keys[0]:
            if self.toCharge:
                if self.chargeMeter < 50:
                    self.chargeMeter += 1
            else:
                self.shoot(character)
        else:
            if self.chargeMeter != 0 and self.toCharge:
                self.shoot(character)
            self.chargeMeter = 0

    def shoot(self, character):
        if self.cur_cooldown == 0:
            x = character.rect[1].centerx
            y = character.rect[1].centery + 5
            mouse_pos = pygame.mouse.get_pos()
            vel = self.vel if not self.toCharge else self.chargeMeter//3
            if self.kind == 'boomerang':
                self.projectiles.append(Boomerang(self.kind, mouse_pos, vel, char_pos=(x,y)))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio/swoosh.mp3'))
            else:
                self.projectiles.append(Projectile(self.kind, mouse_pos, vel, char_pos=(x, y)))
                if self.kind == 'bullet':
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('audio/gun_sound.mp3'))
                else:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio/swoosh.mp3'))
            self.cur_cooldown = self.cooldown
        else:
            self.cur_cooldown -= 1

    def displayPowerBar(self, screen, character):
        if self.kind == 'arrow':
            weapon_type = BOW
        elif self.kind == 'boomerang': 
            weapon_type = BOOMERANG
        character.head = weapon_type[self.chargeMeter//14]
        surface = POWER_BAR[self.chargeMeter//3]
        rect = surface.get_rect(top=10, left=10)
        screen.blit(surface, rect)


class Projectile():

    def __init__(self, kind, mouse_pos, vel, char_pos):
        self.canHit = True
        self.kind = kind
        self.origin_surface = projectile_img[kind]
        self.vel = vel
        self.direction = self.calc_direction(mouse_pos, char_pos)
        self.surface = self.getSurface()
        self.rect = self.surface.get_rect(
            center=char_pos)
        self.real_x = self.rect.x
        self.real_y = self.rect.y
        self.gravity = projectile_gravity[kind]
        self.hold_display = 3

    def calc_direction(self, mouse_pos, char_pos):
        mouse_x = mouse_pos[0] - char_pos[0]
        mouse_y = mouse_pos[1] - char_pos[1]
        if abs(mouse_x) > abs(mouse_y):
            dir_x = self.vel if mouse_x >= 0 else -self.vel
            try:
                dir_y = mouse_y / (abs(mouse_x/self.vel))
            except ZeroDivisionError:
                dir_y = 0
        else:
            dir_y = self.vel if mouse_y >= 0 else -self.vel
            try:
                dir_x = mouse_x / (abs(mouse_y/self.vel))
            except ZeroDivisionError:
                dir_x = 0

        return (dir_x, dir_y)

    def getSurface(self):
        x = self.direction[0]
        y = -self.direction[1]  # because pygame cord system
        if x != 0:
            angle = math.degrees(math.atan(abs(y)/abs(x)))
        else:
            angle = 90
        if x >= 0 and y >= 0:
            angle = -(90-angle)
        elif x < 0 and y >= 0:
            angle = 90 - angle
        elif x < 0 and y < 0:
            angle = 90 + angle
        elif x >= 0 and y < 0:
            angle = -90-angle
        new_projectile_surface = pygame.transform.rotozoom(
            projectile_img[self.kind], angle, 1)
        return new_projectile_surface

    def nextPos(self):
        self.direction = (self.direction[0], self.direction[1]+(self.gravity))
        self.real_x += self.direction[0]
        self.real_y += self.direction[1]

    def display(self, screen):
        if self.hold_display <= 0:
            self.surface = self.getSurface()
            screen.blit(self.surface, self.rect)
        else:
            self.hold_display -= 1


class Boomerang(Projectile):

    def __init__(self, kind, mouse_pos, vel, char_pos):
        super().__init__(kind, mouse_pos, vel, char_pos)
        self.x_momentum = projectile_gravity[kind] if self.direction[0] < 0 else -projectile_gravity[kind]
        self.gravity = -0.25*projectile_gravity[kind]
        self.gravity_multiplier = 8
        if self.direction[1] > 0:
            self.gravity = self.gravity * 4
            self.gravity_multiplier = 2
            
        if self.direction[0] == 0:
            self.x_momentum = 0
            self.gravity = projectile_gravity[kind]

        self.isGravitySwitch = False

    def nextPos(self):
        if (self.x_momentum > 0 and self.direction[0] > 0) or (self.x_momentum < 0 and self.direction[0] < 0):
            if not self.isGravitySwitch:
                self.gravity = -self.gravity*self.gravity_multiplier
                self.isGravitySwitch = True
        self.direction = (self.direction[0] + (self.x_momentum), self.direction[1]+(self.gravity))
        self.real_x += self.direction[0]
        self.real_y += self.direction[1]
