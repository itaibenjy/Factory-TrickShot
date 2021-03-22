import pygame
import os
from data import DOOR, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
pygame.mixer.init()
door_hit = pygame.mixer.Sound('audio/door_hit.wav')
door_slid = pygame.mixer.Sound('audio/door_slide.wav')

class DoorTransition():

    def __init__(self):
        self.activeOpen = False
        self.activeClose = False
        self.nextLevel_animation = 0
        self.animationHitMiddle = False
        self.returnHit = False

    def doorOpen(self, screen):
        if self.activeOpen:
            if not pygame.mixer.Channel(5).get_busy():
                pygame.mixer.Channel(5).play(door_slid)
            rigth_x = self.nextLevel_animation - SCREEN_WIDTH//2
            left_x = SCREEN_WIDTH - self.nextLevel_animation
            screen.blit(DOOR, (rigth_x, 0))
            screen.blit(pygame.transform.flip(DOOR, True, False), (left_x, 0))
            if self.nextLevel_animation == 320:
                pygame.mixer.Channel(6).play(door_hit)
            if self.nextLevel_animation >= 600:
                pygame.mixer.Channel(5).play(door_slid)
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
                pygame.mixer.Channel(5).fadeout(140)
                return True
            self.nextLevel_animation -= 5
        return False
