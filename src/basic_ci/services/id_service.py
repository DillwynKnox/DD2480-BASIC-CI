import hashlib
import time
import uuid
from typing import Optional


class UIDService:
   

    def generate_run_id(self, commit_hash: Optional[str] = None, length: int = 24) -> str:
        """
        Creates a unique, lowercase, filename-safe identifier.

        - Unique across restarts (uses time + uuid + randomness)
        - Optionally mixes in the commit hash
        - Output is hex ([0-9a-f])
        """
        commit_part = (commit_hash or "").strip().lower()

        now_ns = time.time_ns()
        rand = uuid.uuid4().hex

        raw = f"{commit_part}|{now_ns}|{rand}".encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()

        length = max(12, min(length, 64))
        return digest[:length]
