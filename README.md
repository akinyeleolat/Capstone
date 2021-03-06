# Capstone
[![Build Status](https://travis-ci.org/akinyeleolat/Capstone.svg?branch=master)](https://travis-ci.org/akinyeleolat/Capstone)  [![Coverage Status](https://coveralls.io/repos/github/akinyeleolat/Capstone/badge.svg?branch=master)](https://coveralls.io/github/akinyeleolat/Capstone?branch=master)

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
- `. ./setup.sh`
- `. ./setup_db.sh`


#### For Development, 
- run `. ./start_dev.sh`

### Productions
- create app on `heroku`
- set `ENV` on heroku dashboard
- `heroku login`
- `heroku run python manage.py db upgrade -app application-name`
- run `python run.py`

## Running test
- `python test_runner.sh`

## Access Details
### Click the login link below:
[Login to Auth0](https://coffeeshop-ng.auth0.com/authorize?audience=capstone-movie-api&response_type=token&client_id=CY1QiGQBvxSZhP9KDQnNnNH9iklXBJxz&redirect_uri=http://localhost:8080/login-results
) 
### and user the login details below to generate a token
#### The app uses a third-party service (Auth0) for authentication.

### The 3 login details are as follows:
 | Email | Password | Role |
 | ------ | --------|  ---- |
 | producer@capstone.com|capstone2020#|Executive Producer |
 | director@capstone.com|capstone2020#|Casting Director|
 | assistant@capstone.com|capstone2020#|Casting Assistant|
 
 ## ENDPOINTS

### Use This [Heroku Base Url](https://cap.herokuapp.com) to access all the endpoints

 | Method | ROUTE | PERMISSION      | Role | Body | Description |
 | ------ | ----------- | -------------- | ---- |------------|-----|
 | Get | / | * | * | welcome to capstone movie | index page |
 | POST | /movies | post:movies | Executive Producer |{ title:"String", release_date:"YYYY-MM-DD" }| create a movie |
 | PATCH | /movies/id | patch:movies | Executive Producer/Casting Director |{ title:"String", release_date:"YYYY-MM-DD" }| Updates a movie |
 | GET | /movies | get:movies | All Registered Users  | N/A | Gets list of movies |
 | GET | /movies/id | get:movies | All Registered Users | N/A | Get a movie |
 | DELETE | /movies/id | delete:movies | Executive Producer | N/A | Delete a movie |
 | POST | /actors | post:actors | Executive Producer/Casting Director|{ name:"String", age:"Number", gender:"String" } |Create an actor |
 | PATCH | /actors/id | patch:actors | Executive Producer/Casting Director | { name:"optional String", age:"optional Number" gender:"optional String" }| Updates an actor |
 | GET | /actors | get:actors | All Registered Users | N/A | Gets list of actors |
 | GET | /actors/id | get:actors | All Registered Users | N/A | Get an actor |
 | DELETE | /actors/id | delete:actors | Executive Producer/Casting Director | N/A | delete an actor |


## Running test
- `python test_runner.sh`

## Technologies
- Python/Flask
- Auth0
- SQLAlchemy
- Flask-Migrate
- Flask-Script


## Authors
#### Oluwatosin Akinyele- [Capstone](https://capstone-ng.herokuapp.com)
 
