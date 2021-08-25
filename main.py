import pygame, sys
from classes import *
pygame.init()

grid = {} # format: {cell:obj, cell2:obj2}
dragging = False
selected_particle = 0

def create_particle(particle): # creates a grid entry for the new particle
    grid[str(particle.pos)] = particle
    if particle_types[particle.type]['move_type'] != 'static':
        particle.active = True

def move_particle(particle):
    down = [particle.pos[0],particle.pos[1]+1]
    downright = [particle.pos[0]+1,particle.pos[1]+1]
    downleft = [particle.pos[0]-1,particle.pos[1]+1]
    right = [particle.pos[0]+1,particle.pos[1]]
    left = [particle.pos[0]-1,particle.pos[1]]
    if not str(down) in grid.keys():
        del grid[str(particle.pos)]
        grid[str(down)] = particle
        particle.pos = down
    elif not str(downright) in grid.keys():
        del grid[str(particle.pos)]
        grid[str(downright)] = particle
        particle.pos = downright
    elif not str(downleft) in grid.keys():
        del grid[str(particle.pos)]
        grid[str(downleft)] = particle
        particle.pos = downleft
    elif particle_types[particle.type]['move_type'] == 'fluid':
        if not str(right) in grid.keys():
            del grid[str(particle.pos)]
            grid[str(right)] = particle
            particle.pos = right
        elif not str(left) in grid.keys():
            del grid[str(particle.pos)]
            grid[str(left)] = particle
            particle.pos = left

def update_world():
    particles = list(grid.values())
    for p in particles:
        if p.active:
            move_particle(p)
        pygame.draw.rect(constants.DISPLAY,particle_types[p.type]['color'],(p.pos[0]*constants.CELLSIZE,p.pos[1]*constants.CELLSIZE,constants.CELLSIZE,constants.CELLSIZE))

def handle_input(event):
    global dragging
    global selected_particle
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
    if dragging == True:
        create_particle(Particle([round(pygame.mouse.get_pos()[0]/constants.CELLSIZE),round(pygame.mouse.get_pos()[1]/constants.CELLSIZE)],selected_particle))

def initialize():
    for x in range(int(constants.WIDTH/constants.CELLSIZE)):
        create_particle(Particle([x,int(constants.HEIGHT/constants.CELLSIZE)-1],1))
        create_particle(Particle([x,0],1))
    for y in range(int(constants.HEIGHT/constants.CELLSIZE)):
        create_particle(Particle([0,y],1))
        create_particle(Particle([int(constants.WIDTH/constants.CELLSIZE)-1,y],1))
    create_particle(Particle([5,1],0))

def main_loop():
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            handle_input(event)
    constants.DISPLAY.fill(constants.BACKGROUND)
    update_world()
    constants.CLOCK.tick(constants.FPS)

if __name__ == '__main__':
    initialize()
    while True:
        main_loop()
