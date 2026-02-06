import hmac
import hashlib

class InvalidSignature(Exception):
    pass

class Signature_verifier:
    def __init__(self, secret: bytes):
        self.secret = secret

    def verify_signature(
            self,
            *,
            body: bytes,
            signature_header: str
    ):
        try:
            algo, signature = signature_header.split("=")
        except ValueError:
            raise InvalidSignature("Malformed signature")
        if algo != "sha256":
            raise InvalidSignature("Unsupported algorithm")
        mac = hmac.new(self.secret, body, hashlib.sha256)
        expected = mac.hexdigest()

        if not hmac.compare_digest(expected, signature):
            raise InvalidSignature("Signature mismatch")