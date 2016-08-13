# -*- coding: utf-8 -*-
import os
import click
import logging

import matplotlib.pyplot as plt
import pickle

from src.main.BaseObjects.Customer import Customer
from src.main.BaseObjects.Vehicle import Vehicle

class Plotter:
    def __init__(self):
        pass
   
    def beforeAndAfter(self, before, after):
        plt.figure(1)
        plt.subplot(2, 1, 1)
        self.plotRoutes(before)
        plt.title("Routes before improvement {}".format(len(before)))
        plt.subplot(2, 1, 2)
        self.plotRoutes(after)
        plt.title("Routes after improvement {}".format(len(after)))

        return self



    def getPoints(self, customers):
        if(type(customers) == Vehicle):
            xs = [c.xcoord for c in r]
            ys = [c.ycoord for c in r]#fix this
        else:
            xs = [c.x for c in customers]
            ys = [c.y for c in customers]
        return (xs, ys)


    def multiPlotRoutes(self, *routeSet):
        plt.figure(1)
        num = len(routeSet)
        for i, routes in enumerate(routeSet):
            plt.subplot(2,1,i)
            self.plotRoutes(routes)
    
        return self

    def show(self):
        plt.show()

    def draw(self):
        plt.draw()

    def plotCustomers(self, customers):
        xs, ys = self.getPoints(customers)
        plt.scatter(xs, ys)
        return self 

    def plotRoutes(self, routes):
        #print("Generate plot for routes solution") 
        for r in routes:
            self.plotRoute(r)
        self.plotCenter(depot[0][0])
        return self

    def plotRoute(self, route):
        xs, ys = self.getPoints(route)
        plt.plot(xs, ys)
        return self

    def plotCenter(self, center):
        if(type(center) == Customer):
            plt.scatter(center.xcoord, center.ycoord, 250)
        else:
            plt.scatter(center.x, center.y, 250)
        return self


def visualizeProblem(sp):
    xs, ys = self.getPoints(sp.customers)
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

