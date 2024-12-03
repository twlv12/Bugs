import random as r
import pygame as pg

inputNeurones = {
    "random" : 0000,
    "age" : 0001,
    "blockagex" : 0010,
    "blockagey" : 0011,
    "oscillator" : 0100,
    "positionx" : 0101,
    "positiony" : 0110,
    "popdensity" : 0111,
    "borderx" : 1000,
    "bordery" : 1001,
    "lastmovex" : 1010,
    "lastmovey" : 1010,
    "constant" : 1011,
    }

outputNeurones = {
    "moveup" : 0000,
    "movedown" : 0001,
    "moveleft" : 0010,
    "moveright" : 0011,
    "moverandom" : 0100,
    "setoscillator" : 0101,
    }

worldSize = 128
screenSize = 720
genomeLength = 8

bugsList = []

def createBrain():
    brain = Brain()

def initializeBug(pos):
    brain = createBrain()
    bug = Bug(pos, brain)

class Bug:
    def __init__(self, pos, brain):
        self.pos = pos
        self.brain = brain

class Brain:
    def __init__(self, genome):
        self.genome = genome
        self.neurones = []
        self.connections = []
        
    def brainStep(self):
        for neurone in self.neurones:
            neurone.value = 0
        for connection in self.connections:
            connection.transmit()
    
    
class Neurone:
    def __init__(self, type, function, ID):
        self.type = type
        self.function = function
        self.ID = ID
        self.value = 0
            
        
class Connection:
    def __init__(self, source, target, type):
        self.source = source
        self.target = target
        self.type = type
        
    def transmit(self):
        if self.type == "excitor":
            self.target.value += self.source.value
        elif self.type == "inhibitor":
            self.target.value -= self.source.value

pg.init()
screen = pg.display.set_mode((screenSize, screenSize))
clock = pg.time.Clock()
