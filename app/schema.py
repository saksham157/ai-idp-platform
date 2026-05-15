from pydantic import BaseModel


class ServiceCreate(BaseModel):

    service_name: str

    team_name: str

    runtime: str

    docker_build: bool