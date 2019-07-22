import pygame
import random
from os import path

WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768

FPS = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (100, 100, 200)


def draw_text(surf, text, size, x, y, color):
    COLOR = color
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

player_imgblue = pygame.image.load(path.join(img_dir, "big circle.png")).convert()
player_imgred = pygame.image.load(path.join(img_dir, "big circle red first.png")).convert()

redcircle = pygame.image.load(path.join(img_dir, "Unknown.png")).convert()
bluecircle = pygame.image.load(path.join(img_dir, "Unknown-1.png")).convert()

background = pygame.image.load(path.join(img_dir, "colorful.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()


class BigCircle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice((player_imgblue, player_imgred))
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT // 2
        self.rect.centerx = WIDTH // 2
        self.otherimage = player_imgred
        if self.image == player_imgred:
            self.otherimage = player_imgblue
        self.otherimage = pygame.transform.scale(self.otherimage, (250, 250))
        self.image.set_colorkey(WHITE)
        self.score = 0
        self.highscore = 0
        self.colorup = "BLUE"
        self.colordown = "RED"
        if self.image == player_imgred:
            self.colorup, self.colordown = self.colordown, self.colorup
        self.lives = 3
        self.lastpressed = -30
        self.time_between_pressed = 80

    def update(self):
        KEYSTATE = pygame.key.get_pressed()
        if KEYSTATE[pygame.K_SPACE] and pygame.time.get_ticks() - self.lastpressed > self.time_between_pressed:
            self.image, self.otherimage = self.otherimage, self.image
            self.rect = self.image.get_rect()
            self.rect.centery = HEIGHT // 2
            self.rect.centerx = WIDTH // 2
            self.image.set_colorkey(WHITE)
            self.colordown, self.colorup = self.colorup, self.colordown
            self.lastpressed = pygame.time.get_ticks()


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.ImageOrig = random.choice((redcircle, bluecircle))
        self.image = pygame.transform.scale(self.ImageOrig, (self.size, self.size))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = random.choice((HEIGHT // 4 * 3 + 150, (HEIGHT // 4) - 150))
        self.rect.centerx = WIDTH // 2
        self.pos = self.rect.centerx
        if self.ImageOrig == bluecircle:
            self.color = "BLUE"
        elif self.ImageOrig == redcircle:
            self.color = "RED"
        self.scaleamount = 5
        self.animationspeed = 12
        self.animationtime = pygame.time.get_ticks()
        self.speed = 4
        if self.rect.centery == HEIGHT // 4 * 3 + 150:
            self.speed = -4
        self.howbig = 60

    def reset(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.ImageOrig = random.choice((redcircle, bluecircle))
        self.image = pygame.transform.scale(self.ImageOrig, (self.size, self.size))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = random.choice((HEIGHT // 4 * 3 + 150, (HEIGHT // 4) - 150))
        self.rect.centerx = WIDTH // 2
        self.pos = self.rect.centerx
        if self.ImageOrig == bluecircle:
            self.color = "BLUE"
        elif self.ImageOrig == redcircle:
            self.color = "RED"
        self.animationtime = pygame.time.get_ticks()
        if self.rect.centery == HEIGHT // 4 * 3 + 150 and self.speed > 0 or self.rect.centery == (
                HEIGHT // 4) - 150 and self.speed < 0:
            self.speed *= -1

    def animation(self):
        oldcenter = self.rect.center
        if pygame.time.get_ticks() - self.animationtime > self.animationspeed:
            self.size += self.scaleamount
            if self.size > self.howbig:
                self.size = self.howbig
            self.image = pygame.transform.scale(self.ImageOrig, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = oldcenter
            self.image.set_colorkey(WHITE)

    def update(self):
        if self.size < self.howbig:
            self.animation()

        else:
            self.rect.centery += self.speed


def draw_go_window(text1, text2, text3, TEXT4=False, text3size=55):
    while True:
        screen.blit(background, background_rect)
        draw_text(screen, text1, 45, WIDTH // 2, 250, (0, 168, 107))
        draw_text(screen, text2, 50, WIDTH // 2, HEIGHT // 2, PURPLE)
        if not TEXT4:
            draw_text(screen, text3, text3size, WIDTH // 2, HEIGHT // 2 + 150, BLUE)
        if TEXT4:
            draw_text(screen, text3, text3size, WIDTH // 2, HEIGHT // 2 + 100, RED)
            draw_text(screen, TEXT4, text3size - 8, WIDTH // 2, HEIGHT // 2 + 160, (255, 211, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                return True


all_sprites = pygame.sprite.Group()
mob = pygame.sprite.Group()
player = BigCircle()
all_sprites.add(player)
ball = Mob()
mob.add(ball)
all_sprites.add(ball)

playing = draw_go_window("welcome to color switch , a colorful addictive and simple game"
                         , "today im going to be your caption in this ocean of colors",
                         "you know how to player GOOD LUCK and GG's only")
running = True
while running:
    if not playing:
        playing = draw_go_window("seems like our sail has sinked in the ocean of colors",
                                 "no wories lets come out and be more colorful than ever",
                                 "are you ready to continui this colorfull and faboules journey",
                                 "if yes press a colorful button on your colorful keyboard and lets get back on the SHIP OF DREAMS",
                                 40)
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    hits = pygame.sprite.spritecollide(player, mob, False)
    if hits:
        colorlist = [player.colorup, player.colordown]
        if ball.rect.y > HEIGHT // 2:
            index = 1
        else:
            index = 0
        print(colorlist[index])
        if colorlist[index] == ball.color:
            player.score += 1
            ball.reset()
            if player.score - player.score // 2 * 2 == 0:
                if ball.speed > 0:
                    ball.speed += 1
                elif ball.speed < 0:
                    ball.speed += -1
                ball.scaleamount += 1
                if ball.speed > 7 and player.score <= 15:
                    ball.speed = 7
                elif ball.speed < -7 and player.score <= 15:
                    ball.speed = -7
                elif player.score > 15 and player.score < 25 and ball.speed > 10:
                    ball.speed = 10
                elif player.score > 15 and player.score < 25 and ball.speed < -10:
                    ball.speed = -1
                elif player.score >= 25 and player.score <= 35 and ball.speed < -13:
                    ball.speed = -13
                elif player.score >= 25 and player.score <= 35 and ball.speed > 13:
                    ball.speed = 13
                elif player.score > 35 and ball.speed > 16:
                    ball.speed = 16
                elif player.score > 35 and ball.speed < -16:
                    ball.speed = -16

                if ball.scaleamount > ball.howbig // 2:
                    ball.scaleamount = ball.howbig // 2
        else:
            player.lives -= 1
            if player.lives <= 0:
                playing = False
                all_sprites = pygame.sprite.Group()
                mob = pygame.sprite.Group()
                player = BigCircle()
                all_sprites.add(player)
                ball = Mob()
                mob.add(ball)
                all_sprites.add(ball)
            ball.reset()

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()
    print(player.score, player.lives)

pygame.quit()
