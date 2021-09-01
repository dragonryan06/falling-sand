import pygame, sys
pygame.init()

particle_types = [ # air has density of 0, negative values float to top, positive fall
    {
        'name':'sand',
        'move_type':'powder',
        'color':(235,225,52),
        'density':2,
        'reactions':[],
        'decay':None
    },
    {
        'name':'wall',
        'move_type':'static',
        'color':(100,100,100),
        'density':100, # infinity
        'reactions':[],
        'decay':None
    },
    {
        'name':'water',
        'move_type':'fluid',
        'color':(50,50,255),
        'density':1,
        'reactions':[],
        'decay':None
    },
    {
        'name':'hydrogen',
        'move_type':'fluid',
        'color':(200,50,50),
        'density':-1,
        'reactions':[2],
        'decay':None
    },
    {
        'name':'fire_gas',
        'move_type':'fluid',
        'color':(235, 110, 52),
        'density':-1,
        'reactions':[0,2],
        'decay':[5,8] # [decay_into,decay_min_age]
    },
    {
        'name':'smoke',
        'move_type':'fluid',
        'color':(75,75,75),
        'density':-1,
        'reactions':[1],
        'decay':[-1,24]
    }
]
reactions = [
    {
        'name':'fire burn out',
        'reactants':[4], # reactant and product indexes correspond, reactant 0 will become product 0, and so on. making a product -1 will mean the reactant is removed
        'products':[5],
        'reaction_time':15
    },
    {
        'name':'smoke dissipate',
        'reactants':[5], # replace these two with a particle lifetime systm that maks particles decay
        'products':[-1],
        'reaction_time':45
    },
    {
        'name':'hydrogen combust',
        'reactants':[3,4],
        'products':[4,4],
        'reaction_time':5
    }
]

class constants:
    WIDTH, HEIGHT = 1000, 500
    BACKGROUND = (0,0,0)
    FPS = 30
    DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
    CLOCK = pygame.time.Clock()
    CELLSIZE = 5

class Particle:
    def __init__(self,pos,particle_type):
        self.pos = pos
        self.type = particle_type
        self.active = False
        self.age = 0
        #self.velocity