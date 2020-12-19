import random
import pygame

pygame.init()
window = pygame.display.set_mode((1900, 1000))
pygame.display.set_caption("Space shooter")

game_run = True
game_started = False
bullets = []
enemies = []
boss = []


class Player:  # Класс игрока со всей необходимой информацией
    hp = 7
    max_hp = 7
    p_left = False
    p_right = False
    ship_color = "default"
    image = pygame.image.load("Img/Ship_2.png")
    img_l = pygame.image.load("Img/Ship_Left_2.png")
    img_r = pygame.image.load("Img/Ship_Right_2.png")
    image_y = pygame.image.load("Img/Ship_2_Y.png")
    img_l_y = pygame.image.load("Img/Ship_Left_2_Y.png")
    img_r_y = pygame.image.load("Img/Ship_Right_2_Y.png")
    image_bl = pygame.image.load("Img/Ship_2_BL.png")
    img_l_bl = pygame.image.load("Img/Ship_Left_2_BL.png")
    img_r_bl = pygame.image.load("Img/Ship_Right_2_BL.png")
    image_p = pygame.image.load("Img/Ship_2_P.png")
    img_l_p = pygame.image.load("Img/Ship_Left_2_P.png")
    img_r_p = pygame.image.load("Img/Ship_Right_2_P.png")
    img_hp1 = pygame.image.load("Img/HP1.png")
    img_hp0 = pygame.image.load("Img/HP0.png")
    img_hp_g = pygame.image.load("Img/HP_G.png")
    img_0_t = pygame.image.load("Img/0_T.png")
    img_1_t = pygame.image.load("Img/1_T.png")
    img_1_r = pygame.image.load("Img/1_R.png")
    img_r_g = pygame.image.load("Img/Rocket_Indicator_Green.png")
    img_r_r = pygame.image.load("Img/Rocket_Indicator_Red.png")
    img_shield = pygame.image.load("Img/Shield.png")
    img_shield_g = pygame.image.load("Img/Shield_Indicator_Green.png")
    img_shield_r = pygame.image.load("Img/Shield_Indicator_Red.png")
    img_shield_p = pygame.image.load("Img/Shield_Indicator_Purple.png")
    img_l_i_r = pygame.image.load("Img/Laser_Indicator_Red.png")
    img_l_i_g = pygame.image.load("Img/Laser_Indicator_Green.png")
    img_boom = pygame.image.load("Img/Boom_P.png")
    rect = image.get_rect()
    rect.x = 900
    rect.y = 600
    rocket_cd = 100
    gun_cd = 100
    gun_freeze = 0
    shield_hp = 0
    shield_cd = 100
    shield_active_time = -1
    laser_cd = 100
    die = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image = pygame.image.load("Img/Bullet_3.png")
        self.rect = self.image.get_rect()
        self.rect.x = Player.rect.x + 24
        self.rect.y = Player.rect.y - 9
        self.dmg = 1

    def move(self):
        self.rect.y -= 20


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Img/rocket_2.png")
        self.rect = self.image.get_rect()
        self.rect.x = Player.rect.x + 20
        self.rect.y = Player.rect.y - 27
        self.dmg = 10

    def move(self):
        self.rect.y -= 15


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Img/laser_f.png")
        self.rect = self.image.get_rect()
        self.rect.x = Player.rect.x + 22
        self.rect.y = Player.rect.y - 1024
        self.dmg = 2
        self.active_time = 15

    def move(self):
        if self.active_time > 0:
            self.active_time -= 1


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((36, 42))
        self.image = pygame.image.load("Img/Meteorite.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 1860)
        self.rect.y = -10
        self.hp = 3
        self.dmg = 1
        self.can_shoot = False

    def move(self):
        self.rect.y += 5


class Enemy_rocket_launcher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Img/rocket_enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 1850)
        self.rect.y = -10
        self.hp = 10
        self.dmg = 0
        self.can_shoot = True
        self.cd = 0

    def move(self):
        self.rect.y += 5

    def shoot(self):
        bullets.append(Enemy_rocket(self.rect.x + 10, self.rect.y + 60))


