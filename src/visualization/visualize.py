# -*- coding: utf-8 -*-

import os
import click
import logging

import matplotlib.pyplot as plt
import pickle
import networkx as nx

import src.prototype.routeConstructionAlgorithm as rt
import src.model.Matrices as mat





def visualizeProblem(sp):
    xs = [c.xcoord for c in sp.customers]
    ys = [c.ycoord for c in sp.customers]
    depot = sp.customers[0]

    plt.scatter(xs, ys)
    plt.scatter(depot.xcoord, depot.ycoord, 250)
    plt.show()

def visualizeRoute(sp, m):
    print("Begin Visualize Route")
    route = rt.routeConstruction(sp, m) 
    
    print("Enter Naive route")
    naive = rt.naiveRoute(sp, m)

    xs = [c.xcoord for c in sp.customers]
    ys = [c.ycoord for c in sp.customers]
    depot = sp.customers[0]

    edges = [(a[1].xcoord, a[1].ycoord) for a in route]
    edgesX = [edge[0] for edge in edges]
    edgesY = [edge[1] for edge in edges]

    nEdges = [(a[1].xcoord, a[1].ycoord) for a in naive]
    nEdgeX = [edge[0] for edge in nEdges]
    nEdgeY = [edge[1] for edge in nEdges]

    f = plt.figure(1)
    plt.scatter(xs, ys)
    plt.plot(edgesX, edgesY)
    plt.scatter(depot.xcoord, depot.ycoord, 250)
    plt.title("Route with single vehicle of Route Contruction Algorithm")

    g = plt.figure(2)
    plt.scatter(xs, ys)
    plt.plot(nEdgeX, nEdgeY)
    plt.title("Naive/greedy approach")
    plt.scatter(depot.xcoord, depot.ycoord, 250)

    plt.show()

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Plot problem {}'.format(input_filepath))

    with open(input_filepath, 'rb') as pickle_file:
        sp = pickle.load(pickle_file)
    m = mat.Matrices(sp.customers)
    visualizeRoute(sp, m)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()

