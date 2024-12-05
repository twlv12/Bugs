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
#Add neuron functions and insert neuron activation after reset in brainStep()
#
#
#


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
    neuronMap = {}
    def getOrCreateNeuron(type, ID): #ensuring no redundant are created
        key = (type, ID)
        if key not in neuronMap:
            neuronMap[key] = Neuron(type, ID)
        return neuronMap[key] #returns the neuron object from dict
    
    brain = Brain(genome)
    decodedGenome = visualizer.decode(genome, inputNeurons, outputNeurons)
    for gene in decodedGenome:
        #gene:: sType, sID, tType, tID, cType, weight
        sourceNeuron = getOrCreateNeuron(gene[0], gene[1])
        targetNeuron = getOrCreateNeuron(gene[2], gene[3])
        brain.createConnection(sourceNeuron, targetNeuron, gene[4], gene[5])
    
    return brain


def initializeBug(genome=None): #optionally takes in genome, if not creates one
    if genome == None:
        genome = createGenome(genomeComplexity)
    brain = createBrain(genome)
    return Bug((0,0), brain) #pos is 0,0 - no world yet


class Bug:
    def __init__(self, pos, brain):
        self.pos = pos
        self.brain = brain

class Brain:
    def __init__(self, genome):
        self.genome = genome
        self.neuronMap = {} #ID: Object
        self.connectionMap = {} #Source ID: List of outgoing connections
        
    def brainStep(self):
        for neuron in self.neuronMap.values():
            neuron.value = 0
            #add neuron execution function here
        for connection in self.connectionMap.values():
            connection.transmit()


    def createConnection(self, source, target, connectionType, weight):
        connection = Connection(source, target, connectionType, weight)
        if source.ID not in self.connectionMap:
            self.connectionMap[source.ID] = []
        self.connectionMap[source.ID].append(connection)
    
    
class Neuron:
    def __init__(self, type, ID):
        self.type = type
        self.ID = ID
        self.value = 0
            
        
class Connection:
    def __init__(self, source, target, type, weight):
        self.source = source
        self.target = target
        self.type = type
        self.weight = weight
        
    def transmit(self):
        if self.type == "excitor": #00
            self.target.value += (self.source.value * self.weight)
        if self.type == "inhibitor": #01
            self.target.value -= (self.source.value * self.weight)
        if self.type == "inverter" : #10
            self.target.value = -(self.source.value * self.weight)


for i in range(5):
    bugsList.append(initializeBug())

visualizer.createGraph(bugsList)