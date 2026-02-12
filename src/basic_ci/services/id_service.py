import hashlib
import time
import uuid
from typing import Optional


class UIDService:
   

    def generate_run_id(self, commit_hash: Optional[str] = None, length: int = 24) -> str:
        """
        Generate a unique, lowercase, filename-safe identifier for a CI run.

        The identifier is created by combining:
        1. An optional commit hash (for deterministic runs)
        2. Current timestamp in nanoseconds (for uniqueness across time)
        3. A random UUID v4 (for uniqueness across processes)
        
        This combination is then hashed with SHA-256 to produce a fixed-length,
        uniformly distributed hex digest. The result is truncated to the
        requested length.

        Args:
            commit_hash (Optional[str]): Git commit SHA to incorporate into the ID.
                                       Same commit hash will produce same ID prefix
                                       (but full ID still includes time and randomness).
                                       Defaults to None.
            length (int): Desired length of the returned identifier.
                         Minimum: 12, Maximum: 64. Defaults to 24.

        Returns:
            str: Unique identifier consisting of lowercase hexadecimal characters
                [0-9a-f] of the specified length.
        """
        commit_part = (commit_hash or "").strip().lower()

        now_ns = time.time_ns()
        rand = uuid.uuid4().hex

        raw = f"{commit_part}|{now_ns}|{rand}".encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()

        length = max(12, min(length, 64))
        return digest[:length]
