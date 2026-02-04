# Contribute

To contribute please follow the following steps in order:

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

## Issue
First open an issue for the thing you want to do in github ([issues tab]().
The Issue should be atomar (meaning self contained but not unnecessary large).
Every Issue should start with either:
  - [DOC] for documentation (like writing README etc)
  - [FEAT] for implementing a new feature
  - [FIX] for fixing a bug
  - [REFA] for refactoring

If you start working on the issue assign it to yourself with the button for it on the right side.

## Branch
Once the issue is created open it in github and click create branch on the github page this will create a branch that has the same name as the issue.
Then go to your local setup and pull the new branch with:
```
git pull
```
then you can move to the new branch by:
```
git checkout the-name-of-your-issue
```

## Solve the Issue and Test
Do the actual thing that is described in the issue.
If it is a feature implement ALWAYS also implement a test for it in the `tests` folder that uses `pytest`
and the file should start with `test_` every seperate file should have a seperate test file.
Here is an article on endpoint testing in fastapi [Testing](https://fastapi.tiangolo.com/tutorial/testing/#extended-testing-file)

## Code convetions.
All imports should have the module path in them so imports always should look like
`from basic_ci.somethig import something`
 
 DO NOT USE:
 ```
 import src.something
 from src.csomething import something
 ```

 ## Fix formatting
 All code on main should be formatted with the code formatter to check if something violates the code style run:
 ```
 make lint
 ```
 and to fix all automatically fixable formatting problems run:
 ```
 make lint_fint
 ```

 


## Push your changes and create pull reqeust.

Once you have everything and all tests are green commit your changes to your branch.
Then pull the newsest changes to the main branch that might have happend while you worked on your issue with:
```
git fetch origin
```
Then rebase your branch so that on your branch your changes occur after the newest change on main with:

```
git rebase -i origin/main
```

Once you are done with this you can push your changes to your branch with 
```
git push
```
if you pushed already before the rebase you might need to do a force push with :
```
git push -f
```
but NEVER do a force push on main.

Then you can go to your branch or the [Pull Request Tab](https://gits-15.sys.kth.se/DD2480-Group-9/DECIDE/pulls) and create the pull request.
The pull request should have the same name as the issue and a description of what you did (can be from the issue description)

Then you wait for someone to approve it (feel free to ask someone).
Then you click the correct button on your pull request and it should get merged and the issue will get closed automatically.