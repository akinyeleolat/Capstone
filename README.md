# Capstone
As an Executive Producer within Capstone company, I have been able to create a system to simplify and streamline the process of creating movies and managing and assigning actors to those movies.

## Required Features
### Models:
- Movies with attributes title and release date
- Actors with attributes name, age and gender

### Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

## Roles:
### Casting Assistant
- Can view actors and movies

### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

## Tests:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

## Getting Started
### Clone this repo `https://github.com/akinyeleolat/Capstone.git`

- Navigate into the folder in your terminal

## Run the following command on your terminal
- `virtualenv venv`
- `pip install -r requirements.txt`
- `. setup.sh`
- `python manage.py db upgrade`
- `python manage.py seed`
- `flask run --reload`