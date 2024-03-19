import pygame
from sys import exit
import numpy as np
    
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'image/curve_pattern.png'

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")
  
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = [] 
knots = []
pos1 =[20,height-30]
pos2 =[width-20,height-30]
dis = 10
count = 0
myfont = pygame.font.Font(None, 30)
myfont2 = pygame.font.Font(None, 15)

screen.fill(WHITE)

clock= pygame.time.Clock()

def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, color, pt, thick)

def drawLine(pt0, pt1, color='GREEN', thick=3):
    drawPoint((100,100), color,  thick)
    drawPoint(pt0, color, thick)
    drawPoint(pt1, color, thick)

def drawPolylines(color='GREEN', thick=3):
    if(count < 2): return
    for i in range(count-1):
        for j in range(dis):
            pox1 = pts[i][0]+(pts[i+1][0]-pts[i][0])/dis*j
            poy1 = (pts[i+1][1]-pts[i][1])/(pts[i+1][0]-pts[i][0])*(pox1-pts[i][0])+pts[i][1]
            poc1 = [pox1,poy1]
            pox2 = pts[i][0]+(pts[i+1][0]-pts[i][0])/dis*(j+1)
            poy2 = (pts[i+1][1]-pts[i][1])/(pts[i+1][0]-pts[i][0])*(pox2-pts[i][0])+pts[i][1]
            poc2 = [pox2,poy2]
            pygame.draw.line(screen, color,poc1,poc2, thick)

def AnimationFunction(a,color='Red', thick=5):
    
    for i in range(count-1):
        x = pts[i][0]*(1-a) +pts[i+1][0]*a
        y = pts[i][1]*(1-a) +pts[i+1][1]*a
        pos = [x,y]
        drawPoint(pos, color, thick)
        xs =  format(x, '.1f')
        ys =  format(y, '.1f')
        textImage = myfont2.render("("+xs+","+ys+")", True, color)
        screen.blit(textImage, (x-30, y-20))

done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0
Aim = False
a=0
AimSpeed = 5

while not done:   
    time_passed = clock.tick(60)
    time_passed_seconds = time_passed/10000.0
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if Aim:
                Aim = False
            else:
                a=0
                Aim = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :
        pts.append(pt) 
        count += 1
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed)+" add pts ...")
    else:
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed))

    for i in range(count):
        pygame.draw.rect(screen, BLUE, (pts[i][0]-margin, pts[i][1]-margin, 2*margin, 2*margin), 5)
        x = format(pts[i][0], '.1f')
        y = format(pts[i][1], '.1f')
        textImage = myfont2.render("("+x+","+y+")", True, BLACK)
        screen.blit(textImage, (pts[i][0]-30, pts[i][1]-20))

    if len(pts)>1:
        drawPolylines(GREEN, 1)
    
    if Aim:
        AnimationFunction(a)
        a = a + time_passed_seconds*AimSpeed
        if a >= 1:
            a = 0
            Aim = False
    elif a!=0:
        AnimationFunction(a)

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()

