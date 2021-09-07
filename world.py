import pygame, sys
from classes import *
from random import randint
pygame.init()

"""
Handles all simulation events
"""

grid = {} # format: {cell:obj}
chunks = {} # format: {pos:obj}

def get_chunk(pos:list):
    return chunks[str([pos[0]//constants.CHUNKSIZE,pos[1]//constants.CHUNKSIZE])]

def create_particle(particle:Particle) -> None:
    chunk = chunks[str([particle.pos[0]//constants.CHUNKSIZE,particle.pos[1]//constants.CHUNKSIZE])]
    chunk.add_particle(particle.pos,particle)
    # grid[str(particle.pos)] = particle
    # if particle_types[particle.type]['move_type'] != 'static':
    #     particle.active = True
    particle.color = []
    for i in particle_types[particle.type]['color']:
        sign = randint(0,1)
        if sign == 0:
            sign = -1
        value = i+randint(0,10)*sign
        if value > 255:
            value = 255
        if value < 0:
            value = 0
        particle.color.append(value)
        # TODO change this system to instead of assigning and saving a color, color things based on their x,y position with some sort of random map or something

def set_cell(particle:Particle,pos:list) -> None:
    get_chunk(pos).add_particle(pos,particle)
    particle.pos = pos

def clear_cell(particle:Particle,pos:list) -> None:
    get_chunk(pos).remove_particle(pos)

def update() -> None:
    for c in chunks.values():
        if c.dirty_rect != None:
            c.update()

def update_OLD() -> None:
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
                    create_particle(Particle(pos,particle_types[old_type]['decay'][0]))
                    continue
                else:
                    del grid[str(p.pos)]
                    del p
                    continue
        p.age += 1
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
                                        create_particle(Particle(pos,reactions[r]['products'][i.index(old_type)]))
                else:
                    continue

def move_particle(particle:Particle) -> bool: # i believe its possible particles could move twice if they were displaced by another particle falling and then they moved, this probably can be fixed with a "moved" bool property that says if the particle moved that frame already
    moved = False
    direction = randint(0,1) # TODO change this entire function to get the chunk for every position it works with so it doesnt mess up at chunk edges
    if direction == 0: # also the weird teleportation where particles move an extra block at chunk borders is due to the particles moving wtice per frame from the new dirty rect not remmebering the particle
        direction = -1
    neighbors = { # left/right is relative to which dir was picked to go first by the randint
        'down' : [particle.pos[0],particle.pos[1]+1],
        'downdiagonal1' : [particle.pos[0]+direction,particle.pos[1]+1],
        'downdiagonal2' : [particle.pos[0]-direction,particle.pos[1]+1],
        'side1' : [particle.pos[0]+direction,particle.pos[1]],
        'side2' : [particle.pos[0]-direction,particle.pos[1]],
        'up' : [particle.pos[0],particle.pos[1]-1],
        'updiagonal1' : [particle.pos[0]+direction,particle.pos[1]-1],
        'updiagonal2' : [particle.pos[0]-direction,particle.pos[1]-1]
        }

    if not str(neighbors['down']) in get_chunk(neighbors['down']).data.keys() and particle_types[particle.type]['density'] > 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['down'])
        moved = True
    elif str(neighbors['down']) in get_chunk(neighbors['down']).data.keys() and particle_types[get_chunk(neighbors['down']).data[str(neighbors['down'])].type]['density'] < particle_types[particle.type]['density']:
        clear_cell(particle,particle.pos)
        replacing_particle = get_chunk(neighbors['down']).data[str(neighbors['down'])]
        clear_cell(get_chunk(neighbors['down']).data[str(neighbors['down'])],neighbors['down'])
        set_cell(replacing_particle,particle.pos)
        set_cell(particle,neighbors['down'])
        moved = True

    elif not str(neighbors['downdiagonal1']) in get_chunk(neighbors['downdiagonal1']).data.keys() and particle_types[particle.type]['density'] > 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal1'])
        moved = True
    elif str(neighbors['downdiagonal1']) in get_chunk(neighbors['downdiagonal1']).data.keys() and particle_types[get_chunk(neighbors['downdiagonal1']).data[str(neighbors['downdiagonal1'])].type]['density'] < particle_types[particle.type]['density']:
        clear_cell(particle,particle.pos)
        replacing_particle = get_chunk(neighbors['downdiagonal1']).data[str(neighbors['downdiagonal1'])]
        clear_cell(get_chunk(neighbors['downdiagonal1']).data[str(neighbors['downdiagonal1'])],neighbors['downdiagonal1'])
        set_cell(replacing_particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal1'])
        moved = True

    elif not str(neighbors['downdiagonal2']) in get_chunk(neighbors['downdiagonal2']).data.keys() and particle_types[particle.type]['density'] > 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal2'])
        moved = True
    elif str(neighbors['downdiagonal2']) in get_chunk(neighbors['downdiagonal2']).data.keys() and particle_types[get_chunk(neighbors['downdiagonal2']).data[str(neighbors['downdiagonal2'])].type]['density'] < particle_types[particle.type]['density']:
        clear_cell(particle,particle.pos)
        replacing_particle = get_chunk(neighbors['downdiagonal2']).data[str(neighbors['downdiagonal2'])]
        clear_cell(get_chunk(neighbors['downdiagonal2']).data[str(neighbors['downdiagonal2'])],neighbors['downdiagonal2'])
        set_cell(replacing_particle,particle.pos)
        set_cell(particle,neighbors['downdiagonal2'])
        moved = True

    # there is no need for having things bubble up as the substance the are in will push them up
    elif not str(neighbors['up']) in get_chunk(neighbors['up']).data.keys() and particle_types[particle.type]['density'] < 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['up'])
        moved = True
    
    elif not str(neighbors['updiagonal1']) in get_chunk(neighbors['updiagonal1']).data.keys() and particle_types[particle.type]['density'] < 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['updiagonal1'])
        moved = True
    
    elif not str(neighbors['updiagonal2']) in get_chunk(neighbors['updiagonal2']).data.keys() and particle_types[particle.type]['density'] < 0:
        clear_cell(particle,particle.pos)
        set_cell(particle,neighbors['updiagonal2'])
        moved = True

    elif particle_types[particle.type]['move_type'] == 'fluid':
        if not str(neighbors['side1']) in get_chunk(neighbors['side1']).data.keys():
            clear_cell(particle,particle.pos)
            set_cell(particle,neighbors['side1'])
            moved = True
        elif str(neighbors['side1']) in get_chunk(neighbors['side1']).data.keys() and particle_types[get_chunk(neighbors['side1']).data[str(neighbors['side1'])].type]['density'] < particle_types[particle.type]['density']:
            clear_cell(particle,particle.pos)
            replacing_particle = get_chunk(neighbors['side1']).data[str(neighbors['side1'])]
            clear_cell(get_chunk(neighbors['side1']).data[str(neighbors['side1'])],neighbors['side1'])
            set_cell(replacing_particle,particle.pos)
            set_cell(particle,neighbors['side1'])
            moved = True

        elif not str(neighbors['side2']) in get_chunk(neighbors['side2']).data.keys():
            clear_cell(particle,particle.pos)
            set_cell(particle,neighbors['side2'])
            moved = True
        elif str(neighbors['side2']) in get_chunk(neighbors['side2']).data.keys() and particle_types[get_chunk(neighbors['side2']).data[str(neighbors['side2'])].type]['density'] < particle_types[particle.type]['density']:
            clear_cell(particle,particle.pos)
            replacing_particle = get_chunk(neighbors['side2']).data[str(neighbors['side2'])]
            clear_cell(get_chunk(neighbors['side2']).data[str(neighbors['side2'])],neighbors['side2'])
            set_cell(replacing_particle,particle.pos)
            set_cell(particle,neighbors['side2'])
            moved = True
    return moved