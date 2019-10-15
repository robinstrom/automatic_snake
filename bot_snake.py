import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    width = 500

    def __init__(self, start, direction_x=1, direction_y=0, color=(255, 0, 0)):
        self.position = start
        self.direction_x = 1
        self.direction_y = 0
        self.color = color

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface):
        dis = self.width // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))


class snake(object):
    body = []
    turns = {}
    def __init__(self, color, position):
        self.color = color
        self.head = cube(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            
            def turn_left():
                self.direction_x = -1
                self.direction_y = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            def turn_right():
                self.direction_x = 1
                self.direction_y = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            def turn_up():
                self.direction_x = 0
                self.direction_y = -1
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            def turn_down():
                self.direction_x = 0
                self.direction_y = 1
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
            
            keys = pygame.key.get_pressed()

            for key in keys:      
                if keys[pygame.K_LEFT]:
                    turn_left()
                elif keys[pygame.K_RIGHT]:
                    turn_right()
                elif keys[pygame.K_UP]:
                    turn_up()
                elif keys[pygame.K_DOWN]:
                    turn_down()

        for i, body_cube in enumerate(self.body):
            cube_position = body_cube.position[:]
            if cube_position in self.turns:
                turn = self.turns[cube_position]
                body_cube.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(cube_position)
            else:
                if body_cube.direction_x == -1 and body_cube.position[0] <= 0: 
                    body_cube.position = (body_cube.rows-1, body_cube.position[1])
                elif body_cube.direction_x == 1 and body_cube.position[0] >= body_cube.rows-1: 
                    body_cube.position = (0, body_cube.position[1])
                elif body_cube.direction_y == 1 and body_cube.position[1] >= body_cube.rows-1: 
                    body_cube.position = (body_cube.position[0], 0) 
                elif body_cube.direction_y == -1 and body_cube.position[1] <= 0: 
                    body_cube.position = (body_cube.position[0], body_cube.rows-1)
                else: 
                    body_cube.move(body_cube.direction_x, body_cube.direction_y)


    def reset(self, position):
        self.head = cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.position[0]-1, tail.position[1])))
        
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.position[0]+1, tail.position[1])))
        
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.position[0], tail.position[1]-1)))
        
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.position[0], tail.position[1]+1)))

        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy


        
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.position == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
    
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].position == snack.position:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].position in list(map(lambda z:z.position, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You lost!\n Score: ' + len(s.body) + '\n', 'Play again?')
                s.reset((10, 10))
                break


        redrawWindow(win)

main()

