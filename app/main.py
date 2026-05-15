from fastapi import FastAPI
from fastapi.responses import FileResponse
from jinja2 import Environment, FileSystemLoader

from .database import engine, Base, SessionLocal
from .models import Service
from .schema import ServiceCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def health():

    return {
        "status": "platform running"
    }


@app.post("/service")
def create_service(service: ServiceCreate):

    db = SessionLocal()

    new_service = Service(

        service_name=service.service_name,

        team_name=service.team_name,

        runtime=service.runtime,

        docker_build=service.docker_build
    )

    db.add(new_service)

    db.commit()

    db.refresh(new_service)

    return {
        "message": "service created successfully"
    }


@app.get("/services")
def get_services():

    db = SessionLocal()

    services = db.query(Service).all()

    return services


@app.get("/service/{service_id}")
def get_service(service_id: int):

    db = SessionLocal()

    service = db.query(Service).filter(Service.id == service_id).first()

    return service


@app.get("/generate-config/{service_id}")
def generate_config(service_id: int):

    db = SessionLocal()

    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:

        return {
            "error": "service not found"
        }

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("service.yaml.j2")

    output = template.render(

        service_name=service.service_name,

        team_name=service.team_name,

        runtime=service.runtime,

        docker_build=str(service.docker_build).lower()
    )

    file_path = "service.yaml"

    with open(file_path, "w") as file:

        file.write(output)

    return FileResponse(

        path=file_path,

        filename="service.yaml"
    )


@app.get("/generate-jenkinsfile/{service_id}")
def generate_jenkinsfile(service_id: int):

    db = SessionLocal()

    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:

        return {
            "error": "service not found"
        }

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("Jenkinsfile.j2")

    output = template.render()

    file_path = "Jenkinsfile"

    with open(file_path, "w") as file:

        file.write(output)

    return FileResponse(

        path=file_path,

        filename="Jenkinsfile"
    )