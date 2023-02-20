import pygame, sys, random
from pygame.locals import *
import csv

pygame.init()
clock = pygame.time.Clock() 

global value 
global x_cord
global y_cord
global num
global var_i_val
global var_j_val
global global_time 
global_time = 0
value = 0
x = 0
y = 0
dif = 1000/10
var_i_val = 1
var_j_val = -1



# predefined colours
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (92, 181, 87)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (252, 194, 3)
GRAY = (186, 185, 181)


font1 = pygame.font.SysFont(None,40)
font2 = pygame.font.SysFont(None,20)
screen = pygame.display.set_mode((1000,800))
screen.fill(WHITE)

pygame.display.set_caption("Wordle")
img = pygame.image.load("assets/Icon.png")
pygame.display.set_icon(img)

filename="words.csv"

with open('words.csv', mode='r') as infile:
    reader = csv.reader(infile)
    guessWord = {int(rows[0]):rows[1] for rows in reader}
    

num = random.randint(1,140)
print(guessWord[num])

grid = [
    [guessWord[num][0],guessWord[num][0],guessWord[num][0],guessWord[num][0],guessWord[num][0],guessWord[num][0]],
    [guessWord[num][1],guessWord[num][1],guessWord[num][1],guessWord[num][1],guessWord[num][1],guessWord[num][1]],
    [guessWord[num][2],guessWord[num][2],guessWord[num][2],guessWord[num][2],guessWord[num][2],guessWord[num][2]],
    [guessWord[num][3],guessWord[num][3],guessWord[num][3],guessWord[num][3],guessWord[num][3],guessWord[num][3]],
    [guessWord[num][4],guessWord[num][4],guessWord[num][4],guessWord[num][4],guessWord[num][4],guessWord[num][4]],
    [guessWord[num][5],guessWord[num][5],guessWord[num][5],guessWord[num][5],guessWord[num][5],guessWord[num][5]]
]

w, h = 6, 6
grid_data = [['' for x in range(w)] for y in range(h)] 
grid_color = [[0 for x in range(w)] for y in range(h)]

class pop_up:
    def __init__(self,image_game, i_size_x, i_size_y, i_pos_x, i_pos_y):
        self.image_game = image_game
        self.i_size_x = i_size_x
        self.i_size_y = i_size_y
        self.i_pos_x = i_pos_x
        self.i_pos_y = i_pos_y

    def draw_popup(self):

        # Load image
        self.image_wel = pygame.image.load(self.image_game)
            
        # Set the size for the image
        self.DEFAULT_IMAGE_SIZE = (self.i_size_x, self.i_size_y)

        # Set a default position
        self.DEFAULT_IMAGE_POSITION = (self.i_pos_x, self.i_pos_y)
            
        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image_wel, self.DEFAULT_IMAGE_SIZE)
        screen.blit(self.image, self.DEFAULT_IMAGE_POSITION)

def draw_box():
    for i in range(2):
        pygame.draw.line(screen, BLACK, (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 4)
        pygame.draw.line(screen, BLACK, ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 4)  

def draw():
    for i in range(2,8):
        for j in range(var_j_val+3,8):
            pygame.draw.rect(screen,(0, 153, 153),(i*dif,j*dif,dif+1,dif+1))

            text1 = font1.render(str(grid_data[i-2][j-2]),1,RED)
            screen.blit(text1,((i)*dif+35 , (j)*dif+20))

    for i in range(2,9):
        thick = 2
        pygame.draw.line(screen,BLACK,(200,i*dif),(800,i*dif),thick)
        pygame.draw.line(screen,BLACK,(i*dif,200),(i*dif,800),thick)
    
        
def get_cord(pos):
    global x
    global y
    y = pos[1]//dif 
    x = pos[0]//dif

def draw_val(data):
    x_cord = int(x)
    y_cord = int(y)

    grid_data[x_cord-2][y_cord-2] = data
    
    text1 = font1.render(str(grid_data[x_cord-2][y_cord-2]),1,RED)
    screen.blit(text1,(x*dif+35 , y*dif+20))

def event_reset():
    pygame.event.clear(eventtype= pygame.KEYDOWN)

def validate():
    for i in range(2,8):
        for j in range(var_i_val,8):
            if grid_color[i-2][j-2] == 1:
                pygame.draw.rect(screen,GREEN,(i*dif,j*dif,dif+1,dif+1))
                text1 = font1.render(str(grid_data[i-2][j-2]),1,RED)
                screen.blit(text1,((i)*dif+35 , (j)*dif+20))
            elif grid_color[i-2][j-2] == 2:
                pygame.draw.rect(screen,ORANGE,(i*dif,j*dif,dif+1,dif+1))
                text1 = font1.render(str(grid_data[i-2][j-2]),1,RED)
                screen.blit(text1,((i)*dif+35 , (j)*dif+20))
            elif grid_color[i-2][j-2] == 3:
                pygame.draw.rect(screen,GRAY,(i*dif,j*dif,dif+1,dif+1))
                text1 = font1.render(str(grid_data[i-2][j-2]),1,RED)
                screen.blit(text1,((i)*dif+35 , (j)*dif+20))
    for i in range(2,9):
        thick = 2
        pygame.draw.line(screen,BLACK,(200,i*dif),(800,i*dif),thick)
        pygame.draw.line(screen,BLACK,(i*dif,200),(i*dif,800),thick)

timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event,1000)

