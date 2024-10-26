from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, char_img, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(char_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        

class Player(GameSprite):
    def playerLeft(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

    def playerRight(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")

clock = time.Clock()
FPS = 60

playerLeft = Player("ping_pong_player.png", 2, win_height/2, 45, 100, 7)
playerRight = Player("ping_pong_player.png", win_width - 49, win_height/2, 45, 100, 7)
ball = GameSprite("ping_pong_ball.png", win_width/2, win_height/2, 40, 40, 2)

ball_move_X = ball.speed
ball_move_y = ball.speed

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill((0, 0, 0))

        ball.rect.x += ball_move_X
        ball.rect.y += ball_move_y

        if ball.rect.y < 0:
            ball_move_y = ball.speed
        if ball.rect.y > win_height - 40:
            ball_move_y = -ball.speed

        #-Detecting if the ball collides with a player

        if sprite.collide_rect(ball, playerLeft):
            ball_move_X = ball.speed
            print("Touched left", ball_move_X)
        if sprite.collide_rect(ball, playerRight):
            print("Touched right", ball_move_X)
            ball_move_X = -ball.speed

        #-Detecting if a player loses

        if ball.rect.x <= 0:
            print("Player Left Lost!")
            finish = True

        if ball.rect.x >= win_width - 40:
            print("Player Right Lost!")
            finish = True
        
        #-Updating Everything

        playerLeft.playerLeft()
        playerRight.playerRight()
        playerLeft.update()
        playerRight.update()
        ball.update()

        display.update()
        clock.tick(FPS)