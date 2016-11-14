# -*- coding: utf-8 -*-
import os
import logging
import pickle

from .baseobjects import Customer, Point, SolomonProblem, Utils

LOGGER = logging.getLogger(__name__)

class DataBuilder:
    def __init__(self, input_filepath, output_filepath):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.lines = self.loadLines()
        self.problem = self.getProblemDefinition()
        Utils.save_sp(self.problem, self.output_filepath, "")

    def getProblemDefinition(self):
        LOGGER.debug('Extract problem definition.')
        lines = self.lines
        problem_name = lines[0].strip()
        rules = lines[4].split()
        num_vehicles, capacity = [int(r) for r in rules]
        header = lines[7]
        customers_lines = lines[9:]
        customers = [self.extractCustomer(c) for c in customers_lines]
        return SolomonProblem(problem_name, num_vehicles, capacity, customers)

    def extractCustomer(self, line):
        data = [int(d) for d in line.split()]
        assert len(data) == 7, "must be 7 attributes for solomon dataset"
        cid = data[0]
        loc = Point(data[1], data[2])
        rest = data[3:]
        return Customer(cid, loc, *rest)

    def loadLines(self):
        LOGGER.debug('Loading Solomon Problem from {}'.format(self.input_filepath))
        with open(self.input_filepath, 'r') as f:
            lines = f.readlines()
        return lines

def load_files(data_root):
    files = os.listdir(data_root)
    outfiles = [f.replace(".txt", ".p") for f in files]
    return (files, outfiles)

def convert_all():
    data_root = "data/raw"

    LOGGER = logging.getLogger(__name__)
    LOGGER.info('parsing all problems in'.format(data_root))

    files, outfiles = load_files(data_root)
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    convert_all()

