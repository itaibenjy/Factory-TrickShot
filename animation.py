import pygame
import os
from data import DOOR, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()


class DoorTransition():

    def __init__(self):
        self.activeOpen = False
        self.activeClose = False
        self.nextLevel_animation = 0
        self.animationHitMiddle = False
        self.returnHit = False

    def doorOpen(self, screen):
        if self.activeOpen:
            rigth_x = self.nextLevel_animation - SCREEN_WIDTH//2
            left_x = SCREEN_WIDTH - self.nextLevel_animation
            screen.blit(DOOR, (rigth_x, 0))
            screen.blit(pygame.transform.flip(DOOR, True, False), (left_x, 0))
            if self.nextLevel_animation >= 600:
                self.activeOpen = False
                self.activeClose = True
                return True

            self.nextLevel_animation += 5
        return False

    def doorClose(self, screen):
        if self.activeClose:
            right_x = self.nextLevel_animation - SCREEN_WIDTH//2
            left_x = SCREEN_WIDTH - self.nextLevel_animation
            screen.blit(DOOR, (right_x, 0))
            screen.blit(pygame.transform.flip(
                DOOR, True, False), (left_x, 0))
            if self.nextLevel_animation <= 0:
                self.activeClose = False
                self.nextLevel_animation = 0
                return True
            self.nextLevel_animation -= 5
        return False
