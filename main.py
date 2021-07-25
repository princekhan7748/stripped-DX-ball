#   Library initialization

import pygame

#   Module initialization

pygame.init()

#   Screen resolutions

screen_width = 800
screen_height = 600

#   Images

Background = pygame.image.load('b2.png')
Icon = pygame.image.load('ufo.png')

#   Texts

pygame.display.set_caption("DX ball")

#   Clock

clock = pygame.time.Clock()

#   Score

score = 0


#   Classes


class Paddle:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.w, self.h])


class Ball(Paddle):
    def __init__(self, x, y, w, h, color, s):
        super().__init__(x, y, w, h, color)
        self.xv = 1
        self.yv = 1
        self.status = s

    def move(self):
        self.x += self.xv
        self.y += self.yv

    def draw(self, window):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.w)


class Brick(Paddle):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)
        self.xx = self.x + self.w
        self.yy = self.y + self.h


#   Methods


def Display_updater(Text, x, y, s):
    screen.blit(Background, (0, 0))
    player.draw(screen)
    ball.draw(screen)
    for b in bricks:
        b.draw(screen)
    Text_displayer(Text, x, y, s)
    pygame.display.update()


def brick_initialization():
    global bricks
    bricks = []
    for i in range(6):
        for j in range(10):
            bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (120, 205, 250)))


def Text_displayer(Text, x, y, s):
    Super_font = pygame.font.Font('freesansbold.ttf', s)
    Over_text = Super_font.render(Text, True, (255, 255, 0))
    screen.blit(Over_text, (x, y))


def Lose():
    screen.blit(Background, (0, 0))
    Text_displayer("Game Over", 184, 264, 64)
    Text_displayer("Your score: " + str(score), 300, 450, 16)
    pygame.display.update()


def Won():
    screen.blit(Background, (0, 0))
    Text_displayer("You won", 184, 264, 64)
    Text_displayer("Your score: " + str(score), 300, 450, 16)
    pygame.display.update()


#   Game object initialization

bricks = []
player = Paddle(screen_width - 100, screen_height - 20, 100, 20, (255, 255, 0))
ball = Ball(player.x + 10, player.y - 20, 20, 20, (255, 255, 255), False)
attempts = 2
brick_initialization()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(Icon)

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
                if not ball.status:
                    ball = Ball(player.x + ball.w, player.y - 20, 20, 20, (255, 255, 255), True)
            if event.key == pygame.K_r:
                if attempts == 0:
                    attempts = 2
                    brick_initialization()
                    score = 0
    if attempts > 0:
        if ball.status:
            ball.move()
        else:
            ball.x = player.x + ball.w
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
        if ball.x <= ball.w:
            ball.xv *= -1
        if ball.y <= ball.w:
            ball.yv *= -1

        #   Bricks

        for brick in bricks:
            if ball.y <= brick.y + brick.h + ball.w:
                if brick.x - ball.w <= ball.x <= brick.x + brick.w + ball.w:
                    ball.xv = -ball.xv
                    brick.visible = False
                    bricks.pop(bricks.index(brick))
                    score += 1
                    break
            elif (brick.x <= ball.x <= brick.x + brick.w + ball.w) or brick.x <= ball.x <= brick.x + ball.w:
                if (brick.y <= ball.y <= brick.y + ball.w) or brick.y <= ball.y + ball.h <= brick.y + brick.w:
                    brick.visible = False
                    bricks.pop(bricks.index(brick))
                    ball.yv *= -1
                    score += 1
                    break
        Display_updater("Score: " + str(score), 10, 10, 16)
        #   Game Over

        if ball.y > 650:
            attempts -= 1
            ball = Ball(player.x, player.y - ball.h, 20, 20, (255, 255, 255), False)
        if attempts == 0:
            Lose()
        if len(bricks) == 0:
            Won()
            attempts = 0
