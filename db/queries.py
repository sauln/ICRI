from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.setup import Result

from src import Heuristic, Search, RollOut

engine = create_engine('sqlite:///db/results.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def remove_duplicates():
    pass
    
def params_in(params):
    return get_solutions(params).__len__ 

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


