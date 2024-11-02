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

playerLeft = Player("ping_pong_player.png", 2, win_height/2, 20, 100, 7)
playerRight = Player("ping_pong_player.png", win_width - 25, win_height/2, 20, 100, 7)
ball = GameSprite("ping_pong_ball.png", win_width/2, win_height/2, 27, 27, 2)

ball_move_X = ball.speed
ball_move_y = ball.speed

game = True
finish = False

phase = 1

hit_count = 0

bg_red = 0

font.init()
font1 = font.SysFont("Terminal", 30)
text1 = font1.render("Player Right Wins!", True, (255,255,255))
text2 = font1.render("Player Left Wins!", True, (255,255,255))

#--Music
mixer.init()

#--General Sounds
ball_hit = mixer.Sound("Ping_Pong_Ball_Hit.wav")
ball_hit.set_volume(1)

game_end = mixer.Sound("Ping_Pong_End.wav")
game_end.set_volume(1)

#--Phase One
mixer.music.load("Ping_Pong_Phase_One.wav")
mixer.music.set_volume(0.8)

#--Loading Phase One Music
mixer.music.play(-1)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill((bg_red, 0, 0))

        ball.rect.x += ball_move_X
        ball.rect.y += ball_move_y

        if ball.rect.y < 0:
            ball_move_y = ball.speed
        if ball.rect.y > win_height - 40:
            ball_move_y = -ball.speed

        #-Detecting if the ball collides with a player

        if sprite.collide_rect(ball, playerLeft):
            ball.speed += 0.15
            ball_move_X = ball.speed
            print("Touched left", ball_move_X)
            ball_hit.play()
            hit_count += 1
            bg_red += 3
        if sprite.collide_rect(ball, playerRight):
            ball.speed += 0.15
            ball_move_X = -ball.speed
            print("Touched right", ball_move_X)
            ball_hit.play()    
            hit_count += 1
            bg_red += 3

        if hit_count >= 15 and phase == 1:
            phase = 2
            mixer.music.load("Ping_Pong_Phase_Two_2.wav") 
            mixer.music.set_volume(0.9)
            mixer.music.play(-1)

        if hit_count >= 30 and phase == 2:
            phase = 3
            mixer.music.load("Ping_Pong_Phase_Three.wav") 
            mixer.music.set_volume(1)
            mixer.music.play(-1)

        if bg_red >= 200:
            bg_red = 200


        #-Detecting if a player loses

        if ball.rect.x <= 0:
            print("Player Left Lost!")
            window.fill((0, 0, 0))
            window.blit(text1, (win_width/2, win_height/2))
            finish = True
            mixer.music.stop()

        if ball.rect.x >= win_width - 27:
            print("Player Right Lost!")
            window.fill((0, 0, 0))
            window.blit(text2, (win_width/2, win_height/2))
            finish = True
            mixer.music.stop()

        if finish == True:
            game_end.play()
            mixer.music.load("Ping_Pong_Game_Over.wav") 
            mixer.music.set_volume(0.75)
            mixer.music.play(-1)


        #-Updating Everything

        playerLeft.playerLeft()
        playerRight.playerRight()
        playerLeft.update()
        playerRight.update()
        ball.update()

        display.update()
        clock.tick(FPS)