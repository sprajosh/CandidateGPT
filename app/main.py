from fastapi import FastAPI

from app.api.v1.routes import candidate, opportunity
from app.scripts.create_tables import create_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


app.include_router(opportunity.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(candidate.router, prefix="/candidates", tags=["Candidates"])
