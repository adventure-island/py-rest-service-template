# py-rest-service-template
A Python REST micro-service project template that helps developers quickly generate 
production grade Python REST web applications using FastApi, Pydantic, Postgres, 
SQLAlchemy, Pytest, Poetry, Docker Compose, and more!

## Introduction  
  
This project serves as a template to facilitate the quick start of
the development of new REST micro service(s) in Python 3 runtime.  
  
Currently, following facilities and sample usages are provided off-the-shelf:  
* Fastapi application and middleware setup  
* Two sample micro services with following features
  * FastApi applications with middleware injection including
      * Dababase session management
      * Exception handler
  * Example JSONAPI schema defination using Pydantic
  * Example ORM definition and DAL(i.e., Data Access Layer) implementaion    
* Example API endpoints:  
  * `GET` endpoint to retrieve an object from Datastore  
  * `POST` endpoint to create a new object in Datastore  
  * `GET` endpoint to retrieve an object from SQL database  
  * `POST` endpoint to create a new object in SQL database  
* Test infrastructure(`pytest`)
  * Mocked cloud clients  
  * Test clients for Fastapi apps
  * Sample unit tests  
* Poetry dependency management  
* Dockerized environment for local development and testing  
* Sample GAE application configuration files and Cloudbuild scripts  
  
## Usage  
  
### Setup
1. Download this project(in .zip format so git files will be excluded) to you local workstation, unzip it and rename the project directory to your <PROJECT_NAME>  
2. Open a command line terminal, go to directory <PROJECT_NAME> and use it as your root working directory,   
   use a text editor to replace all occurrences of `py-rest-service-template` with <PROJECT_NAME>.  
3. Run following command to initialize a Python virtual environment  and make sure it's Python>=3.7
```
poetry shell  
source .venv/bin/activate 
python -V
```
5. Run following command to install dependencies from `poetry.lock`
```
poetry install
```

### Running and testing using Docker Compose
* Run following command to start services inside docker container and execute unit tests
```make test```
* Run following command to start services inside docker container without unit tests
```make run```

### Notes
#### Non-docker local development environment
* To speed up your development, if possible, use local (non-docker) virtual environment for you development and test, make sure all required emulators are up and running locally.
### Dependency management
* Use `poetry add/remove/update` to manage dependencies, DO NOT manually modify `poetry.lock`.
* Use `poetry add/remove some_lib --dev` to manage libraries that are not required for deployment.
* Before committing your change or starting up your local docker environment, make sure `requirements.txt` is up to date by running following command 
```poetry export -f requirements.txt --output requirements.txt --without-hashes```
* Run ```poetry export -f requirements.txt --output requirements-dev.txt --without-hashes --dev``` to export all dependencies for testing 