heading = pop_up('wordle_edit.png',700,120,140,0)
heading.draw_popup()

intro_msg = pop_up('welcome_msg.png', 250, 100, 375,400)

ques_mark_img = pop_up('question_mark.png',50, 50,930,195)
ques_mark_img.draw_popup()

info_img = pop_up('Instruction2.png', 450, 95, 280,702)
close_img =  pop_up('close.png', 36, 36, 695,701)

won_img = pop_up('won.png', 300, 200, 350,350)

run = True
flag1 = 0
flag2 = 0
t_flag = 0
won_flag = False

while run:    
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False 
        if event.type == timer_event:
            if t_flag == 0:
                intro_msg.draw_popup()
                t_flag += 1
            elif not(won_flag):
                draw()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            get_cord(pos)
            print(x_cord,' and ',y_cord)
            flag1 = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_a:
                value = 'A'
            if event.key == pygame.K_b:
                value = 'B'
            if event.key == pygame.K_c:
                value = 'C'
            if event.key == pygame.K_d:
                value = 'D'
            if event.key == pygame.K_e:
                value = 'E'
            if event.key == pygame.K_f:
                value = 'F'
            if event.key == pygame.K_g:
                value = 'G'
            if event.key == pygame.K_h:
                value = 'H'
            if event.key == pygame.K_i:
                value = 'I'
            if event.key == pygame.K_j:
                value = 'J'
            if event.key == pygame.K_k:
                value = 'K'
            if event.key == pygame.K_l:
                value = 'L'
            if event.key == pygame.K_m:
                value = 'M'
            if event.key == pygame.K_n:
                value = 'N'
            if event.key == pygame.K_o:
                value = 'O'
            if event.key == pygame.K_p:
                value = 'P'
            if event.key == pygame.K_q:
                value = 'Q'
            if event.key == pygame.K_r:
                value = 'R'
            if event.key == pygame.K_s:
                value = 'S'
            if event.key == pygame.K_t:
                value = 'T'
            if event.key == pygame.K_u:
                value = 'U'
            if event.key == pygame.K_v:
                value = 'V'
            if event.key == pygame.K_w:
                value = 'W'
            if event.key == pygame.K_x:
                value = 'X'
            if event.key == pygame.K_y:
                value = 'Y'
            if event.key == pygame.K_z:
                value = 'Z'
            if event.key == pygame.K_BACKSPACE:
                value = ''
            if event.key==pygame.K_RETURN:
                if x_cord == 7:
                    flag2 = 1
                    var_i_val+=1
                    var_j_val+=1
            
    x_cord = int(x)
    y_cord = int(y)

    if x == 9 and y == 2:
        info_img.draw_popup()
        close_img.draw_popup()

    if (x_cord >=2 and x_cord <=7) and ((y_cord >=2 and y_cord <=7)):
        # print(x_cord,' and ',y_cord)
        if flag1 == 1 and not(won_flag):
            draw_box()
        if value != 0:
            if (y_cord-2) >= var_j_val+1:
                draw_val(value)
                grid_data[x_cord-2][y_cord-2] = value
                flag1 = 0
                value = 0

    if flag2 == 1:
        for j in range(0,6):
            x_val = var_j_val
            if (guessWord[num].lower()).__contains__(grid_data[j][x_val].lower()):
                if grid[j][x_val].lower() == grid_data[j][x_val].lower() and grid_data[j][x_val] !=  '':
                    grid_color[j][x_val] = 1
                elif grid[j][x_val].lower() != grid_data[j][x_val].lower() and grid_data[j][x_val] !=  '':
                    grid_color[j][x_val] = 2 
            else:
                grid_color[j][x_val] = 3   
                       
            validate()

        for i in range(0,6):
            count = 0
            for j in range(0,6):
                if grid_color[j][i] == 1:
                    count += 1
            if count == 6:
                won_img.draw_popup()
                won_flag = True
                break
            
    if x_cord != 7:
        flag2 = 0

    pygame.display.update()

pygame.quit()