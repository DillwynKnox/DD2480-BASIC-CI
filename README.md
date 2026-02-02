# Basic CI

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
uv sync --extra dev
```


## vscode Development

This always starts the program from the main entrypoint in `main.py`

## State of contribution
- **Davide Mario Attebrant Sbrzesny (dmas)**


- **Gabriel Alejandro Arias Goa (gaag2)**


- **Mohamed Aziz Jribi (jribi)**


- **Anton Trappe (trappe)**


- **Yasmine Schüllerqvist (yasmines)**



