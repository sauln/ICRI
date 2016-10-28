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
    total_dist = Column(Float)
    vehicles = Column(String) # nosql like, just for storage
    # timestamp
    # parameters: reference a Parameters row

    def __repr__(self):
        return "<Result(problem='%s', num_vehicles='%s', total_dist='%s')>"%(\
            self.problem, self.num_vehicles, self.total_dist)

class Parameters(Base):
    ''' All the information needed to perfectly replicate the results of an experiment
    '''
    __tablename__ = 'parameter_sets'

    id = Column(Integer, primary_key=True)
    width = Column(Integer)
    depth = Column(Integer)
    searchs = Column(Integer)
    improvements = Column(Integer)
    search_type = Column(String)
    heuristic_type = Column(String)
    rollout_type = Column(String)
    repo_version = Column(String) # probably based on `git rev-parse --short HEAD`

    delta_1 = Column(Float) # these probably aren't necessary?
    delta_2 = Column(Float)
    delta_3 = Column(Float)
    delta_4 = Column(Float)
    delta_5 = Column(Float)

Base.metadata.create_all(engine)
