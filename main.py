from fastapi import FastAPI, Query, HTTPException
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


with open(os.path.join(os.getcwd(), 'people.json'), 'r') as f:
    people = json.load(f)


@app.get('/person/{p_id}', status_code=200)
def person_get(p_id: int):
    """
    Method for getting person by ID
    """
    person = [p for p in people if p['id'] == p_id]
    return person[0] if len(person) else {}


@app.get('/search', status_code=200)
def person_search(age: Optional[int] = Query(None, title='Age', description='The age to filter for'),
                  name: Optional[str] = Query(None, title='Name', description='The name to filter for')):
    """
    Method for getting person(s) filtered by name/age params
    """
    person = [p for p in people if (age and age == p['age']) or (name and name.lower() in p['name'].lower())]

    return people if name is None and age is None else person


@app.post('/add', status_code=201)
def person_add(person: Person):
    """
    Method to create a new person
    """
    person = {
        'id': max([p['id'] for p in people]) + 1,
        'name': person.name,
        'age': person.age,
        'gender': person.gender
    }

    people.append(person)

    with open(os.path.join(os.getcwd(), 'people.json'), 'w') as f:
        json.dump(people, f)

    return person


@app.put('/update', status_code=204)
def person_update(person: Person):
    """
    Method to update an existing person
    """
    new_person = {
        'id': person.id,
        'name': person.name,
        'age': person.age,
        'gender': person.gender
    }

    existing_person = [p for p in people if p['id'] == person.id]

    if len(existing_person):
        people.remove(existing_person[0])
        people.append(new_person)

        with open(os.path.join(os.getcwd(), 'people.json'), 'w') as f:
            json.dump(people, f)

        return person
    else:
        return HTTPException(status_code=404, detail=f'Person with id {person.id} does not exist!')


@app.delete('/delete/{p_id}', status_code=200)
def person_delete(p_id: int):
    """
    Method to delete person by ID
    """
    person = [p for p in people if p['id'] == p_id]

    if len(person):
        people.remove(person[0])

        with open(os.path.join(os.getcwd(), 'people.json'), 'w') as f:
            json.dump(people, f)

        return person
    else:
        return HTTPException(status_code=404, detail=f'Person with id {p_id} does not exist!')