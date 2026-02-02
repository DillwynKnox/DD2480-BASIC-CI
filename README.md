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


## Vscode Development
If you use Vscode add this into your `.vscode/settings.json`
```
"python.analysis.extraPaths": [
        "./src"
    ],
    "python.analysis.autoSearchPaths": true,
    "terminal.integrated.env.linux": {
        "PYTHONPATH": "${workspaceFolder}/src"
    },
    "terminal.integrated.env.osx": {
        "PYTHONPATH": "${workspaceFolder}/src"
    },
    "terminal.integrated.env.windows": {
        "PYTHONPATH": "${workspaceFolder}/src"
    }
```
And if you want to debug the application add this into your `.vscode/launch.json`
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI (src layout)",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "my_api.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "jinja": true,
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        }
    ]
}
```

This always starts the program from the main entrypoint in `main.py`

## State of contribution
- **Davide Mario Attebrant Sbrzesny (dmas)**


- **Gabriel Alejandro Arias Goa (gaag2)**


- **Mohamed Aziz Jribi (jribi)**


- **Anton Trappe (trappe)**


- **Yasmine Schüllerqvist (yasmines)**



