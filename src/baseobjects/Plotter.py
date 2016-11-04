# -*- coding: utf-8 -*-
import os
import logging

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

import pickle

from .Customer import Customer
from .Vehicle import Vehicle

class Plotter:
    def __init__(self):
        pass

    def vehicles3D(self, dispatch):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
 
        print(dispatch)
        for vehicle in dispatch.vehicles:
            self.vehicle3D(ax, vehicle)

        plt.show()
        return self

    def vehicle3D(self, ax, vehicle):
        xs, ys, time = map(list, zip(*[(c.location.x, c.location.y, c.readyTime) 
            for c in vehicle.customerHistory]))

        time[-1] = 230
        ax.plot(xs,ys,time)

    def shadow_plot(self, shadow_costs):
        fig = plt.figure()

        print("Plot and save shadow costs")

        for p, var in enumerate(shadow_costs):
            num_vehicles = var[:,0]
            distances = var[:,1]
            lambdas = var[:,p+2]
           
            ax = fig.add_subplot(len(shadow_costs), 2, 2*p)
            ax.scatter(lambdas, distances)
            ax.set_title("Total distance of parameter {}".format(p))
            ax.yaxis.set_major_formatter(FormatStrFormatter("%.0f"))

            ax = fig.add_subplot(len(shadow_costs), 2, 2*p + 1)
            ax.scatter(lambdas, num_vehicles)
            ax.set_title("Total vehicles of parameter {}".format(p))

        plt.savefig("data/processed/shadow_costs.png")
        #    plt.show()
        return self 

    def customers3D(self, customers):
        # take list of cusomters
        # plot x,y, time 

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xs, ys, time = map(list, zip(*[(c.location.x, c.location.y, c.readyTime) 
            for c in customers]))
        #xs = [c.location.x for c in customers]
        #ys = [c.location.y for c in customers]
        #time = [c.readyTime for c in customers]
   
        ax.scatter(xs,ys, time)
        plt.show()


    def savefig(filename):
        plt.savefig(filename)
        


    def twoPlotComparison(self, plotFunc, before, after):
        plt.figure(1)
        plt.subplot(2, 1, 1)
        plotFunc(before)
        plt.title("Before")
        plt.subplot(2, 1, 2)
        plotFunc(after)
        plt.title("After")

        return self


    def beforeAndAfter(self, before, after):
        return self.twoPlotComparison(self.plotDispatch, before, after)

    def plotDispatch(self, dispatch):
        vehicles = dispatch.vehicles
        self.plotVehicles(dispatch.vehicles)
        self.plotCenter(dispatch.depot)
        return self

    def compareRouteSets(self, set1, set2):
        return self.twoPlotComparison(self.plotVehicles, set1, set2)


    def getPoints(self, vehicle):
        xs = [c.location.x for c in vehicle.customerHistory]
        ys = [c.location.y for c in vehicle.customerHistory]
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

    def plotVehicles(self, vehicles):
        #print("Generate plot for routes solution") 
        for r in vehicles:
            self.plotVehicle(r)
        return self

    def plotVehicle(self, vehicle):
        xs, ys = self.getPoints(vehicle)
        plt.plot(xs, ys)
        return self

    def plotCenter(self, center):
        plt.scatter(center.location.x, center.location.y, 250)
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

