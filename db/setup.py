from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db/results.db', echo=True)
Base = declarative_base()
 
class Result(Base):
    ''' Main results workhorse for cateloging and reporting on all runs '''
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    problem = Column(String)
    num_vehicles = Column(Integer)
    total_distance = Column(Float)
    vehicles = Column(String) # nosql like, just for storage
    solution_string = Column(String)    
    
    width = Column(Integer)
    depth = Column(Integer)
    count = Column(Integer)
    
    search_type = Column(String)
    heuristic_type = Column(String)
    rollout_type = Column(String)
    algo_type = Column(String)
    run_type = Column(String)
    
    d0 = Column(Float)
    d1 = Column(Float) # these probably aren't necessary?
    d2 = Column(Float)
    d3 = Column(Float)
    d4 = Column(Float)
    
    def __repr__(self):
        return "<Result(problem='%s', %s, %s, %s num_vehicles='%s', total_distance='%s')>"%(\
            self.problem, self.search_type, self.heuristic_type, self.rollout_type, \
            self.num_vehicles, self.total_distance)

Base.metadata.create_all(engine)

