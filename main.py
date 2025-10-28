from fastapi import FastAPI

from db_setup import create_db
from movies import routes as movie_router
from links import routes as links_routes
from ratings import ratings_routes
from tags import tags_routes

create_db()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(movie_router.router)
app.include_router(links_routes.router)
app.include_router(ratings_routes.router)
app.include_router(tags_routes.router)
