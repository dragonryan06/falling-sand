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

def move_particle(particle): # i believe its possible particles could move twice if they were displaced by another particle falling and then they moved, this probably can be fixed with a "moved" bool
    neighbors = {
        'down' : [particle.pos[0],particle.pos[1]+1],
        'downright' : [particle.pos[0]+1,particle.pos[1]+1],
        'downleft' : [particle.pos[0]-1,particle.pos[1]+1],
        'right' : [particle.pos[0]+1,particle.pos[1]],
        'left' : [particle.pos[0]-1,particle.pos[1]],
        'up' : [particle.pos[0],particle.pos[1]-1],
        'upright' : [particle.pos[0]+1,particle.pos[1]-1],
        'upleft' : [particle.pos[0]-1,particle.pos[1]-1]}

    if not str(neighbors['down']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['down'])] = particle
        particle.pos = neighbors['down']
    elif str(neighbors['down']) in grid.keys() and particle_types[grid[str(neighbors['down'])].type]['density'] < particle_types[particle.type]['density']:
        del grid[str(particle.pos)]
        replacing_particle = grid[str(neighbors['down'])]
        del grid[str(neighbors['down'])]
        grid[str(particle.pos)] = replacing_particle
        grid[str(neighbors['down'])] = particle
        replacing_particle.pos = particle.pos
        particle.pos = neighbors['down']

    elif not str(neighbors['downright']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['downright'])] = particle
        particle.pos = neighbors['downright']
    elif str(neighbors['downright']) in grid.keys() and particle_types[grid[str(neighbors['downright'])].type]['density'] < particle_types[particle.type]['density']:
        del grid[str(particle.pos)]
        replacing_particle = grid[str(neighbors['downright'])]
        del grid[str(neighbors['downright'])]
        grid[str(particle.pos)] = replacing_particle
        grid[str(neighbors['downright'])] = particle
        replacing_particle.pos = particle.pos
        particle.pos = neighbors['downright']

    elif not str(neighbors['downleft']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['downleft'])] = particle
        particle.pos = neighbors['downleft']
    elif str(neighbors['downleft']) in grid.keys() and particle_types[grid[str(neighbors['downleft'])].type]['density'] < particle_types[particle.type]['density']:
        del grid[str(particle.pos)]
        replacing_particle = grid[str(neighbors['downleft'])]
        del grid[str(neighbors['downleft'])]
        grid[str(particle.pos)] = replacing_particle
        grid[str(neighbors['downleft'])] = particle
        replacing_particle.pos = particle.pos
        particle.pos = neighbors['downleft']

    # there is no need for having things bubble up as the substance the are in will push them up
    elif not str(neighbors['up']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['up'])] = particle
        particle.pos = neighbors['up']
    
    elif not str(neighbors['upright']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['upright'])] = particle
        particle.pos = neighbors['upright']
    
    elif not str(neighbors['upleft']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['upleft'])] = particle
        particle.pos = neighbors['upleft']

    elif particle_types[particle.type]['move_type'] == 'fluid':
        if not str(neighbors['right']) in grid.keys():
            del grid[str(particle.pos)]
            grid[str(neighbors['right'])] = particle
            particle.pos = neighbors['right']
        elif str(neighbors['right']) in grid.keys() and particle_types[grid[str(neighbors['right'])].type]['density'] < particle_types[particle.type]['density']:
            del grid[str(particle.pos)]
            replacing_particle = grid[str(neighbors['right'])]
            del grid[str(neighbors['right'])]
            grid[str(particle.pos)] = replacing_particle
            grid[str(neighbors['right'])] = particle
            replacing_particle.pos = particle.pos
            particle.pos = neighbors['right']

        elif not str(neighbors['left']) in grid.keys():
            del grid[str(particle.pos)]
            grid[str(neighbors['left'])] = particle
            particle.pos = neighbors['left']
        elif str(neighbors['left']) in grid.keys() and particle_types[grid[str(neighbors['left'])].type]['density'] < particle_types[particle.type]['density']:
            del grid[str(particle.pos)]
            replacing_particle = grid[str(neighbors['left'])]
            del grid[str(neighbors['left'])]
            grid[str(particle.pos)] = replacing_particle
            grid[str(neighbors['left'])] = particle
            replacing_particle.pos = particle.pos 
            particle.pos = neighbors['left']

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
