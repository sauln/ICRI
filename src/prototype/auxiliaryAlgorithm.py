# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

import numpy as np

from src.model.SolomonProblem import Customer, SolomonProblem
import generalizedCost as g
import src.model.Matrices as mat


class Route():
    def __init__(self):
        self.route = []

    def append(self, item):
        self.route.append(item)

    def __str__(self):
        a = '-'.join(str(i[1].cust_no) for i in self.route)
        s = sum(i[0] for i in self.route)
        return "Total: {0:.4g} {1}".format(s, a)

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self,index,value):
        self.route[index] = value

def aux(solomonProblem, matrices):
    #run the generalized cost function to the entire customer set

    cf = g.CostFunction(matrices.distMatrix) 
    
    route = Route()

    depot = solomonProblem.customers[0]
    cs    = solomonProblem.customers[1:]
    delta = [1]*7
    
    #a = [cf.g("d", depot,c) for c in cs]
    
    route.append((0, depot))

    for i in range(len(cs)):
        ns = [(cf.g("d", route[-1][1], c), c) for c in cs] 
        nextCust = sorted(ns, key=lambda c: c[0])[0] 
        cs.remove(nextCust[1])
        route.append(nextCust)
    
    print(route)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    m = mat.Matrices(sp.customers)

    aux(sp, m)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()


