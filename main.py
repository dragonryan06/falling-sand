import pygame, sys
from classes import *
from random import randint
pygame.init()

grid = {} # format: {cell:obj, cell2:obj2}
dragging = False
selected_particle = 0
cursor_size = 1
cursor_rect = pygame.Rect

def create_particle(particle): # creates a grid entry for the new particle
    grid[str(particle.pos)] = particle
    if particle_types[particle.type]['move_type'] != 'static':
        particle.active = True

def move_particle(particle): # i believe its possible particles could move twice if they were displaced by another particle falling and then they moved, this probably can be fixed with a "moved" bool property that says if the particle moved that frame already
    moved = False
    direction = randint(0,1)
    if direction == 0:
        direction = -1
    neighbors = { # left/right is relative to which dir was picked to go first by the randint
        'down' : [particle.pos[0],particle.pos[1]+1],
        'downdiagonal1' : [particle.pos[0]+direction,particle.pos[1]+1],
        'downdiagonal2' : [particle.pos[0]-direction,particle.pos[1]+1],
        'side1' : [particle.pos[0]+direction,particle.pos[1]],
        'side2' : [particle.pos[0]-direction,particle.pos[1]],
        'up' : [particle.pos[0],particle.pos[1]-1],
        'updiagonal1' : [particle.pos[0]+direction,particle.pos[1]-1],
        'updiagonal2' : [particle.pos[0]-direction,particle.pos[1]-1]}

    if not str(neighbors['down']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['down'])] = particle
        particle.pos = neighbors['down']
        moved = True
    elif str(neighbors['down']) in grid.keys() and particle_types[grid[str(neighbors['down'])].type]['density'] < particle_types[particle.type]['density']:
        del grid[str(particle.pos)]
        replacing_particle = grid[str(neighbors['down'])]
        del grid[str(neighbors['down'])]
        grid[str(particle.pos)] = replacing_particle
        grid[str(neighbors['down'])] = particle
        replacing_particle.pos = particle.pos
        particle.pos = neighbors['down']
        moved = True

    elif not str(neighbors['downdiagonal1']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['downdiagonal1'])] = particle
        particle.pos = neighbors['downdiagonal1']
        moved = True
    elif str(neighbors['downdiagonal1']) in grid.keys() and particle_types[grid[str(neighbors['downdiagonal1'])].type]['density'] < particle_types[particle.type]['density']:
        del grid[str(particle.pos)]
        replacing_particle = grid[str(neighbors['downdiagonal1'])]
        del grid[str(neighbors['downdiagonal1'])]
        grid[str(particle.pos)] = replacing_particle
        grid[str(neighbors['downdiagonal1'])] = particle
        replacing_particle.pos = particle.pos
        particle.pos = neighbors['downdiagonal1']
        moved = True

    elif not str(neighbors['downdiagonal2']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['downdiagonal2'])] = particle
        particle.pos = neighbors['downdiagonal2']
        moved = True
    elif str(neighbors['downdiagonal2']) in grid.keys() and particle_types[grid[str(neighbors['downdiagonal2'])].type]['density'] < particle_types[particle.type]['density']:
        del grid[str(particle.pos)]
        replacing_particle = grid[str(neighbors['downdiagonal2'])]
        del grid[str(neighbors['downdiagonal2'])]
        grid[str(particle.pos)] = replacing_particle
        grid[str(neighbors['downdiagonal2'])] = particle
        replacing_particle.pos = particle.pos
        particle.pos = neighbors['downdiagonal2']
        moved = True

    # there is no need for having things bubble up as the substance the are in will push them up
    elif not str(neighbors['up']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['up'])] = particle
        particle.pos = neighbors['up']
        moved = True
    
    elif not str(neighbors['updiagonal1']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['updiagonal1'])] = particle
        particle.pos = neighbors['updiagonal1']
        moved = True
    
    elif not str(neighbors['updiagonal2']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        del grid[str(particle.pos)]
        grid[str(neighbors['updiagonal2'])] = particle
        particle.pos = neighbors['updiagonal2']
        moved = True

    elif particle_types[particle.type]['move_type'] == 'fluid':
        if not str(neighbors['side1']) in grid.keys():
            del grid[str(particle.pos)]
            grid[str(neighbors['side1'])] = particle
            particle.pos = neighbors['side1']
            moved = True
        elif str(neighbors['side1']) in grid.keys() and particle_types[grid[str(neighbors['side1'])].type]['density'] < particle_types[particle.type]['density']:
            del grid[str(particle.pos)]
            replacing_particle = grid[str(neighbors['side1'])]
            del grid[str(neighbors['side1'])]
            grid[str(particle.pos)] = replacing_particle
            grid[str(neighbors['side1'])] = particle
            replacing_particle.pos = particle.pos
            particle.pos = neighbors['side1']
            moved = True

        elif not str(neighbors['side2']) in grid.keys():
            del grid[str(particle.pos)]
            grid[str(neighbors['side2'])] = particle
            particle.pos = neighbors['side2']
            moved = True
        elif str(neighbors['side2']) in grid.keys() and particle_types[grid[str(neighbors['side2'])].type]['density'] < particle_types[particle.type]['density']:
            del grid[str(particle.pos)]
            replacing_particle = grid[str(neighbors['side2'])]
            del grid[str(neighbors['side2'])]
            grid[str(particle.pos)] = replacing_particle
            grid[str(neighbors['side2'])] = particle
            replacing_particle.pos = particle.pos 
            particle.pos = neighbors['side2']
            moved = True
    return moved, neighbors

def update_world():
    particles = list(grid.values())
    for p in particles:
        if p.active:
            moved, neighbors = move_particle(p)
            if moved == False:
                p.active = False
            else:
                for n in neighbors.values():
                    if str(n) in grid.keys():
                        if particle_types[grid[str(n)].type]['move_type'] != 'static':
                            grid[str(n)].active = True
            
        pygame.draw.rect(constants.DISPLAY,particle_types[p.type]['color'],(p.pos[0]*constants.CELLSIZE,p.pos[1]*constants.CELLSIZE,constants.CELLSIZE,constants.CELLSIZE))

def handle_input(event):
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
                create_particle(Particle([x//constants.CELLSIZE,y//constants.CELLSIZE],selected_particle))

def initialize():
    for x in range(int(constants.WIDTH/constants.CELLSIZE)):
        create_particle(Particle([x,int(constants.HEIGHT/constants.CELLSIZE)-1],1))
        create_particle(Particle([x,0],1))
    for y in range(int(constants.HEIGHT/constants.CELLSIZE)):
        create_particle(Particle([0,y],1))
        create_particle(Particle([int(constants.WIDTH/constants.CELLSIZE)-1,y],1))
    create_particle(Particle([5,1],0))

def main_loop():
    global cursor_rect
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            handle_input(event)
    constants.DISPLAY.fill(constants.BACKGROUND)
    update_world()
    cursor_rect = pygame.Rect((pygame.mouse.get_pos()[0]//constants.CELLSIZE)*constants.CELLSIZE,(pygame.mouse.get_pos()[1]//constants.CELLSIZE)*constants.CELLSIZE,constants.CELLSIZE*cursor_size,constants.CELLSIZE*cursor_size)
    pygame.draw.rect(constants.DISPLAY,(200,200,200),cursor_rect) # to add alpha this has to be a surface that is blitted to the screen
    constants.CLOCK.tick(constants.FPS)

if __name__ == '__main__':
    initialize()
    while True:
        main_loop()
