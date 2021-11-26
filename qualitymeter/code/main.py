import os

from antlr4 import *
import networkx as nx
import networkx.algorithms.community as nx_comm
from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from relationChecker import realationListener
from handleGraph import add_nodes, add_edges
import re
import argparse


def compile_j(arg, graph):

    # Stage 1 --------------------------------------------------------------------------------------------------------
    stream = FileStream(arg, encoding='utf8')  # Step 1.1: Load input source into stream
    lexer = JavaLexer(stream)  # Step 1.2: Create an instance of AssignmentStLexer
    token_stream = CommonTokenStream(lexer)  # Step 1.3: Convert the input source into a list of tokens
    parser = JavaParserLabeled(token_stream)  # Step 1.4: Create an instance of the AssignmentStParser

    # Stage 2 --------------------------------------------------------------------------------------------------------
    parse_tree = parser.compilationUnit()  # Step 2.1: Create parse tree
    my_listener = realationListener()  # Step 2.2: Create an instance of AssignmentStListener
    walker = ParseTreeWalker()  # Step 2.3: Create a walker to traverse the parse tree
    walker.walk(t=parse_tree, listener=my_listener)  # Step 2.4: Traverse the parse tree using Listener
    # print('nodes are :', my_listener.getNodes())
    # print('edges are :', my_listener.getEdges())

    # Stage 3 --------------------------------------------------------------------------------------------------------
    add_nodes(graph, my_listener.getNodes())
    add_edges(graph, my_listener.getEdges())
    # print('Graph nodes are :', graph.nodes)
    # print('Graph edges are :', graph.edges)

def main():
    graph = nx.Graph()

    pattern = re.compile(r".+\.java$")
    for root, subdirs, files in os.walk('.'):
        java_file_names = list(filter(lambda f: pattern.match(f), files))
        for el in java_file_names:
            compile_j(os.path.join(root, el), graph)

    # Measure modularity
    q = nx_comm.modularity(graph, nx_comm.label_propagation_communities(graph))
    print(q)

if __name__ == '__main__':
    main()
