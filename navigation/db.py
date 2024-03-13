from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()

class NavigationState(Base):
    __tablename__ = 'NavigationState'

    id = Column(Integer, primary_key=True, default=0)
    state = Column(String, default="idle")
    routeTo = Column(String, nullable=True)
    route = Column(String, nullable=True)
    nextStep = Column(String, nullable=True)
    distToNextStep = Column(Float, nullable=True)
    currentX = Column(Float, default=0)
    currentY = Column(Float, default=0)
    heading = Column(Float, default=0)
    uiRequest = Column(String, nullable=True)

def init_session() -> Session:
    engine = create_engine('sqlite:///../compute/db/dev.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
