from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import os
import json


app = FastAPI()


class Person(BaseModel):
    """
    Class Person based on BaseModal
    """
    id: Optional[int] = None
    name: str
    age: int
    gender: str


file = os.path.join(os.getcwd(), 'people.json')
with open(file, 'r') as f:
    people = json.load(f)


@app.get('/person/{p_id}', status_code=200)
def get_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    return person[0] if len(person) else {}


@app.get('/search/', status_code=200)
def search_person(age: Optional[int] = Query(None, title='Age', description='The age to filter for'),
                  name: Optional[str] = Query(None, title='Name', description='The name to filter for')):
    person = [p for p in people if (age and age == p['age']) or (name and name.lower() in p['name'].lower())]

    return people if name is None and age is None else person
