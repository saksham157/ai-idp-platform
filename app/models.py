from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Service(Base):

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    service_name = Column(String, unique=True)

    team_name = Column(String)

    runtime = Column(String)

    docker_build = Column(Boolean)