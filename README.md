# Basic CIIIIIIIIIIIII

## Repository Structure
`src/` is for the actual code `test` is for the tests.
`src` has the following subfolders:
- `api` all fastapi endpoints should be defined here
- `services` the logic for running the tests and compiling etc. (basically everything that is not technical)

## Setup
To Setup dependencies and the package run in the project root. (same level as `pyproject.toml`):
```
pip install uv
```

Everytime the pyproject.toml changes run 
```bash
uv sync --extra dev
```
or 
```bash
make setup
```
Then you need to copy the `.env.template` file to a file named just `.env` and fill in the correct values for the Configurations

## Run development server locally
To run the development server locally run:
```
make dev
```


## State of contribution
- **Davide Mario Attebrant Sbrzesny (dmas)**
Participated in all group meetings. Worked on git interaction, commandservices, various fixes and documentation and more. 

- **Gabriel Alejandro Arias Goa (gaag2)**
Participated in all group meetings. Worked on notificationservices, unique ID generation, making the pipeline work and more.


- **Mohamed Aziz Jribi (jribi)**
Participated in all group meetings. Worked on services that interact with files, loggers, docstrings to public methods and static syntax check and more.


- **Anton Trappe (trappe/DillwynKnox)**
Participated in all group meetings. Project leader and worked on core features and basic structure and design. FastAPI, endpoints for GitHub and setting up server and more.

- **Yasmine Schüllerqvist (yasmines)**
Participated in all group meetings. Worked on creating dataclasses for information from github, command services, task runner and more.


