from pygame import *

import random
import time as timer

window_width = 1300
window_height = 700
window = display.set_mode( (window_width, window_height) )

bg = transform.scale(image.load("tennis_court.png"), (window_width, window_height))

class Character(sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(filename),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.w = w
        self.h = h
    def draw (self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Racket(Character):
    def __init__(self, filename, x, y, w, h, speed, score):
        super().__init__(filename, x, y, w, h, speed,)
        self.score = score

class Ball(Character):
    def __init__(self, filename, x, y, w, h, speed):
        super().__init__(filename, x, y, w, h, speed)
        self.speed_x = self.speed
        self.speed_y = self.speed

        self.rotate_speed = 3
        self.angle = 0
        self.rotate_image = self.image
        self.rotate_rect = self.rotate_image.get_rect()
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y 
        if self.rect.y > window_height - self.h:
            self.speed_y *= -1
       
        elif self.rect.y < 0:
            self.speed_y *= -1
    def rotate(self):
        self.angle += self.rotate_speed
        self.rotate_image = transform.rotate(self.image, self.angle)
        self.rotate_rect = self.rotate_image.get_rect(center=(self.rect.x, self.rect.y))
    def draw (self):
        window.blit(self.rotate_image,(self.rotate_rect.x,self.rotate_rect.y))







ball = Ball("Pokemon.png", 300, 50, 100, 100, 4)
player2 = Racket("Red_Sword.png", 1250, 250, 30, 250, 5, 0)#Green
player1 = Racket("Green_Sword.png", 25, 250, 30, 250, 5, 0)#Red
player2.score = 0
player1.score = 0
bomb = Ball("bomb.png", 500, 100, 100 ,100 , 4)
font.init()
style = font.SysFont(None, 60)

isDelay = False
delay_for_next_match = 2

game = True
finish = False
fps = 45
clock = time.Clock()
while game:
    window.blit(bg,(0,0))
    ball.draw()
    player1.draw()
    player2.draw()
    bomb.draw()
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    text_score = style.render(str(player1.score) + " : " +str(player2.score), 1, (26, 24, 24))
    window.blit(text_score, (600,50))

    if finish == False:
        if isDelay == False:
            ball.rotate()
            ball.update()
            bomb.rotate()
            bomb.update()
            keys_pressed = key.get_pressed()
            if keys_pressed[K_w] and player1.rect.y > 0:
                player1.rect.y -= player1.speed

            elif keys_pressed[K_s] and player1.rect.y < 450:
                player1.rect.y += player1.speed
        
            if keys_pressed[K_UP] and player2.rect.y > 0:
                player2.rect.y -= player2.speed

            elif keys_pressed[K_DOWN] and player2.rect.y < 450:
                player2.rect.y += player2.speed
        
            isCollide = sprite.collide_rect(player1, ball)
            if (isCollide == 1):
                ball.speed_x *= -1
        
            isCollide = sprite.collide_rect(player2, ball)
            if (isCollide == 1):
                ball.speed_x *= -1
            

            if ball.rect.x > window_width:
                player1.score += 1
                ball.rect.x = 600
                ball.rect.y = 50
                isDelay = True
                start_delay_time = timer.time()
            elif ball.rect.x < 0:
                player2.score += 1 
                ball.rect.x = 600
                ball.rect.y = 50
                isDelay = True
                start_delay_time = timer.time()
            if (player1.score == 5):
                finish = True
                whoWin = 1
            if (player2.score == 5):
                finish = True 
                whoWin = 2
        elif timer.time() - start_delay_time > delay_for_next_match:
            isDelay = False
    else:
        if whoWin == 1:
            whoWin = style.render("player1 wins", 1, (18, 17, 17))
            window.blit(whoWin, (560,350))
        else: 
            whoWin = style.render("player2 wins", 1, (18, 17, 17))
            window.blit(whoWin, (560,350))
           

        


        















    display.update()
    clock.tick(fps)
