# falling-sand
This is a project I've been having a lot of fun with working on in study hall using a chromebook running a crostini linux vm. 

I initially made a project like this last year (also done in study hall) but I decided that that old code was just too unsustainable, so I started rewriting it this year.

# game systems
The game features particles like any falling sand game, that move following simple rules (if you want to learn more about these rules you can easily find a youtube video on them)
In this game, particle types have several properities, as of this version they have a move type, which determines if they can move horizontally or not, a color, a density which determines if they sink or float in other particles (and if they rise to the top, negative densities cause particles to fall upward) , and a decay value which transforms the particle when it reaches a certain age (if decay is specified)

another main system of the game is the reactions system, any interaction between two particles that transforms or destroys particles is handled as a reaction
for example, if wood touches fire, then there is a random chance that the wood will become a fire_solid particle (burning solid) and then that fire_solid eventually decays to fire_gas, which decays to smoke
this code right here allows for wood to burn in a pretty realistic manner and the same code can be applied to all sorts of chemical reactions in the future

the main challenge with this project is getting it to run smooth on a semi dated chromebook with all its complexity and so far its been going fine.
