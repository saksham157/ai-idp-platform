@app.get("/generate-values/{service_id}")
def generate_values(service_id: int):

    db = SessionLocal()

    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:

        return {
            "error": "service not found"
        }

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("values.yaml.j2")

    output = template.render(

        service_name=service.service_name
    )

    file_path = "values.yaml"

    with open(file_path, "w") as file:

        file.write(output)

    return FileResponse(

        path=file_path,

        filename="values.yaml"
    )