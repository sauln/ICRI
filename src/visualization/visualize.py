# -*- coding: utf-8 -*-

import os
import click
import logging

import matplotlib.pyplot as plt
import pickle

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Plot problem {}'.format(input_filepath))

    with open(input_filepath, 'rb') as pickle_file:
        route = pickle.load(pickle_file)

    logging.info("Open route: \n -- {}".format(route))

    xs = [c.xcoord for c in route.customers]
    ys = [c.ycoord for c in route.customers]
    depot = route.customers[0]

    plt.scatter(xs, ys)
    plt.scatter(depot.xcoord, depot.ycoord, 250)
    plt.show()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()

