import pygame, time ,sys , random

pygame.init()
clock = pygame.time.Clock()

file = open('High_Score.txt', 'r')
High_Score = file.read()
High_Score = float(High_Score)
file.close()


# Game Loop
def Game(Background_Path, Target_Path, Crosshair_path, curtain_path, num_bullets,screen_width,screen_height):
    # Timer
    current_time = 0
    static_time = 0
    time = 0
    # Score Settings
    font = pygame.font.Font('freesansbold.ttf', 50)
    Score = 0
    Bonus = 1
    Bullets = int(num_bullets + 2)
    Bullet_x = 1050
    Bullet_y = 150
    BulletImg = pygame.image.load('PNG/HUD/icon_bullet_gold_long.png')

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

        def shoot(self, Score, Bonus, Bullets):
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
                Bullets += - 1
            return [Score, Bonus, Bullets]

        def update(self):
            self.rect.center = pygame.mouse.get_pos()

    class Target(pygame.sprite.Sprite):
        def __init__(self, target_path):
            super().__init__()
            self.image = pygame.image.load(target_path)
            self.rect = self.image.get_rect()
            self.rect.center = [random.randint(0, screen_width - 100), random.randint(200, screen_height - 100)]

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
                Score, Bonus, Bullets = crosshair.shoot(Score, Bonus, Bullets)

        target_group.draw(screen)
        crosshair_group.draw(screen)
        crosshair_group.update()
        time_text = font.render(f":{(3000 - time) / 100} ", True, (255, 255, 255))
        score_text = font.render(f"{Score}", True, (0, 0, 0))
        bonus_text = font.render(f"{Bonus}", True, (0, 0, 0))

        for num in range(Bullets):
            screen.blit(BulletImg, (Bullet_x + (num * 25), Bullet_y))
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

        if Bullets == 0:
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