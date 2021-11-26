
def add_nodes(graph, nodeList):
    for i in nodeList:
        graph.add_node(i)
        # print(i)


def add_edges(graph, edgeDictionary):
    startNodes = list(edgeDictionary.keys())
    for i in range(len(startNodes)):
        graph.add_edge(startNodes[i], edgeDictionary[startNodes[i]][0], weight=edgeDictionary[startNodes[i]][1])
        # Ex: graph[startNode][endNode]['weight']
        # print(startNodes[i], edgeDictionary[startNodes[i]])
