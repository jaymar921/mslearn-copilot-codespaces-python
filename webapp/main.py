import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = 20


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}


# Example data for demonstration
COUNTRY_CITIES = {
    "usa": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "france": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
    "japan": ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Sapporo"],
    "philippines": ["Cebu City", "Talisay", "Minglanilla", "Somewhere", "Another"]
}

@app.get('/cities')
def get_cities(country: str = Query(..., description="Country name")):
    """
    Get a list of cities for a given country.
    Example: /cities?country=usa
    """
    cities = COUNTRY_CITIES.get(country.lower())
    if cities is None:
        return {"error": "Country not found"}
    return {"country": country, "cities": cities}