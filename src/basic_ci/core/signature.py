import hmac
import hashlib
from fastapi import HTTPException,Request, Header, Depends

from basic_ci.core.config import Settings, get_settings

class InvalidSignature(Exception):
    pass

class Signature_verifier:
    def __init__(self, settings: Settings):
        self.settings = settings
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
        mac = hmac.new(self.settings.GITHUB_WEBHOOK_SECRET.encode(), body, hashlib.sha256)
        expected = mac.hexdigest()

        if not hmac.compare_digest(expected, signature):
            raise InvalidSignature("Signature mismatch")
        
async def get_signature_verifier(
    request: Request, 
    x_hub_signature_256: str = Header(...),
    settings: Settings = Depends(get_settings)
):    
    verifier = Signature_verifier(settings=settings)
    
    body = await request.body()
    try:
        verifier.verify_signature(body=body, signature_header=x_hub_signature_256)
    except InvalidSignature as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return verifier