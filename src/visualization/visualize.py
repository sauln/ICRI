# -*- coding: utf-8 -*-
import os
import click
import logging

import matplotlib.pyplot as plt
import pickle

def PlotRoutes(routes):
    print("Generate plot for routes solution") 
    for r in routes:
        xs = [c.xcoord for c in r]
        ys = [c.ycoord for c in r]#fix this
        plt.plot(xs, ys)
    depot = routes[0][0]

    plt.scatter(depot.xcoord, depot.ycoord, 250)
    plt.show()

def visualizeProblem(sp):
    xs = [c.xcoord for c in sp.customers]
    ys = [c.ycoord for c in sp.customers]
    depot = sp.customers[0]

    plt.scatter(xs, ys)
    plt.scatter(depot.xcoord, depot.ycoord, 250)
    plt.show()

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Plot problem {}'.format(input_filepath))

    with open(input_filepath, 'rb') as pickle_file:
        sp = pickle.load(pickle_file)
    visualizeProblem(sp)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()

