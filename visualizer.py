import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

inputNeurons = {
    "Random Value" : "00001",
    "Age" : "00010",
    "Blockage Left" : "00011", 
    "Blockage Right" : "00100",
    "Oscillator" : "00101",
    "X Position" : "00110",
    "Y Position" : "00111",
    "Bug Density" : "01000",
    "X Border Dist" : "01001",
    "Y Border Dist" : "01010",
    "Last X Move" : "01011",
    "Last Y Move" : "01100",
    "Constant" : "01101",
    "Blockage Above" : "01110",
    "Blockage Below" : "01111",
    }

outputNeurons = {
    "Move Up" : "00001",
    "Move Down" : "00010",
    "Move Left" : "00011",
    "Move Right" : "00100",
    "Jitter" : "00101",
    }

def decode(genome, inputDict=inputNeurons, outputDict=outputNeurons):
    decodedGenome = []
    for i in range(len(genome)//20):
        gene = genome[:20]

        if gene[:2] == "00": 
            sourceDict = inputDict.copy()
            sourceType = "input"
        if gene[:2] == "01": 
            sourceDict = outputNeurons.copy()
            sourceType = "output"
        if gene[:2] == "10": 
            sourceDict = "internal"
            sourceType = "internal"

        if sourceDict != "internal":
            #get neuron function from correct table using source indicator
            sourceID = list(sourceDict.keys())[list(sourceDict.values()).index(str(gene[2:7]))]
        else: sourceID = "internal"+str(int(gene[2:7], 2))

        if gene[7:9] == "00": 
            targetDict = inputDict.copy()
            targetType = "input"
        if gene[7:9] == "01": 
            targetDict = outputDict.copy()
            targetType = "output"
        if gene[7:9] == "10": 
            targetDict = "internal"
            targetType = "internal"

        if targetDict != "internal":
            targetID = list(targetDict.keys())[list(targetDict.values()).index(str(gene[9:14]))]
        else: targetID = "internal"+str(int(gene[9:14], 2))

        if gene[14:16] == "00": connectionType = "excitor"
        elif gene[14:16] == "01": connectionType = "inhibitor"
        elif gene[14:16] == "10": connectionType = "inverter"
        
        #converting binary weight to int 0-15 then remapped to 0-1
        rawWeight = int(gene[16:], 2)
        mappedWeight = round(np.interp(rawWeight, [0,15], [0.5,1]), 2)

        gene = [sourceType, sourceID, targetType, targetID, connectionType, mappedWeight]
        decodedGenome.append(gene)
        genome = genome[20:]
    #print(decodedGenome)
    return decodedGenome


def createGraph(input, figureNum):
    genome = decode(input)

    graph = nx.DiGraph()
    for gene in genome:
        if gene[1] not in graph:
            graph.add_node(gene[1], type=gene[0])
        if gene[3] not in graph:
            graph.add_node(gene[3], type=gene[2])
        
        graph.add_edge(gene[1], gene[3], connectionType=gene[4], weight=gene[5])

    nodeColours = []
    for node in graph.nodes():
        if graph.nodes[node]["type"] == "input":
            nodeColours.append("lightgreen")
        if graph.nodes[node]["type"] == "output":
            nodeColours.append("red")
        if graph.nodes[node]["type"] == "internal":
            nodeColours.append("grey")

    connectionColours = []
    connectionWidths = []
    for source, target, data in graph.edges(data=True):
        if data["connectionType"] == "excitor":
            connectionColours.append("lightgreen")
        elif data["connectionType"] == "inhibitor":
            connectionColours.append("red")
        elif data["connectionType"] == "inverter":
            connectionColours.append("blue")

        connectionWidth = data["weight"] * 5
        connectionWidths.append(connectionWidth)

    layout = nx.circular_layout(graph)
    plt.figure(i)
    nx.draw(graph, layout, with_labels=True, node_size=4000, font_weight="bold", node_color=nodeColours, edge_color=connectionColours, width=connectionWidths, font_size=10)
    plt.show()