class Enemy_suicide(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Img/Boomer_off.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 1
        self.dmg = 3
        self.can_shoot = False

    def move(self):
        self.rect.y += 3
        if self.rect.y < Player.rect.y and Player.rect.y - self.rect.y < 200 and abs(Player.rect.x - self.rect.x) < 200:
            self.image = pygame.image.load("Img/Boomer_on.png")
            if self.rect.x > Player.rect.x:
                self.rect.x -= 6
                self.rect.y += 3
            else:
                self.rect.x += 6
                self.rect.y += 3
        else:
            self.image = pygame.image.load("Img/Boomer_off.png")


class Enemy_sniper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Img/sniper_enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 1850)
        self.rect.y = -10
        self.hp = 3
        self.dmg = 0
        self.can_shoot = True
        self.cd = 0

    def move(self):
        if self.rect.y < 80:
            self.rect.y += 3
        if random.randint(0, 1) and self.rect.y > 70:
            if self.rect.x < 1080:
                self.rect.x += 3
        else:
            if self.rect.x > 10:
                self.rect.x -= 3

    def shoot(self):
        bullets.append(Enemy_sniper_bullet(self.rect.x, self.rect.y + 60))


class Boss:
    hp = 560
    max_hp = 560
    image = pygame.image.load("Img/Boss_eye.png")
    image_ship = pygame.image.load("Img/Boss.png")
    rect = image.get_rect()
    rect.x = 704
    rect.y = 214
    spawn = False
    can_shoot = True
    cd = 0
    go_left = True
    move_speed = 5
    bomber_cd = 0
    body = True
    get_killed = False

    def move(self):
        if self.go_left and self.rect.x > 404:
            self.rect.x -= self.move_speed
        else:
            self.go_left = False
        if not self.go_left and self.rect.x < 1404:
            self.rect.x += self.move_speed
        else:
            self.go_left = True

    def shoot(self):
        if self.cd == 0:
            bullets.append(Enemy_sniper_bullet(self.rect.x - 4, self.rect.y + 76))
            bullets.append(Enemy_sniper_bullet(self.rect.x + 112, self.rect.y + 76))
            self.cd = 15
        else:
            self.cd -= 1


class Boss_gun:
    def __init__(self, x, y):
        self.hp = 100
        self.image = pygame.image.load("Img/Boss_Gun.png")
        self.rect = self.image.get_rect()
        self.rect.x = Boss.rect.x + x
        self.rect.y = Boss.rect.y + y
        self.can_shoot = True
        self.x = x
        self.y = y
        self.cd = 0
        self.body = False

    def move(self):
        self.rect.x = Boss.rect.x + self.x
        self.rect.y = Boss.rect.y + self.y

    def shoot(self):
        if self.hp > 0:
            if self.cd == 0:
                bullets.append(Enemy_rocket(self.rect.x, self.rect.y + 80))
                bullets.append(Enemy_rocket(self.rect.x + 20, self.rect.y + 80))
                self.cd = 40
            else:
                self.cd -= 1
        elif self.hp == 0:
            self.image = pygame.image.load("Img/Boss_gun_off.png")
            self.hp = -1


class Boss_engine:
    def __init__(self, x, y):
        self.hp = 200
        self.image = pygame.image.load("Img/Boss_engine.png")
        self.rect = self.image.get_rect()
        self.rect.x = Boss.rect.x + x
        self.rect.y = Boss.rect.y + y
        self.can_shoot = False
        self.x = x
        self.y = y
        self.body = False

    def move(self):
        if self.hp == 0:
            Boss.move_speed -= 2
            self.image = pygame.image.load("Img/Boss_engine_off.png")
            self.hp = -1
        self.rect.x = Boss.rect.x + self.x
        self.rect.y = Boss.rect.y + self.y


class Enemy_rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Img/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dmg = 1

    def move(self):
        self.rect.y += 10


