# -*- coding: utf-8 -*-

import os
import click
import logging

import matplotlib.pyplot as plt
import pickle
import networkx as nx

import src.prototype.routeConstructionAlgorithm as rt






def visualizeProblem(sp):
    xs = [c.xcoord for c in sp.customers]
    ys = [c.ycoord for c in sp.customers]
    depot = sp.customers[0]

    plt.scatter(xs, ys)
    plt.scatter(depot.xcoord, depot.ycoord, 250)
    plt.show()

def visualizeRoute(sp, route):
    logging.info("Open route: \n -- {}".format(sp))

    G = nx.Graph()
    G.add_node(1)
    G.add_node(2)
    G.add_note(3)
    G.add_edges_from([(1,2),(1,3)])
    nx.draw(G)
    plt.show()

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Plot problem {}'.format(input_filepath))

    with open(input_filepath, 'rb') as pickle_file:
        sp = pickle.load(pickle_file)
    logging.info("Open Problem: \n -- {}".format(sp))

    
    #visualizeProblem(sp)

    logging.info("Find route")
    m = mat.Matrices(sp.customers)
    route = rt.routeConstruction(sp, m) 
    visualizeRoute(sp, route)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()

