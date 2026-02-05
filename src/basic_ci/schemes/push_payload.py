from dataclasses import dataclass

##Useful link:
##https://docs.github.com/en/webhooks/webhook-events-and-payloads#push

@dataclass
class Author:
    date: str
    email: str | None
    name: str
    username: str

@dataclass
class Commiter:
    date: str
    email: str | None
    name: str
    username: str

@dataclass
class Commit: #Commits
    added: list[str]
    author: object | Author
    commiter: object| Commiter
    distinct: bool
    id: str
    message: str
    modified: list[str]
    removed: list[str]
    timestamp: str
    tree_id: str
    url: str

@dataclass
class Head_commit:
    added: list[str]
    author: object
    commiter: object
    distinct: bool
    id: str
    message: str
    modified: list[str]
    removed: list[str]
    timestamp: str
    tree_id: str
    url: str

@dataclass
class Pusher:
    date: str
    email: str | None
    name: str
    username: str
    
@dataclass
class Push_payload_parameters:
    after: str
    base_ref: str | None
    before: str
    commits: list[Commit]
    compare: str
    created: bool
    deleted: bool
    forced: bool
    head_commit: object|Head_commit | None
    installation: object
    pusher: object
    ref: str
    repository: object
    sender: object