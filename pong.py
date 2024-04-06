import pygame
pygame.init()
WINNING_SCORE = 1
WIDTH,HIEGHT= 1000,800
WIN = pygame.display.set_mode((WIDTH,HIEGHT))
pygame.display.set_caption("Ping Pong")
FPS = 60
BLACK=(0,0,0)
YELLOW=(0,255,255)
WHITE=(255,255,255)
PADDLE_W,PADDLE_H=30,150
BALL_RADIUS=10
RED =(255,0,0)
SCORE_FONT=pygame.font.SysFont("comicsans" , 50)
class paddle:
    COLOR = WHITE
    VEL = 10 
    def  __init__(self,x,y,width,height) :
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height=height
    def draw(self,win):
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))
    def move(self,up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class ball:
    COLOR = RED
    MAX_VEL = 5
    def __init__(self,x,y,radius):
        self.x= self.original_x = x 
        self.y= self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    def reset(self): 
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles,ball,left_score,right_score): 
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}",1,WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2,20))
    win.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2,20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(20,HIEGHT,HIEGHT//10):
        if i % 4 == 1:
                continue
        pygame.draw.rect(win,WHITE,(WIDTH//2-5,i,10,HIEGHT//20))
    ball.draw(win)
    pygame.display.update()

def handle_collosion(ball,pad1,pad2):
    if ball.y + ball.radius >= HIEGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if  ball.x_vel < 0:
        if ball.y >= pad1.y and ball.y <=pad1.y + pad1.height:
            if ball.x - ball.radius <= pad1.x +pad1.width:
                ball.x_vel*=-1

                middle_y = pad1.y + (pad1.height / 2)
                diff_y = middle_y - ball.y
                reduction_factor = (pad1.height/2)/ball.MAX_VEL 
                y_vel = diff_y / reduction_factor
                ball.y_vel= -1 * y_vel                                 



    else:
        if ball.y >= pad2.y and ball.y <=pad2.y + pad2.height:
            if ball.x+ ball.radius>= pad2.x:
                ball.x_vel*=-1

                middle_y = pad2.y + (pad2.height / 2)
                diff_y = middle_y - ball.y
                reduction_factor = (pad2.height/2)/ball.MAX_VEL 
                y_vel = diff_y / reduction_factor
                ball.y_vel= -1* y_vel   



def handle_pad_move(keys,pad1,pad2):
    #for left pad
    if keys[pygame.K_w] and  pad1.y - pad1.VEL>= 0:
        pad1.move(up=True)
    if keys[pygame.K_s] and pad1.y + pad1.height + pad1.VEL <=HIEGHT:
        pad1.move(up=False)
    #for right pad
    if keys[pygame.K_p] and  pad2.y - pad2.VEL>= 0:
        pad2.move(up=True)
    if keys[pygame.K_l] and pad2.y + pad2.height + pad2.VEL <=HIEGHT:
        pad2.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()
    pad1 = paddle(10, HIEGHT//2-PADDLE_H//2,PADDLE_W,PADDLE_H)
    pad2 = paddle(WIDTH-10-PADDLE_W, HIEGHT//2-PADDLE_H//2,PADDLE_W,PADDLE_H)
    ball1 = ball(WIDTH//2,HIEGHT//2,BALL_RADIUS)
    left_score=0
    right_score=0
    while run:
        clock.tick(FPS)
        draw(WIN,[pad1,pad2],ball1,left_score,right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_pad_move(keys,pad1,pad2)
        ball1.move()    
        handle_collosion(ball1,pad1,pad2)

        if ball1.x < 0 :
            right_score +=1
            ball1.reset()
        elif ball1.x > WIDTH:
            left_score +=1
            ball1.reset()

        won = False
        if left_score >=WINNING_SCORE:
            won = True
            wintext = "Left PLayer Won"
        elif right_score >=WINNING_SCORE:
            won = True
            wintext = "Right Player Won"
        if won:
            text = SCORE_FONT.render(wintext,1,YELLOW)
            WIN.blit(text,(WIDTH//2-text.get_width()//2 ,HIEGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball1.reset()
            pad1.reset()
            pad2.reset()
            left_score = 0
            right_score = 0 
    pygame.quit()
if __name__ == '__main__':
    main()