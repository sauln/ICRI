from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.setup import Result

from src import Heuristic, Search, RollOut

engine = create_engine('sqlite:///db/results.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def add_fake():
    add_result_line("r101", 4,  5,"a,b,c,d,ed,e,d,e")
    add_result_line("r102", 34, 5,"a,b,c,d,ed,e,d,e")
    add_result_line("r103", 12,12,"a,b,c,d,ed,e,d,e")
    add_result_line("r104", 1, 43,"a,b,c,d,ed,e,d,e")

def add_result_line(problem, num_vehicles, total_dist, vehicles):
    session.add( Result(problem=problem,

                        num_vehicles=num_vehicles, 
                        total_dist=total_dist,
                        vehicles=vehicles
                        ))
    session.commit()

def save_result_to_db(problem, solution, params):

    search_type = Search().__class__.__bases__[0].__name__
    heuristic_type = Heuristic().__class__.__bases__[0].__name__
    rollout_type = RollOut().__class__.__bases__[0].__name__

    res = Result(problem=problem, 
                 search_type=search_type, 
                 heuristic_type=heuristic_type, 
                 rollout_type=rollout_type,
                 run_type=params.run_type,
                 algo_type=params.algo_type,
                 num_vehicles=solution.num_vehicles, 
                 total_distance=solution.total_distance,
                 width=params.width, 
                 depth=params.depth, 
                 count=params.count,
                 d0=solution.params[0], 
                 d1=solution.params[1], 
                 d2=solution.params[2],
                 d3=solution.params[3], 
                 d4=solution.params[4], 
                 solution_string=solution.solution.pretty_print()
                 )

    session.add(res)
    session.commit()

def get_results():
    return session.query(Result)

def print_results():
    for result in get_results():
        print(result)

