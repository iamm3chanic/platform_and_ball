import pygame
pygame.init()

#выбор уровня сложности
level = input('Выберите уровень сложности (1/2/3):')
while level != "1" and level != "2" and level != "3":
    print("Неверный ввод!")
    level = input('Выберите уровень сложности (1/2/3):')
level = int(level)
if level == 1:
    plat_v = 5
    ball_v = 3
elif level == 2:
    plat_v = 4
    ball_v = 4 
elif level == 3:
    plat_v = 3
    ball_v = 4

back = (200,255,255)
bg = pygame.image.load("nebo.png")
bg = pygame.transform.scale(bg, (500,400))

mw = pygame.display.set_mode((500, 400)) #окно программы (main window)
mw.blit(bg,(0,0))
clock = pygame.time.Clock()
 
#переменные, отвечающие за координаты платформы
racket_x = 200
racket_y = 330
move_right = False
move_left = False 
#переменные, отвечающие за скорость мяча
dx = ball_v
dy = ball_v
#флаг окончания игры
game_over = False
#класс из предыдущего проекта
class Area():
   def __init__(self, x=0, y=0, width=10, height=10, color=None):
       self.rect = pygame.Rect(x, y, width, height)
       self.fill_color = back
       if color:
           self.fill_color = color
   def color(self, new_color):
       self.fill_color = new_color
   def fill(self):
       pygame.draw.rect(mw, self.fill_color, self.rect)
 
   def collidepoint(self, x, y):
       return self.rect.collidepoint(x, y)
   def colliderect(self, rect):
       return self.rect.colliderect(rect)
 
#класс для объектов-надписей
class Label(Area):
   def set_text(self, text, fsize=12, t_color=(0,0,0)):
       self.image = pygame.font.SysFont('verdana',fsize).render(text, True, t_color)
   def draw(self, shift_x, shift_y):
       self.fill()
       mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

#класс для объектов-картинок
class Picture(Area):
   def __init__(self, filename, x=0, y=0, width=10, height=10):
       Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
       self.image = pygame.image.load(filename)
       self.width=width
       self.height=height
   def draw(self):
       mw.blit(self.image, (self.rect.x, self.rect.y))
   def fill_back(self, filename):
       self.imageback = pygame.image.load(filename)
       self.imageback = pygame.transform.scale(self.imageback, (self.width,self.height))
       mw.blit(self.imageback, (self.rect.x, self.rect.y))
   def resize(self, w, h):
       self.image = pygame.transform.scale(self.image, (w,h))
       

ball = Picture('ball.png', 160, 200, 50, 50)
ball.resize(50,50)
platform = Picture('platform.png', racket_x, racket_y, 100, 30)
platform.resize(100,30)

#создание списка монстров
start_x = 5
start_y = 5
count = 9
monsters = []
for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        m = Picture('brick.png',x,y,50,50)
        m.resize(50,50)
        monsters.append(m)
        x += 55
    count -= 1

while game_over != True:
    mw.blit(bg,(0,0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_over = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                game_over = True
            if e.key == pygame.K_a:
                move_left = True
            if e.key == pygame.K_d:
                move_right = True
            if e.key == pygame.K_LEFT:
                move_left = True
            if e.key == pygame.K_RIGHT:
                move_right = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                move_left = False
            if e.key == pygame.K_RIGHT:
                move_right = False
            if e.key == pygame.K_a:
                move_left = False
            if e.key == pygame.K_d:
                move_right = False

    if move_right:
        platform.rect.x += plat_v
    if move_left:
        platform.rect.x -= plat_v
    
    ball.rect.x += dx
    ball.rect.y += dy
    if  ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    #если мяч коснулся ракетки, меняем направление движения
    if ball.rect.colliderect(platform.rect):
        dy *= -1
    if ball.rect.y > racket_y+20:
        txt = Label(125,170,250,60,(0,0,0))
        txt.set_text('YOU LOSE...',40, (255,0,0))
        txt.draw(10,10)
        game_over = True
    if len(monsters)==0:
        txt = Label(125,170,250,60,(0,0,0))
        txt.set_text('YOU WIN!!!',40, (0,200,0))
        txt.draw(10,10)
        game_over = True
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill_back("win.png") #вместо fill
            dy *= -1
    if platform.rect.x < 0:
        platform.rect.x = 0
    if platform.rect.x > 400:
        platform.rect.x = 400

    ball.draw()
    platform.draw()
    pygame.display.update()
    clock.tick(40)
