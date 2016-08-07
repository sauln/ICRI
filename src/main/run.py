# -*- coding: utf-8 -*-
import os
import click
import time
import logging
from dotenv import find_dotenv, load_dotenv

import pickle
import sortedcontainers
import numpy as np

from src.visualization.visualize import Plotter
from src.main.Validator import Validator
from src.main.Vehicle   import Vehicle
from src.main.Customer  import Customer
from src.main.Heuristic import Heuristic
from src.main.RollOut   import RollOut 

from src.main.Parameters import Parameters
from src.main.Improvement import Improvement

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Begin auxiliary algorithm file")
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Setup parameters singleton')
    
    parameters = Parameters()
    parameters.build(sp, 10, 20)

    logger.info('Construct routes')
    
    
    d = [1,1,1,1,1,1,1] 
    # routes = Heuristic().run(d, parameters.depot, parameters.customers)
    # print(routes) 
    
    routes = RollOut().constructRoute()

    print("There are {} vehicles with {} allowed"\
        .format(len(routes), sp.numVehicles))
   
    print("Solution {}".format(routes))

    Plotter().plotRoutes(routes).show()
    #newRoutes = Improvement(routes)

    logger.info("Pickling routes")
    # pickle the set so we can use that for deving the 
    with open("data/interim/tmpr101.p", "wb") as f:
        pickle.dump(routes, f)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

