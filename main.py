import pygame, sys
from classes import *
from random import randint
pygame.init()

grid = {} # format: {cell:obj, cell2:obj2}
dragging = False
selected_particle = 0
cursor_size = 1
cursor_rect = pygame.Rect

def create_particle(particle:Particle) -> None:
    # creates a grid entry for the new particle
    grid[str(particle.pos)] = particle
    if particle_types[particle.type]['move_type'] != 'static':
        particle.active = True

def set_cell(particle:Particle,pos:list) -> None:
    grid[str(pos)] = particle
    particle.pos = pos
    neighbors = [[particle.pos[0],particle.pos[1]+1],[particle.pos[0]+1,particle.pos[1]+1],[particle.pos[0]-1,particle.pos[1]+1],[particle.pos[0]+1,particle.pos[1]],[particle.pos[0]-1,particle.pos[1]],[particle.pos[0],particle.pos[1]-1],[particle.pos[0]+1,particle.pos[1]-1],[particle.pos[0]-1,particle.pos[1]-1]]
    if particle_types[particle.type]['move_type'] != 'static':
        particle.active = True
    for n in neighbors:
        if str(n) in grid.keys():
            if particle_types[grid[str(n)].type]['move_type'] != 'static':
                grid[str(n)].active = True

def clear_cell(particle:Particle,pos:list) -> None:
    neighbors = [[particle.pos[0],particle.pos[1]+1],[particle.pos[0]+1,particle.pos[1]+1],[particle.pos[0]-1,particle.pos[1]+1],[particle.pos[0]+1,particle.pos[1]],[particle.pos[0]-1,particle.pos[1]],[particle.pos[0],particle.pos[1]-1],[particle.pos[0]+1,particle.pos[1]-1],[particle.pos[0]-1,particle.pos[1]-1]]
    for n in neighbors:
        if str(n) in grid.keys():
            if particle_types[grid[str(n)].type]['move_type'] != 'static':
                grid[str(n)].active = True
    del grid[str(pos)]


