import pygame
import os

pygame.init()
screen = pygame.display.set_mode((0, 0))


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 90
BULLET_VEL = 10
ARROW_VEL = 10
WALKING_SPEED = 3
GRAVITY = 0.25
JUMP = -8
GAME_FONT = pygame.font.Font(os.path.join('font','terminal-grotesque_open.otf'), 40)
MENU_FONT = pygame.font.Font(os.path.join('font', 'terminal-grotesque_open.otf'), 30)

CURSOR = pygame.image.load(os.path.join(
    'images', 'cursor.png')).convert_alpha()

POWER_BAR = []
for i in range(17):
    POWER_BAR.append(pygame.image.load(os.path.join(
        'images', 'power_bar', f'power_bar{i+1}.png')))


BOW = []
for i in range(4):
    BOW.append(pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bow', f'soldier_bow_blue{i+1}.png'))).convert_alpha())


BOOMERANG = []
for i in range(4):
    BOOMERANG.append(pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'boomerang', f'soldier_boomerang{i+1}.png'))).convert_alpha())

# all blocks and their animation images
BLOCKS = {
    1: pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'blue_dirt.png'))).convert_alpha(),
    2: pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'blue_grass2.png'))).convert_alpha(),
    3: [pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin1.png')).convert_alpha(),
        pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin2.png')).convert_alpha(),
        pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin3.png')).convert_alpha(),
        pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin4.png')).convert_alpha(),
        pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin5.png')).convert_alpha(),
        pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin6.png')).convert_alpha(),
        pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin7.png')).convert_alpha()],
    4: [pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin1.png')).convert_alpha(), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin2.png')).convert_alpha(), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin3.png')).convert_alpha(), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin4.png')).convert_alpha(), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin5.png')).convert_alpha(), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin6.png')).convert_alpha(), True, False),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin7.png')).convert_alpha(), True, False)],
    5: [pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin1.png')).convert_alpha(), False, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin2.png')).convert_alpha(), False, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin3.png')).convert_alpha(), False, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin4.png')).convert_alpha(), False, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin5.png')).convert_alpha(), False, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin6.png')).convert_alpha(), False, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin7.png')).convert_alpha(), False, True)],
    6: [pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin1.png')).convert_alpha(), True, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin2.png')).convert_alpha(), True, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin3.png')).convert_alpha(), True, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin4.png')).convert_alpha(), True, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin5.png')).convert_alpha(), True, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin6.png')).convert_alpha(), True, True),
        pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin7.png')).convert_alpha(), True, True)],
    7:  pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'clear.png'))).convert_alpha(),
    8: [pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher1.png'))).convert_alpha(),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher2.png'))).convert_alpha(),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher3.png'))).convert_alpha(),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher4.png'))).convert_alpha(),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher5.png'))).convert_alpha(),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher6.png'))).convert_alpha(),
        pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'launcher', 'launcher7.png'))).convert_alpha(), ],
    10: pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'blocks', 'target.png'))).convert_alpha(),
    11: [pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular1.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin_regular2.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin_regular3.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin_regular4.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin_regular5.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin_regular6.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular7.png')).convert_alpha()],
    12: [pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular1.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks','trampolin', 'trampolin_regular2.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular3.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular4.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular5.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular6.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular7.png')).convert_alpha(), 270, 1)],
    13: [pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular1.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular2.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular3.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular4.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular5.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular6.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular7.png')).convert_alpha(), False, True)],
    14: [pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular1.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular2.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular3.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular4.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular5.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular6.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_regular7.png')).convert_alpha(), 90, 1), ],
    15: [pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power1.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power2.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power3.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power4.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power5.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power6.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power7.png')).convert_alpha()],
    16: [pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power1.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power2.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power3.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power4.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power5.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power6.png')).convert_alpha(), 270, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power7.png')).convert_alpha(), 270, 1)],
    17: [pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power1.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power2.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power3.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power4.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power5.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power6.png')).convert_alpha(), False, True),
         pygame.transform.flip(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power7.png')).convert_alpha(), False, True)],
    18: [pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power1.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power2.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power3.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power4.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power5.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power6.png')).convert_alpha(), 90, 1),
         pygame.transform.rotozoom(pygame.image.load(os.path.join('images', 'blocks', 'trampolin', 'trampolin_power7.png')).convert_alpha(), 90, 1), ],
    19: [pygame.image.load(os.path.join('images', 'blocks', 'portal', 'orange_portal1.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'orange_portal2.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'orange_portal3.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'orange_portal4.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'orange_portal5.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'orange_portal6.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'portal', 'orange_portal7.png')).convert_alpha()],
    20: [pygame.image.load(os.path.join('images', 'blocks', 'portal', 'purple_portal1.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'purple_portal2.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'purple_portal3.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'purple_portal4.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'purple_portal5.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks','portal', 'purple_portal6.png')).convert_alpha(),
         pygame.image.load(os.path.join('images', 'blocks', 'portal', 'purple_portal7.png')).convert_alpha()],
    100: pygame.image.load(os.path.join('images', 'spawn.png')).convert_alpha(),


}

# Door animation
DOOR = pygame.transform.scale2x(pygame.image.load(
    os.path.join('images', 'door.png'))).convert_alpha()

# for level editig specify the block to switch to
BLOCKS_POS = {
    1: (1200, 0),
    2: (1250, 0),
    3: (1200, 50),
    4: (1250, 50),
    5: (1200, 100),
    6: (1250, 100),
    7: (1200, 150),
    8: (1250, 150),
    9: (1200, 200),
    10: (1250, 200),
    11: (1200, 250),
    12: (1250, 250),
    13: (1200, 300),
    14: (1250, 300),
    15: (1200, 350),
    16: (1250, 350),
    17: (1200, 400),
    18: (1250,400),
    19: (1200, 450),
    20: (1250, 450)
}


# level top indicater
LEVEL = pygame.image.load(
    os.path.join('images', 'level', 'level.png')).convert_alpha()

# level menu numbers
LEVELS = [pygame.image.load(os.path.join('images', 'level', 'level_num0.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num1.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num2.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num3.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num4.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num5.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num6.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num7.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level',
                                         'level_num8.png')).convert_alpha(),
          pygame.image.load(os.path.join('images', 'level', 'level_num9.png')).convert_alpha(), ]

# 0-14 and next and back positions in level menu
LEVELS_MENU = {
    1: (6, 8),
    2: (8, 8),
    3: (10, 8),
    4: (12, 8),
    5: (14, 8),
    6: (16, 8),
    7: (18, 8),
    8: (6, 10),
    9: (8, 10),
    10: (10, 10),
    11: (12, 10),
    12: (14, 10),
    13: (16, 10),
    14: (18, 10),
    "next": (20, 13),
    "back": (3, 13),
}

LOCKED = pygame.image.load(os.path.join(
    'images', 'blocks', 'locked.png')).convert_alpha()

# next and back buttons
NAVIGATION = [pygame.image.load(os.path.join('images', 'blocks', 'next.png')).convert_alpha(),
              pygame.image.load(os.path.join(
                  'images', 'blocks', 'back.png')).convert_alpha()
              ]


# Weapon display left corner
WEAPONS = {
    'bow': [pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'weapons', 'bow.png'))).convert_alpha(),
            pygame.transform.scale2x(pygame.image.load(os.path.join(
                'images', 'weapons', 'bow_outlines.png'))).convert_alpha()
            ],
    'tommy': [pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'weapons', 'tommy.png'))).convert_alpha(),
              pygame.transform.scale2x(pygame.image.load(os.path.join(
                  'images', 'weapons', 'tommy_outlines.png'))).convert_alpha()
              ],
    'boomerang': [pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'weapons', 'boomerang_weapon.png'))).convert_alpha(),
              pygame.transform.scale2x(pygame.image.load(os.path.join(
                  'images', 'weapons', 'boomerang_weapon_outline.png'))).convert_alpha()
              ],
}

# number to level indicator at the top of level (red)
NUMBERS = [pygame.image.load(os.path.join('images', 'numbers', 'num_0.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_1.png')),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_2.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_3.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_4.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_5.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_6.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_7.png')).convert_alpha(),
           pygame.image.load(os.path.join(
               'images', 'numbers', 'num_8.png')).convert_alpha(),
           pygame.image.load(os.path.join('images', 'numbers', 'num_9.png')).convert_alpha(), ]



# messages help
MESSAGES = {}
with open(os.path.join('texts', 'messages.txt')) as file:
    data = file.readlines()

for line in data:
    index = line.find(".")
    num = int(line[:index])
    line = line[index+1:]
    line = line.replace('@', '\n')
    MESSAGES[num] = line
