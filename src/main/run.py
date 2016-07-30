# -*- coding: utf-8 -*-
import os
import click
import time
import logging
from dotenv import find_dotenv, load_dotenv

import pickle
import sortedcontainers
import numpy as np

from src.visualization.visualize import PlotRoutes 
from src.main.Matrices  import Matrices
from src.main.Routes    import Routes
from src.main.Validator import Validator
from src.main.Vehicle   import Vehicle
from src.main.Customer  import Customer
from src.main.Heuristic import Heuristic
from src.main.RollOut   import *



@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Begin auxiliary algorithm file")
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    matrices = Matrices()
    matrices.build(sp.customers)

    logger.info('Construct routes')
    routes = constructRoute(sp)

    logger.info('Validate the routes')
    Validator(sp, routes).validate()
    print(routes)
    print("There are {} vehicles with {} allowed"\
        .format(len(routes), sp.numVehicles))
    PlotRoutes(routes)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

