import pygame, sys, random

import GameLoop

pygame.init()
clock = pygame.time.Clock()

# Reading The Currency Store
file = open('Currency.txt', 'r')
currency = file.read()
currency = float(currency)
file.close()

XL_font = pygame.font.Font('freesansbold.ttf', 64)


def Instructions():
    screen = pygame.display.set_mode((1205, 780))
    page = pygame.image.load('PNG/Stall/Instructions.png')
    pygame.mouse.set_visible(True)
    Show = True
    while Show:
        screen.fill((0, 0, 0))
        screen.blit(page, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x >= 1030 and x <= 1180 and y >= 28 and y <= 85:
                    Show = False
        pygame.display.flip()
    return


# Main_Menu Screen
screen_width = 1205
screen_height = 780
menu_screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load('PNG/HUD/crosshair_blue_large.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Carnival Shooting                               byCienkang')
menu_bg = pygame.image.load('PNG/Stall/bg_wood.png')
Main_menu = True
Background_Path = 'PNG/Stall/bg_blue.png'
Target_Path = 'PNG/Objects/target_red3.png'
Curtain_Path = 'PNG/Stall/curtain_straight.png'
Crosshair_Path = 'PNG/HUD/crosshair_white_large.png'


class Menu_Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('PNG/HUD/Gunshot.mp3')

    def shoot(self):
        self.gunshot.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


crosshair = Menu_Crosshair(Crosshair_Path)
menu_crosshair_group = pygame.sprite.Group()
menu_crosshair_group.add(crosshair)
gunshot = pygame.mixer.Sound('PNG/HUD/Gunshot.mp3')
num_of_bullets = 4
while Main_menu:

    menu_screen.fill((0, 0, 0))
    menu_screen.blit(menu_bg, (0, 0))
    Menu_Text = XL_font.render(f"${currency}", True, (25, 25, 25))
    menu_screen.blit(Menu_Text, (550, 680))
    menu_crosshair_group.draw(menu_screen)
    menu_crosshair_group.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file = open('Currency.txt', 'w')
            file.write(str(currency))
            file.close()
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                Instructions()
            if event.key == pygame.K_s:
                pass
            if event.key == pygame.K_c:
                pass
            if event.key == pygame.K_p:
                currency += GameLoop.Game(Background_Path, Target_Path, Crosshair_Path, Curtain_Path, num_of_bullets,
                                          screen_width, screen_height)
        if event.type == pygame.MOUSEBUTTONDOWN:
            gunshot.play()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x >= 480 and mouse_x <= 780) and (mouse_y >= 290 and mouse_y <= 365):
                currency += GameLoop.Game(Background_Path, Target_Path, Crosshair_Path, Curtain_Path, num_of_bullets,
                                          screen_width, screen_height)
    pygame.display.flip()
    clock.tick(60)
