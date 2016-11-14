from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.setup import Result

#from src import Heuristic, Search, RollOut
from src import Heuristic, RollOut

engine = create_engine('sqlite:///db/results.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def save_result_to_db(params, solution):
    #search_type = Search().__class__.__bases__[0].__name__
    search_type="RandomSearch"
    heuristic_type = Heuristic().__class__.__bases__[0].__name__
    rollout_type = RollOut().__class__.__bases__[0].__name__

    res = Result(problem=params.problem,
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
                 solution_string=solution.solution.save_print()
                 )

    session.add(res)
    session.commit()

