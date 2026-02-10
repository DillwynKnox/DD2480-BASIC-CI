import hashlib
import hmac

import pytest

from basic_ci.core.config import Settings
from basic_ci.core.signature import InvalidSignature, Signature_verifier

"""
Constants used for testing
"""
SECRET_STR = "test_secret_key"
SECRET_BYTES = SECRET_STR.encode()
VALID_BODY = b'{"payload": "data"}'

@pytest.fixture
def verifier():
    """
    Creates a Signature_verifier instance with manually injected settings.
    This avoids reliance on FastAPI's dependency injection during unit tests.
    """
    mock_settings = Settings(GITHUB_WEBHOOK_SECRET=SECRET_STR)
    return Signature_verifier(settings=mock_settings)

def test_verify_signature_success(verifier):
    """
    Correct signature should not raise an exception.
    """
    mac = hmac.new(SECRET_BYTES, VALID_BODY, hashlib.sha256)
    valid_header = f"sha256={mac.hexdigest()}"
    
    verifier.verify_signature(body=VALID_BODY, signature_header=valid_header)

def test_verify_signature_malformed_header(verifier):
    """
    Malformed signature header should raise InvalidSignature with 'Malformed signature'.
    """
    with pytest.raises(InvalidSignature, match="Malformed signature"):
        verifier.verify_signature(body=VALID_BODY, signature_header="invalidformat")

def test_verify_signature_unsupported_algorithm(verifier):
    """
    Unsupported algorithm in signature header should raise InvalidSignature with 'Unsupported algorithm'.
    """
    with pytest.raises(InvalidSignature, match="Unsupported algorithm"):
        verifier.verify_signature(body=VALID_BODY, signature_header="md5=somesignature")

def test_verify_signature_mismatch(verifier):
    """
    A signature that does not match the body should raise InvalidSignature with 'Signature mismatch'.
    """
    wrong_mac = hmac.new(SECRET_BYTES, b"different_body", hashlib.sha256)
    invalid_header = f"sha256={wrong_mac.hexdigest()}"
    
    with pytest.raises(InvalidSignature, match="Signature mismatch"):
        verifier.verify_signature(body=VALID_BODY, signature_header=invalid_header)