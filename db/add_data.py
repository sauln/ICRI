from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from setup import Result

engine = create_engine('sqlite:///db/Results.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def add_result_line(problem, num_vehicles, total_dist):
    session.add( Result(problem=problem, 
                        num_vehicles=num_vehicles, 
                        total_dist=total_dist))
    session.commit()

def get_results():
    return session.query(Results)

def print_results():
    for result in get_results():
        print(result)



