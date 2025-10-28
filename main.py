from typing import Union

from fastapi import FastAPI

from links import links_routes
from movies import routes as movie_router
from ratings import ratings_routes
from tags import tags_routes

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(movie_router.router)
app.include_router(links_routes.router)
app.include_router(ratings_routes.router)
app.include_router(tags_routes.router)