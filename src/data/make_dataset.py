# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

from src.main.BaseObjects.SolomonProblem import SolomonProblem
from src.main.BaseObjects.Customer import Customer, Point

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    logger = logging.getLogger(__name__)
    logger.info('parsing solomon file {}'.format(input_filepath))

    customers = []
    
    with open(input_filepath, 'r') as f:
        lines = f.readlines()
        problem_name = lines[0].strip()
        rules = lines[4].split()
        
        num_vehicles, capacity = [int(r) for r in rules]

        header = lines[7]
        customers_lines = lines[9:]
        for line in customers_lines:
            data = [int(d) for d in line.split()]
            
            assert len(data) == 7, "must be 7 attributes for solomon dataset"
            cid = data[0]
            loc = Point(data[1], data[2])
            rest = data[3:]
            c = Customer(cid, loc, *rest)
            customers.append(c)

    problem = SolomonProblem(problem_name, num_vehicles, capacity, customers) 
    print(problem)

    with open(output_filepath, "wb") as f:
        pickle.dump(problem, f)

    logger.info("problem: %s", problem)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

