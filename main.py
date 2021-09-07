import pygame, sys, world
from classes import *
from random import randint
pygame.init()

"""
Handles main system processes, rendering, and input
"""

dragging = False
selected_particle = 0
cursor_size = 1
cursor_rect = pygame.Rect

def handle_input(event:pygame.event) -> None:
    global dragging
    global selected_particle
    global cursor_size
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == pygame.BUTTON_LEFT:
            dragging = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
            dragging = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
            if not selected_particle +1 >= len(particle_types):
                selected_particle += 1
            else:
                selected_particle = 0
            print(particle_types[selected_particle]['name'].upper())
        elif event.key == pygame.K_EQUALS:
            cursor_size += 1
        elif event.key == pygame.K_MINUS and cursor_size > 1:
            cursor_size -= 1
    if dragging == True:
        for x in range(cursor_rect.left,cursor_rect.left+cursor_rect.width):
           for y in range(cursor_rect.top,cursor_rect.top+cursor_rect.height):    
                world.create_particle(Particle([x//constants.CELLSIZE,y//constants.CELLSIZE],selected_particle))

def initialize() -> None:
    for x in range(constants.WIDTH//constants.CELLSIZE):
        for y in range(constants.HEIGHT//constants.CELLSIZE):
            if x % constants.CHUNKSIZE == 0 and y % constants.CHUNKSIZE == 0:
                pos = [x//constants.CHUNKSIZE,y//constants.CHUNKSIZE]
                world.chunks[str(pos)] = Chunk(pos)
    for x in range(int(constants.WIDTH/constants.CELLSIZE)):
        world.create_particle(Particle([x,int(constants.HEIGHT/constants.CELLSIZE)-1],1))
        world.create_particle(Particle([x,0],1))
    for y in range(int(constants.HEIGHT/constants.CELLSIZE)):
        world.create_particle(Particle([0,y],1))
        world.create_particle(Particle([int(constants.WIDTH/constants.CELLSIZE)-1,y],1))

def main_loop() -> None:
    global cursor_rect
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            handle_input(event)
    constants.DISPLAY.fill(constants.BACKGROUND)
    world.update()
    for c in world.chunks.values():
        pygame.draw.rect(constants.DISPLAY,(255,255,255),(c.bounds.left*constants.CELLSIZE,c.bounds.top*constants.CELLSIZE,c.bounds.width*constants.CELLSIZE,c.bounds.height*constants.CELLSIZE),1)
        if c.dirty_rect != None:
            pygame.draw.rect(constants.DISPLAY,(255,0,0),(c.dirty_rect.left*constants.CELLSIZE,c.dirty_rect.top*constants.CELLSIZE,c.dirty_rect.width*constants.CELLSIZE,c.dirty_rect.height*constants.CELLSIZE),1)
        for p in c.data.values():
            if particle_types[p.type]['density'] < 0:
                p.color = []
                for i in particle_types[p.type]['color']:
                    sign = randint(0,1)
                    if sign == 0:
                        sign = -1
                    value = i+randint(0,10)*sign
                    if value > 255:
                        value = 255
                    if value < 0:
                        value = 0
                    p.color.append(value)
            pygame.draw.rect(constants.DISPLAY,tuple(p.color),(p.pos[0]*constants.CELLSIZE,p.pos[1]*constants.CELLSIZE,constants.CELLSIZE,constants.CELLSIZE))
    cursor_rect = pygame.Rect((pygame.mouse.get_pos()[0]//constants.CELLSIZE)*constants.CELLSIZE,(pygame.mouse.get_pos()[1]//constants.CELLSIZE)*constants.CELLSIZE,constants.CELLSIZE*cursor_size,constants.CELLSIZE*cursor_size)
    pygame.draw.rect(constants.DISPLAY,(200,200,200),cursor_rect) # to add alpha this has to be a surface that is blitted to the screen
    constants.CLOCK.tick(constants.FPS)

if __name__ == '__main__':
    initialize()
    while True:
        main_loop()
