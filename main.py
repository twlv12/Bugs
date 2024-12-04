import random as r
import pygame as pg
import numpy as np
import visualizer

inputNeurons = {
    "random" : "00001",
    "age" : "00010",
    "blockageleft" : "00011", 
    "blockageright" : "00100",
    "oscillator" : "00101",
    "positionx" : "00110",
    "positiony" : "00111",
    "popdensity" : "01000",
    "borderx" : "01001",
    "bordery" : "01010",
    "lastmovex" : "01011",
    "lastmovey" : "01100",
    "constant" : "01101",
    "blockageup" : "01110",
    "blockagedown" : "01111",
    }

outputNeurons = {
    "moveup" : "00001",
    "movedown" : "00010",
    "moveleft" : "00011",
    "moveright" : "00100",
    "moverandom" : "00101",
    }
#00 -> input
#01 -> output
#10 -> internal

worldSize = 128
screenSize = 720
genomeComplexity = 4

#---TO-DO---
#Implement connection conversion from binary and float remapping
#Create brain structure using genome
#Possibly filter redundant genes?
# ¦> May slow evolution as creatures might not be able to make new neurons? ->ask chatgpt
# ¦> start thinking about mutation function - bitwise mutation or random?


bugsList = []

def createGenome(genomeLength):
    numInternalNeurons = 0
    genome = ""
    
    for i in range(genomeLength):
        #genes are 20 bits FORMAT:: 00(sType)  00000(sID)  00(tType)  00000(tID)  00(cType)  0000(Weight)  BITS:: 2 5 2 5 2 4

        #creating random source and target neurons from dicts
        sourceType = r.choice(["10", "00", "00"])
        if sourceType == "00":
            sourceID = r.choice(list(inputNeurons.values()))
        elif sourceType == "10":
            #internal neurons ids are created:: get next id -> bin -> string -> slice 0b prefix -> add leading zeros
            sourceID = str(bin(numInternalNeurons)[2:].zfill(5))
            numInternalNeurons += 1
        sourceNeuron = sourceType + sourceID
    
        targetType = r.choice(["10", "01", "01"])
        if targetType == "01":
            targetID = r.choice(list(outputNeurons.values()))
        elif targetType == "10":
            targetID = str(bin(numInternalNeurons)[2:].zfill(5))
            numInternalNeurons += 1
        targetNeuron = targetType + targetID

        #excitor/inhibitor/inverter
        connectionType = r.choice(["00","01","10"]) #00-excitor 01-inhibitor 10-inverter
        #creating random weight from 0-15 inclusive (will be remapped 0-1 when connection created)
        weight = str(bin(r.randint(0,15))[2:].zfill(4))

        #print(sourceType, sourceID, targetType, targetID, connectionType, weight)
        gene = sourceNeuron + targetNeuron + connectionType + weight
        genome += gene
    return genome
        
def createBrain(genome):
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
        self.neurons = []
        self.connections = []
        
    def brainStep(self):
        for neuron in self.neurons:
            neuron.value = 0
        for connection in self.connections:
            connection.transmit()
    
    
class Neuron:
    def __init__(self, type, function, ID):
        self.type = type
        self.function = function
        self.ID = ID
        self.value = 0
            
        
class Connection:
    def __init__(self, source, target, type, weight):
        self.source = source
        self.target = target
        self.type = type
        self.weight = weight
        #MUST CONVERT THESE VALUES FROM BIN6
        
    def transmit(self):
        if self.type == "excitor": #00
            self.target.value += (self.source.value * self.weight)
        if self.type == "inhibitor": #01
            self.target.value -= (self.source.value * self.weight)
        if self.type == "inverter" : #10
            self.target.value = -(self.source.value * self.weight)


visualizer.createGraph(createGenome(genomeComplexity))