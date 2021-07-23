#   Library initialization

import pygame

#   Module initialization

pygame.init()

#   Screen resolutions

screen_width = 800
screen_height = 600

#   Images

Background = pygame.image.load('b2.png')
screen = pygame.display.set_mode((screen_width, screen_height))

#   Texts

pygame.display.set_caption("Break")
Super_font = pygame.font.Font('freesansbold.ttf', 64)

#   Clock

clock = pygame.time.Clock()


#   Classes


class Paddle:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])


class Ball(Paddle):
    def __init__(self, x, y, w, h, color, s):
        super().__init__(x, y, w, h, color)
        self.xv = 1
        self.yv = 1
        self.status = s

    def move(self):
        self.x += self.xv
        self.y += self.yv

    def draw(self, win):
        pygame.draw.circle(win, self.color, [self.x, self.y], self.w)


class Brick(Paddle):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)
        self.xx = self.x + self.w
        self.yy = self.y + self.h


#   Methods

def Display_updater():
    screen.blit(Background, (0, 0))
    player.draw(screen)
    ball.draw(screen)
    for b in bricks:
        b.draw(screen)
    pygame.display.update()


def init():
    global bricks
    bricks = []
    for i in range(6):
        for j in range(10):
            bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (120, 205, 250)))


def Game_Over():
    Over_text = Super_font.render("Game Over", True, (255, 255, 0))
    screen.blit(Background, (0, 0))
    screen.blit(Over_text, (200, 300))
    pygame.display.update()


#   Game object initialization

bricks = []
player = Paddle(350, 500, 100, 20, (255, 255, 0))
ball = Ball(player.x, player.y - 30, 20, 20, (255, 255, 255), False)
attempts = 1
init()

#   Game loop

running = True
while running:
    clock.tick(100)

#   Input settings

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if attempts > 0:
                    ball = Ball(player.x, player.y - 30, 20, 20, (255, 255, 255), True)
    if attempts > 0:
        if ball.status:
            ball.move()
        else:
            ball.x = player.x
        if pygame.mouse.get_pos()[0] - player.w // 2 < 0:
            player.x = 0
        elif pygame.mouse.get_pos()[0] + player.w // 2 > screen_width:
            player.x = screen_width - player.w
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w // 2

#   Boundaries

        if (player.x <= ball.x <= player.x + player.w) or (player.x <= ball.x + ball.w <= player.x + player.w):
            if player.y <= ball.y + ball.h <= player.y + player.h:
                ball.yv *= -1
                ball.y = player.y - ball.h - 1
        if ball.x + ball.w >= screen_width:
            ball.xv *= -1
        if ball.x < 0:
            ball.xv *= -1
        if ball.y <= 0:
            ball.yv *= -1

#   Bricks

        for brick in bricks:
            if (brick.x <= ball.x <= brick.x + brick.w) or brick.x <= ball.x + ball.w <= brick.x + brick.w:
                if (brick.y <= ball.y <= brick.y + brick.h) or brick.y <= ball.y + ball.h <= brick.y + brick.h:
                    brick.visible = False
                    bricks.pop(bricks.index(brick))
                    ball.yv *= -1
        Display_updater()

#   Game Over

        if ball.y > 650:
            attempts -= 1
        if attempts == 0:
            Game_Over()
