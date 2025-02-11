#!/usr/bin/env python3

try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

import random
from graphtheory.structures.edges import Edge
from graphtheory.structures.graphs import Graph
from graphtheory.forests.treecenter import TreeCenter
from graphtheory.forests.treeplot import TreePlotRadiusAngle


def make_halin_outer(n=4):
    """Create a random weighted Halin graph with the set of outer nodes."""
    if n < 4:
        raise ValueError("number of nodes must be greater than 3")
    graph = Graph(n)
    weights = list(range(1, 1 + 2 * n - 2))
    random.shuffle(weights)
    for node in range(n):
        graph.add_node(node)
    # Teraz trzeba dodawac krawedzie, ale nie moze zostac wierzcholek
    # stopnia 2. Startuje od gwiazdy.
    graph.add_edge(Edge(1, 0, weights.pop()))
    graph.add_edge(Edge(2, 0, weights.pop()))
    graph.add_edge(Edge(3, 0, weights.pop()))
    nodes = set([0, 1, 2, 3])
    node = 4
    while node < n:
        parent = random.sample(nodes, 1)[0]
        if graph.degree(parent) == 1:   # leaf, we must add two edges
            if node + 1 == n:
                continue
            nodes.add(node)
            graph.add_edge(Edge(parent, node, weights.pop()))
            node += 1
            nodes.add(node)
            graph.add_edge(Edge(parent, node, weights.pop()))
            node += 1
        else:    # degree > 2
            nodes.add(node)
            graph.add_edge(Edge(parent, node, weights.pop()))
            node += 1
    # Method 1. Finding root without TreeCenter.
    for node in graph.iternodes():
        if graph.degree(node) > 1:   # always present
            root = node
            break
    # Method 2. Finding root with TreeCenter.
    # TreeCenter reduces floating point errors for points.
    #algorithm = TreeCenter(graph)
    #algorithm.run()
    #root = algorithm.tree_center[0]
    # Wyznaczam slownik z punktami.
    algorithm = TreePlotRadiusAngle(graph)
    algorithm.run(root)
    L = list()   # for leafs
    for node in algorithm.point_dict:
        if graph.degree(node) == 1:   # leafs
            L.append(node)
    # Sortowanie lisci ze wzgledu na kat.
    L.sort(key=lambda node: algorithm.point_dict[node][1])
    n_leafs = len(L)
    for i in range(n_leafs):
        graph.add_edge(Edge(L[i], L[(i + 1) % n_leafs], weights.pop()))
    return graph, set(L)


def make_halin(n=4):
    """Create a random weighted Halin graph."""
    graph, outer = make_halin_outer(n)
    return graph


def make_halin_cubic_outer(n=4):
    """Create a random weighted cubic Halin graph with the set of outer nodes."""
    if n < 4:
        raise ValueError("number of nodes must be greater than 3")
    if n % 2:
        raise ValueError("odd number of nodes")
    graph = Graph(n)
    weights = list(range(1, 1 + 3 * n // 2))
    random.shuffle(weights)
    for node in range(n):
        graph.add_node(node)
    # Teraz trzeba dodawac krawedzie, ale nie moze zostac wierzcholek
    # stopnia 2. Startuje od gwiazdy.
    graph.add_edge(Edge(1, 0, weights.pop()))
    graph.add_edge(Edge(2, 0, weights.pop()))
    graph.add_edge(Edge(3, 0, weights.pop()))
    nodes = set([1, 2, 3])
    node = 4
    while node < n:
        parent = random.sample(nodes, 1)[0]
        nodes.remove(parent)   # to juz nie bedzie lisc
        nodes.add(node)   # nowy lisc
        graph.add_edge(Edge(parent, node, weights.pop()))
        node += 1
        nodes.add(node)   # nowy lisc
        graph.add_edge(Edge(parent, node, weights.pop()))
        node += 1
    # Method 1. Finding root without TreeCenter.
    for node in graph.iternodes():
        if graph.degree(node) > 1:   # always present
            root = node
            break
    # Method 2. Finding root with TreeCenter.
    # TreeCenter reduces floating point errors for points.
    #algorithm = TreeCenter(graph)
    #algorithm.run()
    #root = algorithm.tree_center[0]
    # Wyznaczam slownik z punktami.
    algorithm = TreePlotRadiusAngle(graph)
    algorithm.run(root)
    #print algorithm.point_dict
    L = list()   # for leafs
    for node in algorithm.point_dict:
        if graph.degree(node) == 1:   # leaf
            L.append(node)
    # Sortowanie lisci ze wzgledu na kat.
    L.sort(key=lambda node: algorithm.point_dict[node][1])
    n_leafs = len(L)
    for i in range(n_leafs):
        graph.add_edge(Edge(L[i], L[(i + 1) % n_leafs], weights.pop()))
    return graph, set(L)


def make_halin_cubic(n=4):
    """Create a random weighted cubic Halin graph."""
    graph, outer = make_halin_cubic_outer(n)
    return graph

# EOF
