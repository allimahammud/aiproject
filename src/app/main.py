from fastapi import FastAPI, Depends
from .routers import items, auth
from .database import Base, engine

# create DB tables (for SQLite development convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project API (expanded template)")

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "API is running"}
