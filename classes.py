import pygame, sys
pygame.init()

particle_types = [ # air has density of 0, negative values float to top, positive fall
    {
        'name':'sand',
        'move_type':'powder',
        'color':(235,225,52),
        'density':2
    },
    {
        'name':'wall',
        'move_type':'static',
        'color':(100,100,100),
        'density':100 # infinity 
    },
    {
        'name':'water',
        'move_type':'fluid',
        'color':(50,50,255),
        'density':1
    },
    {
        'name':'hydrogen',
        'move_type':'fluid',
        'color':(200,50,50),
        'density':-1
    }
]

class constants:
    WIDTH, HEIGHT = 1000, 500
    BACKGROUND = (0,0,0)
    FPS = 30
    DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
    CLOCK = pygame.time.Clock()
    CELLSIZE = 10

class Particle:
    def __init__(self,pos,particle_type):
        self.pos = pos
        self.type = particle_type
        self.active = False
        #self.velocity