class Enemy_sniper_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image = pygame.image.load("Img/Bullet_3.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dmg = 1
        self.target_x = Player.rect.x
        self.target_y = Player.rect.y

    def move(self):
        self.rect.y += 20


class Boost:
    image = pygame.image.load("Img/Boost.png")
    rect = image.get_rect()
    rect.x = random.randint(10, 1850)
    rect.y = -100
    boost_speed = 10
    active = False
    active_time = 0

    def move(self):
        self.rect.y += 3
        if self.rect.y > 1500:
            self.rect.y = -2000


class Health:
    image = pygame.image.load("Img/Heal.png")
    rect = image.get_rect()
    rect.x = random.randint(10, 1850)
    rect.y = -10000

    def move(self):
        self.rect.y += 3
        if self.rect.y > 1500:
            self.rect.y = -4000


class BackGround:
    layer1 = 0
    layer2 = 0
    bg_1 = pygame.image.load("Img/Bg_1_level.jpg")
    bg_2 = pygame.image.load("Img/Bg_2_level.jpg")
    bg_3 = pygame.image.load("Img/BG2.png")
    boom = pygame.image.load("Img/Boom.png")
    font_score = pygame.font.SysFont("Arial", 26, bold=True)
    death = pygame.font.SysFont("Arial", 40, bold=True)
    score = 0


class Menu:
    level = 1
    select = 197
    select_ship = 297
    main_menu = True
    choose_level = False
    choose_ship = False
    img_select = pygame.image.load("Img/select.png")
    img_ship_select = pygame.image.load("Img/Ship_selector.png")
    ship_choose = pygame.image.load("Img/Ship_choose.png")
    ship_fon = pygame.image.load("Img/Ship_Fon.png")
    level_choose = pygame.image.load("Img/Level_chooser.png")


class Music:
    pygame.mixer.music.load("music/game_music.ogg")
    shield = pygame.mixer.Sound("music/Shield.ogg")
    shot = pygame.mixer.Sound("music/player_shot.ogg")
    reload = pygame.mixer.Sound("music/reload.ogg")
    speed_up = pygame.mixer.Sound("music/speed_up.ogg")
    break_shield = pygame.mixer.Sound("music/break_shield.ogg")
    laser = pygame.mixer.Sound("music/laser.ogg")
    rocket = pygame.mixer.Sound("music/rocket.ogg")
    death = pygame.mixer.Sound("music/dead.ogg")
    boom_P = pygame.mixer.Sound("music/Boom.ogg")
    boss_boom = pygame.mixer.Sound("music/BossExplosion.wav")
    music_start = False


def draw_menu():
    window.blit(pygame.image.load("Img/menu_fon.png"), (0, 0))
    if not Menu.choose_ship:
        window.blit(Menu.img_select, (195, Menu.select))
    if Menu.main_menu:
        window.blit(pygame.image.load("Img/Ship_Launch.png"), (200, 200))
        window.blit(pygame.image.load("Img/Choose_Level.png"), (200, 300))
        window.blit(pygame.image.load("Img/Choose_Ship.png"), (200, 400))
        window.blit(pygame.image.load("Img/close_interface.png"), (200, 500))
    if Menu.choose_level:
        window.blit(Menu.level_choose, (195, 95 + Menu.level * 100))
        window.blit(pygame.image.load("Img/Level_1.png"), (200, 200))
        window.blit(pygame.image.load("Img/Level_2.png"), (200, 300))
        window.blit(pygame.image.load("Img/Level_3.png"), (200, 400))
        window.blit(pygame.image.load("Img/Level_4.png"), (200, 500))
        window.blit(pygame.image.load("Img/Cancel.png"), (200, 600))
    if Menu.choose_ship:
        window.blit(Menu.ship_fon, (297, 298))
        window.blit(Player.image, (300, 300))
        window.blit(Menu.ship_fon, (397, 298))
        window.blit(Player.image_y, (400, 300))
        window.blit(Menu.ship_fon, (497, 298))
        window.blit(Player.image_bl, (500, 300))
        window.blit(Menu.ship_fon, (597, 298))
        window.blit(Player.image_p, (600, 300))
        if Player.ship_color == "y":
            window.blit(Menu.ship_choose, (397, 298))
        elif Player.ship_color == "bl":
            window.blit(Menu.ship_choose, (497, 298))
        elif Player.ship_color == "p":
            window.blit(Menu.ship_choose, (597, 298))
        else:
            window.blit(Menu.ship_choose, (297, 298))
    if Menu.choose_ship:
        window.blit(Menu.img_ship_select, (Menu.select_ship, 298))


def action():
    if BackGround.layer2 + 2 >= 0:  # передвижение заднего фона
        BackGround.layer1 = 0
        if Menu.level == 1:
            BackGround.layer2 = -1010
        elif Menu.level == 2:
            BackGround.layer2 = -2000
        elif Menu.level == 3:
            BackGround.layer2 = -1080
        elif Menu.level == 4:
            BackGround.layer2 = -1080
    else:
        BackGround.layer1 += 2
        BackGround.layer2 += 2

    for bullet in bullets:  # полет пули
        if - 1000 < bullet.rect.y < 1090:
            bullet.move()
            if bullet.dmg == 2:
                if bullet.active_time == 0:
                    bullets.pop(bullets.index(bullet))
        else:
            bullets.pop(bullets.index(bullet))

    if Menu.level == 1:
        if random.randint(0, 5) > 4:
            enemies.append(Meteor())  # спавн врагов
    elif Menu.level == 2:
        if random.randint(0, 100) > 95:
            enemies.append(Enemy_rocket_launcher())
        if random.randint(0, 5) > 4:
            enemies.append(Enemy_suicide(random.randint(10, 1850), -10))
    elif Menu.level == 3:
        if random.randint(0, 100) > 95:
            enemies.append(Enemy_rocket_launcher())
        if random.randint(0, 100) > 98:
            enemies.append(Enemy_sniper())
        if random.randint(0, 5) > 4:
            enemies.append(Enemy_suicide(random.randint(10, 1850), -10))
    elif Menu.level == 4:
        if Boss.bomber_cd == 0:
            enemies.append(Enemy_suicide(50, -10))
            enemies.append(Enemy_suicide(1820, -10))
            Boss.bomber_cd = 70
        elif Boss.bomber_cd > 0:
            Boss.bomber_cd -= 1
        if not Boss.spawn:
            boss.append(Boss())
            boss.append(Boss_gun(-204, -50))
            boss.append(Boss_gun(-68, 8))
            boss.append(Boss_gun(118, 8))
            boss.append(Boss_gun(256, -50))
            boss.append(Boss_engine(-135, -188))
            boss.append(Boss_engine(187, -188))
            Boss.spawn = True

        for bos in boss:
            bos.move()
            if Player.rect.colliderect(bos.rect):
                Player.hp = 0
            for bullet in bullets:
                if pygame.sprite.collide_rect(bos, bullet):
                    if bos.hp > 0:
                        bos.hp -= 1
                    if bullet.dmg != 2:
                        bullets.pop(bullets.index(bullet))
            if bos.can_shoot:
                bos.shoot()
            if bos.body:
                if bos.hp <= 0:
                    Boss.get_killed = True
                    Music.boss_boom.play()

    for enemy in enemies:  # передвижение врага, проверка на хп, стрельба
        enemy.move()
        if enemy.can_shoot and enemy.cd == 0:
            enemy.shoot()
            enemy.cd = 90
        elif enemy.can_shoot and enemy.cd > 0:
            enemy.cd -= 1
        if enemy.hp <= 0:  # удаление врагов
            window.blit(BackGround.boom, (enemy.rect.x, enemy.rect.y))
            enemies.pop(enemies.index(enemy))
            BackGround.score += 1
            Music.death.play()
        if enemy.rect.y > 1090:
            enemies.pop(enemies.index(enemy))

    for enemy in enemies:  # столкновение с игроком
        if Player.rect.colliderect(enemy.rect):
            window.blit(BackGround.boom, (enemy.rect.x, enemy.rect.y))
            enemies.pop(enemies.index(enemy))
            BackGround.score += 10
            Music.death.play()
            if Player.shield_hp > 0:
                if Player.shield_hp - enemy.dmg > 0:
                    Player.shield_hp -= enemy.dmg
                else:
                    Player.shield_hp = 0
                    Music.break_shield.play()
            else:
                if Player.hp - enemy.dmg > 0:
                    Player.hp -= enemy.dmg
                else:
                    Player.hp = 0

    for bullet in bullets:  # столкновение игрока и пуль
        if Player.rect.colliderect(bullet.rect) and bullet.dmg != 2:
            if Player.shield_hp > 0:
                if Player.shield_hp - bullet.dmg > 0:
                    Player.shield_hp -= bullet.dmg
                else:
                    Player.shield_hp = 0
                    Music.break_shield.play()
            else:
                if Player.hp - bullet.dmg > 0:
                    Player.hp -= bullet.dmg
                else:
                    Player.hp = 0
            bullets.pop(bullets.index(bullet))

    for enemy in enemies:  # столкновение врага с пулей
        for bullet in bullets:
            if pygame.sprite.collide_rect(enemy, bullet):
                enemy.hp -= bullet.dmg
                if bullet.dmg != 2:
                    bullets.pop(bullets.index(bullet))

    if Player.rect.colliderect(Boost.rect):  # поднятие буста
        Boost.active = True
        Boost.rect.y = -2000
        Boost.rect.x = random.randint(10, 1900)
        Boost.active_time = 70
        Boost.boost_speed = 10
        Music.speed_up.play()
    Boost().move()  # передвижение буста
    if Boost.active_time > 0:  # перезарядка буста
        Boost.active_time -= 1
    else:
        Boost.active = False
        Boost.boost_speed = 0

    if Player.rect.colliderect(Health.rect):
        if Player.hp < Player.max_hp:
            Player.hp += 1
        Health.rect.y = -2000
        Health.rect.x = random.randint(10, 1900)
    Health().move()

    if Player.rocket_cd > 0:  # перезарядка ракет
        Player.rocket_cd -= 1

    if Player.gun_cd <= 0 and Player.gun_freeze == 0:  # перезарядка осн пушки
        Player.gun_freeze = 60
        Music.reload.play()
    if Player.gun_freeze > 0:
        Player.gun_freeze -= 1
    if Player.gun_cd < 100:
        Player.gun_cd += 1

    if Player.shield_cd > 0 and Player.shield_hp == 0:  # перезарядка щита
        Player.shield_cd -= 1
    if Player.shield_active_time > 0:
        Player.shield_active_time -= 1
    elif Player.shield_active_time == 0:
        Player.shield_hp = 0
        Music.break_shield.play()
        Player.shield_active_time = -1

    if Player.laser_cd > 0:
        Player.laser_cd -= 1


def respawn():
    Player.hp = Player.max_hp
    enemies.clear()
    bullets.clear()
    boss.clear()
    Boss.spawn = False
    Player.rect.x = 900
    Player.rect.y = 600
    Music.music_start = False
    Boost.rect.y = -100
    Boost.rect.x = random.randint(10, 1850)
    Health.rect.x = random.randint(10, 1850)
    Health.rect.y = -10000


def draw_level():
    if Menu.level == 1:
        window.blit(BackGround.bg_1, (0, BackGround.layer1))  # Отрисовка заднего фона
        window.blit(BackGround.bg_1, (0, BackGround.layer2))
    elif Menu.level == 2:
        window.blit(BackGround.bg_2, (-58, BackGround.layer1))
        window.blit(BackGround.bg_2, (952, BackGround.layer1))
        window.blit(BackGround.bg_2, (-58, BackGround.layer2))
        window.blit(BackGround.bg_2, (952, BackGround.layer2))
    elif Menu.level == 3:
        window.blit(BackGround.bg_3, (0, BackGround.layer1))  # Отрисовка заднего фона
        window.blit(BackGround.bg_3, (0, BackGround.layer2))
    elif Menu.level == 4:
        window.blit(BackGround.bg_3, (0, BackGround.layer1))  # Отрисовка заднего фона
        window.blit(BackGround.bg_3, (0, BackGround.layer2))
        window.blit(Boss.image_ship, (Boss.rect.x - 204, Boss.rect.y - 204))
        for bos in boss:
            window.blit(bos.image, (bos.rect.x, bos.rect.y))
            if bos.body:
                if bos.hp <= 0:
                    window.blit(BackGround.death.render(f"You WIN!!!", True, (255, 100, 10)), (740, 350))
                    window.blit(BackGround.death.render(f"Press ESC to go to Menu", True, (255, 100, 10)), (720, 400))
                for i in range(bos.hp):
                    window.blit(Player.img_1_r, (100 + i * 3, 900))
                for i in range(bos.hp, Boss.max_hp):
                    window.blit(Player.img_0_t, (100 + i * 3, 900))

    window.blit(Boost.image, (Boost.rect.x, Boost.rect.y))
    window.blit(Health.image, (Health.rect.x, Health.rect.y))

    for enemy in enemies:  # Отриовка врагов
        window.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

    for bullet in bullets:  # Отрисовка пуль
        window.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

    if Menu.level != 4:      # счет
        render_score = BackGround.font_score.render(f"Score: {BackGround.score}", True, (255, 100, 10))
        window.blit(render_score, (1750, 20))


def draw_player():
    if Player.ship_color == "default":
        if Player.p_left:  # Отрисовка игрока
            window.blit(Player.img_l, (Player.rect.x, Player.rect.y))
        elif Player.p_right:
            window.blit(Player.img_r, (Player.rect.x, Player.rect.y))
        else:
            window.blit(Player.image, (Player.rect.x, Player.rect.y))
    elif Player.ship_color == "y":
        if Player.p_left:
            window.blit(Player.img_l_y, (Player.rect.x, Player.rect.y))
        elif Player.p_right:
            window.blit(Player.img_r_y, (Player.rect.x, Player.rect.y))
        else:
            window.blit(Player.image_y, (Player.rect.x, Player.rect.y))
    elif Player.ship_color == "bl":
        if Player.p_left:
            window.blit(Player.img_l_bl, (Player.rect.x, Player.rect.y))
        elif Player.p_right:
            window.blit(Player.img_r_bl, (Player.rect.x, Player.rect.y))
        else:
            window.blit(Player.image_bl, (Player.rect.x, Player.rect.y))
    elif Player.ship_color == "p":
        if Player.p_left:
            window.blit(Player.img_l_p, (Player.rect.x, Player.rect.y))
        elif Player.p_right:
            window.blit(Player.img_r_p, (Player.rect.x, Player.rect.y))
        else:
            window.blit(Player.image_p, (Player.rect.x, Player.rect.y))

    for i in range(Player.hp):  # отрисовка хп
        window.blit(Player.img_hp1, (30 * (i + 1), 10))
    for i in range(Player.hp, Player.max_hp):
        window.blit(Player.img_hp0, (30 * (i + 1), 10))
    for i in range(Player.shield_hp):
        window.blit(Player.img_hp_g, (30 * (i + 1), 10))

    for i in range(Player.gun_cd):  # бар перезарядки оружия
        if Player.gun_freeze == 0:
            window.blit(Player.img_1_t, (20 + 3 * i, 40))
        else:
            window.blit(Player.img_1_r, (20 + 3 * i, 40))
    for i in range(Player.gun_cd, 100):
        window.blit(Player.img_0_t, (20 + 3 * i, 40))

    if Player.rocket_cd > 0:  # перезарядка ракет
        window.blit(Player.img_r_r, (20, 70))
    else:
        window.blit(Player.img_r_g, (20, 70))

    if Player.shield_active_time > 0 and Player.shield_hp > 0 and Player.shield_cd != 0:  # отрисовка щита
        window.blit(Player.img_shield_p, (70, 70))
        window.blit(Player.img_shield, (Player.rect.x - 4, Player.rect.y - 4))
    elif Player.shield_cd == 0:
        window.blit(Player.img_shield_g, (70, 70))
    else:
        window.blit(Player.img_shield_r, (70, 70))

    if Player.laser_cd > 0:
        window.blit(Player.img_l_i_r, (120, 70))
    else:
        window.blit(Player.img_l_i_g, (120, 70))

    if Boost.active_time > 0:  # отрисовка буста в статах
        window.blit(Boost.image, (170, 70))

    if Player.hp == 0:
        window.blit(Player.img_boom, (Player.rect.x, Player.rect.y))
        window.blit(BackGround.death.render(f"Press ESC to go to Menu", True, (255, 100, 10)), (720, 400))


while game_run:  # Цикл игры
    keys = pygame.key.get_pressed()  # Обработка нажатий

    if game_started:
        if not Music.music_start:
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            Music.music_start = True
        draw_level()
        draw_player()
        if Player.hp > 0 and not Boss.get_killed:
            action()
            if keys[pygame.K_a] and Player.rect.x > 15:
                Player.rect.x -= 15 + Boost.boost_speed
                Player.p_left = True
                Player.p_right = False
            elif keys[pygame.K_d] and Player.rect.x < 1823:
                Player.rect.x += 15 + Boost.boost_speed
                Player.p_left = False
                Player.p_right = True
            else:
                Player.p_left = False
                Player.p_right = False
            if keys[pygame.K_w] and Player.rect.y > 15:
                Player.rect.y -= 15 + Boost.boost_speed
            if keys[pygame.K_s] and Player.rect.y < 935:
                Player.rect.y += 15 + Boost.boost_speed
            if keys[pygame.K_SPACE]:
                if Player.gun_cd > 0 and Player.gun_freeze == 0:
                    bullets.append(Bullet())
                    Player.gun_cd -= 3
                    Music.shot.play()
            if keys[pygame.K_q]:
                if Player.rocket_cd == 0:
                    bullets.append(Rocket())
                    Player.rocket_cd = 100
                    Music.rocket.play()
            if keys[pygame.K_e]:
                if Player.laser_cd == 0:
                    bullets.append(Laser())
                    Player.laser_cd = 350
                    Music.laser.play()
            if keys[pygame.K_f]:
                if Player.shield_cd == 0:
                    Player.shield_hp = 3
                    Player.shield_active_time = 250
                    Player.shield_cd = 500
                    Music.shield.play()
            if keys[pygame.K_ESCAPE]:
                game_started = False
                respawn()
        elif Player.hp <= 0:  # смерть
            if not Player.die:
                Music.boom_P.play()
                Player.die = True
            if keys[pygame.K_ESCAPE]:
                game_started = False
                respawn()
        elif Menu.level == 4 and Boss.get_killed:
            if keys[pygame.K_ESCAPE]:
                game_started = False
                respawn()
                Boss.get_killed = False

    else:  # меню
        draw_menu()
        pygame.mixer.music.stop()
        if keys[pygame.K_UP] and not Menu.choose_ship:
            if Menu.select > 200:
                Menu.select -= 100
        if keys[pygame.K_DOWN] and not Menu.choose_ship:
            if Menu.main_menu:
                if Menu.select < 400:
                    Menu.select += 100
            elif Menu.choose_level:
                if Menu.select < 500:
                    Menu.select += 100
        if keys[pygame.K_RIGHT] and Menu.choose_ship:
            if Menu.select_ship < 501:
                Menu.select_ship += 100
        if keys[pygame.K_LEFT] and Menu.choose_ship:
            if Menu.select_ship > 301:
                Menu.select_ship -= 100
        if keys[pygame.K_SPACE]:
            if Menu.main_menu:
                if Menu.select == 197:
                    game_started = True
                if Menu.select == 297:
                    Menu.choose_level = True
                    Menu.main_menu = False
                if Menu.select == 397:
                    Menu.choose_ship = True
                    Menu.main_menu = False
                if Menu.select == 497:
                    game_run = False
            if Menu.choose_level:
                if Menu.select == 197:
                    Menu.level = 1
                if Menu.select == 297:
                    Menu.level = 2
                if Menu.select == 397:
                    Menu.level = 3
                if Menu.select == 497:
                    Menu.level = 4
                if Menu.select == 597:
                    Menu.choose_level = False
                    Menu.main_menu = True
                    Menu.select = 197
            if Menu.choose_ship:
                if Menu.select_ship == 297:
                    Player.ship_color = "default"
                if Menu.select_ship == 397:
                    Player.ship_color = "y"
                if Menu.select_ship == 497:
                    Player.ship_color = "bl"
                if Menu.select_ship == 597:
                    Player.ship_color = "p"
        if keys[pygame.K_ESCAPE]:
            Menu.select = 197
            if Menu.choose_level:
                Menu.choose_level = False
                Menu.main_menu = True
            if Menu.choose_ship:
                Menu.choose_ship = False
                Menu.main_menu = True

    for event in pygame.event.get():  # цикл обработки событий
        if event.type == pygame.QUIT:
            game_run = False

    pygame.display.update()
    pygame.time.delay(30)
