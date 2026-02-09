import pytest
import hmac
import hashlib
from basic_ci.core.signature import Signature_verifier, InvalidSignature
from basic_ci.core.config import Settings

"""
Test constants
"""
SECRET = "test_secret_key"
VALID_BODY = b'{"event": "push"}'

@pytest.fixture
def mock_settings():
    """
    Provides a Settings instance with a fixed secret for testing
    """
    return Settings(GITHUB_WEBHOOK_SECRET=SECRET)

@pytest.fixture
def verifier(mock_settings):
    """
    Provides a Signature_verifier initialized with mock settings
    """
    return Signature_verifier(settings=mock_settings)

def test_verify_signature_success(verifier):
    """
    A correct sha256 signature should pass without exceptions
    """
    mac = hmac.new(SECRET.encode(), VALID_BODY, hashlib.sha256)
    valid_header = f"sha256={mac.hexdigest()}"
    
    verifier.verify_signature(body=VALID_BODY, signature_header=valid_header)

def test_verify_signature_malformed_header(verifier):
    """
    Header without an equal sign should raise Malformed signature
    """
    with pytest.raises(InvalidSignature, match="Malformed signature"):
        verifier.verify_signature(body=VALID_BODY, signature_header="invalid_string")

def test_verify_signature_unsupported_algo(verifier):
    """
    Using an algorithm other than sha256 should raise Unsupported algorithm
    """
    with pytest.raises(InvalidSignature, match="Unsupported algorithm"):
        verifier.verify_signature(body=VALID_BODY, signature_header="sha1=hash")

def test_verify_signature_mismatch(verifier):
    """
    If the signature does not match the body, it should raise Signature mismatch
    """
    wrong_mac = hmac.new(SECRET.encode(), b"wrong body", hashlib.sha256)
    invalid_header = f"sha256={wrong_mac.hexdigest()}"
    
    with pytest.raises(InvalidSignature, match="Signature mismatch"):
        verifier.verify_signature(body=VALID_BODY, signature_header=invalid_header)