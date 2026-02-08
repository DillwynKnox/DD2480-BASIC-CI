from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class Github_basemodel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

class Github_user(Github_basemodel):
    name: str
    email: Optional[str]
    date: Optional[str] = None

class Commit_author(Github_user):
    pass


class Commit_committer(Github_user):
    pass

class Commit(Github_basemodel):
    id: str
    message: str
    timestamp: str
    url: str
    tree_id: str
    distinct: bool

    added: List[str]
    modified: List[str]
    removed: List[str]

    author: Commit_author
    committer: Commit_committer

class Head_commit(Commit):
    pass

class Repository_owner(Github_basemodel):
    login: str
    id: int

class Repository(Github_basemodel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool

    owner: Repository_owner

    html_url: str
    description: Optional[str]
    url: str

class Pusher(Github_user):
    pass


class Push_payload(Github_basemodel):
    ref: str
    before: str
    after: str

    created: bool
    deleted: bool
    forced: bool

    base_ref: Optional[str]
    compare: str

    repository: Repository
    commits: List[Commit]
    head_commit: Optional[Head_commit]

    pusher: Pusher
    sender: Optional[dict]
