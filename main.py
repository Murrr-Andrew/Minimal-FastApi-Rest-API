from fastapi import FastAPI
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


@app.get('/person/{p_id}')
def get_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    return person[0] if len(person) else {}
