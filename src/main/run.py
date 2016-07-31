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
from src.main.RollOut   import constructRoute

from src.main.Parameters import Parameters

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
    parameters.build(sp)
    #parameters.problemSet = sp

    #logger.info('Setup matrices singleton')
    #matrices = Matrices()
    #matrices.build(sp.customers)

    logger.info('Construct routes')
    routes = constructRoute()

    logger.info('Validate the solution')
    Validator(routes).validate()

    logger.info("Pickling routes")
    # pickle the set so we can use that for deving the 
    with open("data/interim/tmpr101.p", "wb") as f:
        pickle.dump(routes, f)


    logger.info('Generate visualization of solution')
    Plotter().plotRoutes(routes)

    print(routes)
    print("There are {} vehicles with {} allowed"\
        .format(len(routes), sp.numVehicles))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

