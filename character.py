import pygame
import os
import math
from data import SCREEN_WIDTH, WALKING_SPEED, GRAVITY, JUMP, BOW, BOOMERANG


class Character():

    def __init__(self, bottomleftpos, character='soldier'):
        self.character = character
        self.isFacingRight = True
        self.surface = [
            # Body - walking part
            pygame.transform.scale2x(pygame.image.load(os.path.join(
                'images', self.character, f"{self.character}_bottom.png"))).convert_alpha(),
            # Head and Hands - rotating part
            pygame.transform.scale2x(pygame.image.load(os.path.join(
                'images', self.character, f"{self.character}_upper_tommy.png"))).convert_alpha()
        ]
        self.head = self.surface[1]
        # Rotating Destroy quality (rotate once from default position)

        self.rect = self.getRects(bottomleftpos)
        self.pos = self.rect[0].center
        self.movement = [0, 0]
        self.canJump = True
        self.animation = 1
        self.animationSlower = 6

    def getRects(self, bottomleftpos):
        bottom = self.surface[0].get_rect(bottomleft=bottomleftpos)
        upper = self.surface[1].get_rect(
            center=(bottom.centerx, bottom.centery - 32))
        return [bottom, upper]

    def updateRects(self):
        bottom = self.rect[0]
        upper = self.surface[1].get_rect(
            center=(bottom.centerx, bottom.centery - 32))
        return [bottom, upper]

    def flip(self):
        self.surface[0] = pygame.transform.flip(self.surface[0], True, False)
        self.surface[1] = pygame.transform.flip(self.surface[0], True, False)
        self.head = pygame.transform.flip(self.head, True, False)

    def checkCollisions(self, direction, world):
        if direction == 'left':
            if world.getTile(self.rect[0].left - WALKING_SPEED, self.rect[0].bottom) == 0:
                if world.getTile(self.rect[0].left - WALKING_SPEED, self.rect[0].top-20) == 0:
                    return True
            else:
                return False
        if direction == 'right':
            if world.getTile(self.rect[0].right + WALKING_SPEED, self.rect[0].bottom) == 0:
                if world.getTile(self.rect[0].right + WALKING_SPEED, self.rect[0].top-20) == 0:
                    return True
            else:
                return False

    def collision_test(self, rect, world):
        hit_list = []
        for tile in world.tile_rect:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, keys, world):
        rect = pygame.Rect(self.rect[0].x, self.rect[0].y -
                           20, self.rect[0].width, self.rect[0].height+20)
        collision_types = {'top': False, 'bottom': False,
                           'left': False, 'right': False}
        if keys[pygame.K_a] and self.rect[0].x > 0:
            self.movement[0] = WALKING_SPEED * -1
        else:
            self.movement[0] = 0
        if keys[pygame.K_d] and self.rect[0].right < SCREEN_WIDTH:
            self.movement[0] = WALKING_SPEED
        elif self.movement[0] > 0:
            self.movement[0] = 0
        if keys[pygame.K_SPACE] and self.canJump and self.movement[1] < 3:
            self.movement[1] = JUMP
            self.canJump = False
        self.movement[1] += GRAVITY

        rect.x += self.movement[0]
        hit_list = self.collision_test(rect, world)
        for tile in hit_list:
            if self.movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif self.movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += self.movement[1]
        hit_list = self.collision_test(rect, world)
        for tile in hit_list:
            if self.movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True

        if collision_types['top'] or collision_types['bottom']:
            self.movement[1] = 0
        if collision_types['bottom']:
            y = self.rect[0].bottom +10
            x = self.rect[0].centerx
            if world.getTile(x,y) == 8:
                world.activeBlock(x,y)
                self.movement[1] = JUMP * 2
            else: 
                self.canJump = True

        self.rect[0].x = rect.x
        self.rect[0].y = rect.y + 20

        self.animationContoller(keys)

        # return rect, collision_types

    def display(self, screen, mouse_pos):
        self.rotateHead(mouse_pos)
        self.rect = self.updateRects()
        if not self.isFacingRight:
            screen.blit(self.surface[0], self.rect[0])
            screen.blit(self.surface[1], self.rect[1])
        else:
            screen.blit(pygame.transform.flip(
                self.surface[0], True, False), self.rect[0])
            screen.blit(pygame.transform.flip(
                self.surface[1], True, False), self.rect[1])

    def rotateHead(self, mouse_pos):
        x = mouse_pos[0] - self.rect[1].centerx
        y = mouse_pos[1] - self.rect[1].centery
        if x != 0:
            angle = math.degrees(math.atan(abs(y)/abs(x)))
        else:
            angle = 90
        if x >= 0 and y >= 0:
            angle = angle
        elif x >= 0 and y < 0:
            angle = -angle
        elif x < 0 and y < 0:
            angle = -angle

        if x < 0:
            if self.isFacingRight:
                self.isFacingRight = False
        else:
            if not self.isFacingRight:
                self.isFacingRight = True

        self.surface[1] = pygame.transform.rotozoom(
            self.head, angle, 1)

    def weapon_hold(self, kind):
        if kind == "bow":
            self.head = BOW[0]
        elif kind == "tommy":
            self.head = pygame.transform.scale2x(pygame.image.load(os.path.join(
                'images', self.character, f"{self.character}_upper_{kind}.png"))).convert_alpha()
        elif kind == "boomerang":
            self.head = BOOMERANG[0]

    def animationContoller(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if self.animationSlower <= 0:
                if self.animation == 7:
                    self.animation = 1
                else:
                    self.animation += 1
                self.animationSlower = 6
            else:
                self.animationSlower -= 1

            self.surface[0] = pygame.transform.scale2x(pygame.image.load(os.path.join(
                'images', self.character, f"{self.character}_orange{self.animation}.png"))).convert_alpha()

        else:
            self.surface[0] = pygame.transform.scale2x(pygame.image.load(os.path.join(
                'images', self.character, f"{self.character}_bottom.png"))).convert_alpha()
