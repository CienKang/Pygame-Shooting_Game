import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()

# Reading The Currency Store
file = open('Currency.txt', 'r')
currency = file.read()
currency = float(currency)
file.close()

file = open('High_Score.txt', 'r')
High_Score = file.read()
High_Score = float(High_Score)
file.close()

XL_font = pygame.font.Font('freesansbold.ttf', 64)


# Game Loop
def Game(Background_Path, Target_Path, Crosshair_path, curtain_path):
    # Timer
    current_time = 0
    static_time = 0
    time = 0
    # Score Settings
    font = pygame.font.Font('freesansbold.ttf', 50)
    Score = 0
    Bonus = 1

    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.image.load(Background_Path)
    pygame.mouse.set_visible(False)
    score_curtain = pygame.image.load(curtain_path)

    class Crosshair(pygame.sprite.Sprite):
        def __init__(self, picture_path):
            super().__init__()
            self.image = pygame.image.load(picture_path)
            self.rect = self.image.get_rect()
            self.gunshot = pygame.mixer.Sound('PNG/HUD/Gunshot.mp3')

        def shoot(self, Score, Bonus):
            self.gunshot.play()
            create_new = False
            if pygame.sprite.spritecollide(crosshair, target_group, True):
                create_new = True
                Score += 1 * Bonus
                Bonus += 0.5
                if Bonus > 3:
                    Bonus = 3
            if create_new:
                new_target = Target('PNG/Objects/target_red3.png')
                target_group.add(new_target)
            else:
                Score += -1 * Bonus
                Bonus = 1
            return [Score, Bonus]

        def update(self):
            self.rect.center = pygame.mouse.get_pos()

    class Target(pygame.sprite.Sprite):
        def __init__(self, target_path):
            super().__init__()
            self.image = pygame.image.load(target_path)
            self.rect = self.image.get_rect()
            self.rect.center = [random.randint(287, screen_width - 100), random.randint(300, screen_height - 100)]

    # Crosshair Settings
    crosshair = Crosshair(Crosshair_path)
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)

    # Target Settings
    target_group = pygame.sprite.Group()
    num_primarytargets = 10
    for target in range(num_primarytargets):
        new_target = Target(Target_Path)
        target_group.add(new_target)

    while True:
        screen.blit(background, (0, 0))
        screen.blit(score_curtain, (0, 0,))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                Score, Bonus = crosshair.shoot(Score, Bonus)

        target_group.draw(screen)
        crosshair_group.draw(screen)
        crosshair_group.update()
        time_text = font.render(f":{(3000 - time) / 100} ", True, (255, 255, 255))
        score_text = font.render(f"{Score}", True, (0, 0, 0))
        bonus_text = font.render(f"{Bonus}", True, (0, 0, 0))
        current_time = pygame.time.get_ticks()
        if current_time - static_time > 1:
            time += 1
            static_time += 1

        if 1500 - time <= 0:
            if Score > High_Score:
                file = open('High_Score.txt', 'w')
                file.write(str(Score))
                file.close()
            break
        screen.blit(time_text, (240, 110))
        screen.blit(score_text, (580, 130))
        screen.blit(bonus_text, (1020, 110))

        pygame.display.flip()
        clock.tick(60)

    return Score / 100


# Ending game Loop


# Main_Menu Screen
screen_width = 1205
screen_height = 800
menu_screen = pygame.display.set_mode((screen_width, screen_height))
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
            if event.type == pygame.K_i:
                Instructions()
            if event.type == pygame.K_s:
                Settings()
            if event.type == pygame.K_c:
                Currency = Customize()
            if event.key == pygame.K_p:
                currency += Game(Background_Path, Target_Path, Crosshair_Path, Curtain_Path)
        if event.type == pygame.MOUSEBUTTONDOWN:
            gunshot.play()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x >= 480 and mouse_x <= 780) and (mouse_y >= 290 and mouse_y <= 365):
                currency += Game(Background_Path, Target_Path, Crosshair_Path, Curtain_Path)
    pygame.display.flip()
    clock.tick(60)
