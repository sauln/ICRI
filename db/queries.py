import functools
import pandas as pd
from operator import add
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.setup import Result
from src import Heuristic, RollOut

tab_root = 'sqlite:///db/'
#tables = ['results.db', 'results/gcloud_r.db', 'results/gcloud_results.db',
#          'results/gcloud_results_large.db', 'results/other_results.db',
#          'results/unknown_params_results.db']
tables = ['results.db']


def get_best_solutions():
    res = aggregate_results(tables)
    res = res.drop('id', 1).drop('_sa_instance_state', 1).drop_duplicates()

    best = res.loc[res.groupby('problem')['num_vehicles'].idxmin()]
    return best

def build_session(name):
    engine = create_engine(name)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def aggregate_results(tables):
    def get_records(t):
        session = build_session(tab_root + t)
        results = get_results(session)
        data_records = [rec.__dict__ for rec in results.all()]
        return data_records

    results_list = map(get_records, tables)
    results = functools.reduce(add, results_list, [])
    df = pd.DataFrame.from_records(results)
    return df

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

def get_results(session):
    return session.query(Result)

if __name__=='__main__':
    best = get_best_solutions()
    best['p_groups'] = best['problem'].map(lambda x: x.zfill(5)[:3])

    avg = best.groupby('p_groups')['num_vehicles'].mean()
    print(avg)

