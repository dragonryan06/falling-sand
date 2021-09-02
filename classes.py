import pygame, sys
pygame.init()

particle_types = [ # air has density of 0, negative values float to top, positive fall
    {
        'name':'sand',
        'move_type':'powder',
        'color':(235,225,52),
        'density':3,
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
        'density':2,
        'reactions':[],
        'decay':None
    },
    {
        'name':'hydrogen',
        'move_type':'fluid',
        'color':(200,50,50),
        'density':-1,
        'reactions':[0],
        'decay':None
    },
    {
        'name':'fire_gas',
        'move_type':'fluid',
        'color':(235,110,52),
        'density':-1,
        'reactions':[0,1,2],
        'decay':[5,8] # [decay_into,decay_min_age]
    },
    {
        'name':'smoke',
        'move_type':'fluid',
        'color':(75,75,75),
        'density':-1,
        'reactions':[],
        'decay':[-1,24]
    },
    {
        'name':'wood',
        'move_type':'static',
        'color':(168,100,50),
        'density':100,
        'reactions':[1],
        'decay':None
    },
    {
        'name':'fire_solid',
        'move_type':'static',
        'color':(235,110,52),
        'density':100,
        'reactions':[],
        'decay':[4,20]
    },
    {
        'name':'oil',
        'move_type':'fluid',
        'color':(168,133,50),
        'density':2,
        'reactions':[2],
        'decay':None
    },
    {
        'name':'fire_liquid',
        'move_type':'fluid',
        'color':(235,110,52),
        'density':2,
        'reactions':[],
        'decay':[4,20]
    }
]
reactions = [
    {
        'name':'hydrogen combust',
        'reactants':[3,4],
        'products':[4,4],
        'reaction_difficulty':5 # this is basically since there is no energy, the more energy required the less likely it is to happen.
    },
    {
        'name':'wood combust',
        'reactants':[6,4],
        'products':[7,4],
        'reaction_difficulty':20
    },
    {
        'name':'oil combust',
        'reactants':[8,4],
        'products':[9,4],
        'reaction_difficulty':8
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