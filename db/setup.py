from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db/Results.db', echo=True)
Base = declarative_base()
 
class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    problem = Column(String)
    num_vehicles = Column(Integer)
    total_dist = Column(Float)

    def __repr__(self):
        return "<Result(problem='%s', num_vehicles='%s', total_dist='%s')>"%(\
            self.problem, self.num_vehicles, self.total_dist)


#print(Result.__table__)
Base.metadata.create_all(engine)

#Session = sessionmaker(bind=engine)
#session = Session()
#session.commit()

