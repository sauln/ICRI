from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.setup import Result

from src import Heuristic, Search, RollOut

engine = create_engine('sqlite:///db/results.db')
Session = sessionmaker(bind=engine)
session = Session()

def remove_duplicates():
   


def params_in(params):
    num_solutions=get_solutions(params).__len__()
    return num_solutions

def get_solutions(params):
    results = session.query(Result).filter(
            Result.width==params.width,
            Result.depth==params.depth,
            Result.count==params.count,
            Result.algo_type==params.algo_type,
            Result.run_type==params.run_type,
            Result.problem==params.problem).all()

    return results

def print_results():
    for result in get_results():
        print(result)

def get_results():
    return session.query(Result)


