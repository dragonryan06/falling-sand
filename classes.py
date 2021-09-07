import pygame, sys, world
pygame.init()

"""
Stores constant data and classes
"""

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
        'reactants':[[3,4],[3,7],[3,9]],
        'products':[4,-2],
        'reaction_difficulty':2 # this is basically since there is no energy, the more energy required the less likely it is to happen.
    },
    {
        'name':'wood combust',
        'reactants':[[6,4],[6,7],[6,9]],
        'products':[7,-2],
        'reaction_difficulty':8
    },
    {
        'name':'oil combust',
        'reactants':[[8,4],[8,7],[8,9]],
        'products':[9,-2],
        'reaction_difficulty':5
    }
]

class constants:
    WIDTH, HEIGHT = 1024, 512
    BACKGROUND = (0,0,0)
    FPS = 30
    DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
    CLOCK = pygame.time.Clock()
    CELLSIZE = 4
    CHUNKSIZE = 64

class Particle:
    def __init__(self,pos,particle_type):
        self.pos = pos
        self.type = particle_type
        self.active = False
        self.age = 0
        self.color = []
        #self.velocity

class Chunk:
    def __init__(self,pos:list) -> None:
        self.bounds = pygame.Rect(pos[0]*constants.CHUNKSIZE,pos[1]*constants.CHUNKSIZE,constants.CHUNKSIZE,constants.CHUNKSIZE)
        print(self.bounds)
        self.data = {}
        self.dirty_rect = None
    
    def add_particle(self,pos:list,particle:Particle) -> None:
        self.data[str(pos)] = particle
        if particle_types[particle.type]['move_type'] != 'static':  
            self.expand_dirty_rect(pos)

    def remove_particle(self,pos:list) -> None:
        del self.data[str(pos)]
        self.expand_dirty_rect(pos)

    def expand_dirty_rect(self,pos:list) -> None:
        if self.dirty_rect == None:
            self.dirty_rect = pygame.Rect(pos[0]-1,pos[1]-1,3,3)
            if self.dirty_rect.left < self.bounds.left:
                self.dirty_rect.left = self.bounds.left
            if self.dirty_rect.right > self.bounds.right:
                self.dirty_rect.right = self.bounds.right
            if self.dirty_rect.top < self.bounds.top:
                self.dirty_rect.top = self.bounds.top
            if self.dirty_rect.bottom > self.bounds.bottom:
                self.dirty_rect.bottom = self.bounds.bottom
        else:
            left,right,top,bottom = self.dirty_rect.left,self.dirty_rect.right,self.dirty_rect.top,self.dirty_rect.bottom
            if pos[0] <= self.dirty_rect.left:
                left = pos[0]-1
                if left < self.bounds.left:
                    left = self.bounds.left
            elif pos[0]+1 >= self.dirty_rect.right:
                right = pos[0]+2
                if right > self.bounds.right:
                    right = self.bounds.right
            if pos[1] <= self.dirty_rect.top:
                top = pos[1]-1
                if top < self.bounds.top:
                    top = self.bounds.top
            elif pos[1]+1 >= self.dirty_rect.bottom:
                bottom = pos[1]+2
                if bottom > self.bounds.bottom:
                    bottom = self.bounds.bottom
            self.dirty_rect = pygame.Rect(left,top,right-left,bottom-top)

    def update(self) -> None:
        old_dirty_rect = self.dirty_rect.copy()
        last_data = self.data.copy()
        self.dirty_rect = None
        for x in range(old_dirty_rect.left,old_dirty_rect.left+old_dirty_rect.width):
            for y in range(old_dirty_rect.top,old_dirty_rect.top+old_dirty_rect.height):
                if str([x,y]) in last_data.keys():
                    if particle_types[self.data[str([x,y])].type]['move_type'] != 'static':
                        moved = world.move_particle(last_data[str([x,y])],self)
                        if moved:
                            self.expand_dirty_rect([x,y])