def move_particle(particle:Particle) -> dict: # i believe its possible particles could move twice if they were displaced by another particle falling and then they moved, this probably can be fixed with a "moved" bool property that says if the particle moved that frame already
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
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['down'])
    elif str(neighbors['down']) in grid.keys() and particle_types[grid[str(neighbors['down'])].type]['density'] < particle_types[particle.type]['density']:
        clear_cell(particle,particle.pos)
        replacing_particle = grid[str(neighbors['down'])]
        clear_cell(grid[str(neighbors['down'])],neighbors['down'])
        set_cell(replacing_particle,particle.pos)
        set_cell(particle,neighbors['down'])

    elif not str(neighbors['downdiagonal1']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal1'])
    elif str(neighbors['downdiagonal1']) in grid.keys() and particle_types[grid[str(neighbors['downdiagonal1'])].type]['density'] < particle_types[particle.type]['density']:
        clear_cell(particle,particle.pos)
        replacing_particle = grid[str(neighbors['downdiagonal1'])]
        clear_cell(grid[str(neighbors['downdiagonal1'])],neighbors['downdiagonal1'])
        set_cell(replacing_particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal1'])

    elif not str(neighbors['downdiagonal2']) in grid.keys() and particle_types[particle.type]['density'] > 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal2'])
    elif str(neighbors['downdiagonal2']) in grid.keys() and particle_types[grid[str(neighbors['downdiagonal2'])].type]['density'] < particle_types[particle.type]['density']:
        clear_cell(particle,particle.pos)
        replacing_particle = grid[str(neighbors['downdiagonal2'])]
        clear_cell(grid[str(neighbors['downdiagonal2'])],neighbors['downdiagonal2'])
        set_cell(replacing_particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal2'])

    # there is no need for having things bubble up as the substance the are in will push them up
    elif not str(neighbors['up']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['up'])
    
    elif not str(neighbors['updiagonal1']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['updiagonal1'])
    
    elif not str(neighbors['updiagonal2']) in grid.keys() and particle_types[particle.type]['density'] < 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['updiagonal2'])

    elif particle_types[particle.type]['move_type'] == 'fluid':
        if not str(neighbors['side1']) in grid.keys():
            clear_cell(particle,particle.pos)
            set_cell(particle,neighbors['side1'])
        elif str(neighbors['side1']) in grid.keys() and particle_types[grid[str(neighbors['side1'])].type]['density'] < particle_types[particle.type]['density']:
            clear_cell(particle,particle.pos)
            replacing_particle = grid[str(neighbors['side1'])]
            clear_cell(grid[str(neighbors['side1'])],neighbors['side1'])
            set_cell(replacing_particle,particle.pos)
            set_cell(particle,neighbors['side1'])

        elif not str(neighbors['side2']) in grid.keys():
            clear_cell(particle,particle.pos)
            set_cell(particle,neighbors['side2'])
        elif str(neighbors['side2']) in grid.keys() and particle_types[grid[str(neighbors['side2'])].type]['density'] < particle_types[particle.type]['density']:
            clear_cell(particle,particle.pos)
            replacing_particle = grid[str(neighbors['side2'])]
            clear_cell(grid[str(neighbors['side2'])],neighbors['side2'])
            set_cell(replacing_particle,particle.pos)
            set_cell(particle,neighbors['side2'])
    return neighbors

def reaction_check(p:Particle,neighbors:dict) -> None:
    if len(particle_types[p.type]['reactions']) > 0:
        for r in particle_types[p.type]['reactions']:
            for i in reactions[r]['reactants']:
                if p.type in i:
                    for n in neighbors.values():
                        if str(n) in grid.keys() and p.type == grid[str(n)].type:
                            continue
                        elif str(n) in grid.keys() and grid[str(n)].type in i:
                            if randint(0,reactions[r]['reaction_difficulty']) == 0:
                                reactants = [p,grid[str(n)]]
                                for x in reactants:
                                    if reactions[r]['products'][i.index(x.type)] == -1:
                                        clear_cell(x,x.pos)
                                        continue
                                    elif reactions[r]['products'][i.index(x.type)] == -2:
                                        continue
                                    else:
                                        del grid[str(x.pos)]
                                        pos = x.pos
                                        old_type = x.type
                                        del x
                                        new_x = Particle(pos,reactions[r]['products'][i.index(old_type)])
                                        set_cell(new_x,pos)
                else:
                    continue

def update_world() -> None:
    particles = list(grid.values())
    neighbors = {}
    for p in particles:
        if p.active:
            neighbors = move_particle(p)
            reaction_check(p,neighbors)
        if particle_types[p.type]['decay'] != None:
            if p.age > particle_types[p.type]['decay'][1] and randint(0,4) == 0:
                if particle_types[p.type]['decay'][0] != -1:
                    del grid[str(p.pos)]
                    pos = p.pos
                    old_type = p.type
                    del p
                    new_p = Particle(pos,particle_types[old_type]['decay'][0])
                    set_cell(new_p,pos)
                    continue
                else:
                    del grid[str(p.pos)]
                    del p
                    continue
        p.age += 1
            
        pygame.draw.rect(constants.DISPLAY,particle_types[p.type]['color'],(p.pos[0]*constants.CELLSIZE,p.pos[1]*constants.CELLSIZE,constants.CELLSIZE,constants.CELLSIZE))

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
                create_particle(Particle([x//constants.CELLSIZE,y//constants.CELLSIZE],selected_particle))

def initialize() -> None:
    for x in range(int(constants.WIDTH/constants.CELLSIZE)):
        create_particle(Particle([x,int(constants.HEIGHT/constants.CELLSIZE)-1],1))
        create_particle(Particle([x,0],1))
    for y in range(int(constants.HEIGHT/constants.CELLSIZE)):
        create_particle(Particle([0,y],1))
        create_particle(Particle([int(constants.WIDTH/constants.CELLSIZE)-1,y],1))

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
    update_world()
    cursor_rect = pygame.Rect((pygame.mouse.get_pos()[0]//constants.CELLSIZE)*constants.CELLSIZE,(pygame.mouse.get_pos()[1]//constants.CELLSIZE)*constants.CELLSIZE,constants.CELLSIZE*cursor_size,constants.CELLSIZE*cursor_size)
    pygame.draw.rect(constants.DISPLAY,(200,200,200),cursor_rect) # to add alpha this has to be a surface that is blitted to the screen
    constants.CLOCK.tick(constants.FPS)

if __name__ == '__main__':
    initialize()
    while True:
        main_loop()
