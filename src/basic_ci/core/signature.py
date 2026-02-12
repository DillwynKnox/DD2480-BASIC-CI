import hashlib
import hmac

from fastapi import Depends, Header, HTTPException, Request

from basic_ci.core.config import Settings, get_settings


class InvalidSignature(Exception):
    """
    Raised when there are errors with webhook signature such as it missing or not matching expected format.
    """
    pass

class Signature_verifier:
    def __init__(self, settings: Settings):
        """
        Initializes signature varifier. 
        
        Args:
            settings(Settings): Object with configuration details such as github webhook secret.
        """
        
        self.settings = settings
        
        
    def verify_signature(
            self,
            *,
            body: bytes,
            signature_header: str
    ):
        """
        Varifyes github webhook secret.
        
        Args:
            body(bytes): HTTP request body in raw bytes.
            signature_header(str): Value of signature header.
            
        Raises:
            InvalidSignature: If header does not match.
        """
        
        
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
    
    """
    Uses fastAPI features to validate github webhook request signature.
    
    Args:
        request (Request): Incoming FastAPI request object.
        x_hub_signature_256 (str): Signature header from request.
        settings (Settings): Application configurations.

    Returns:
        Signature_verifier: Varifier that has validated the request signature.

    Raises:
        HTTPException: If the signature is invalid.
    
    """  
    verifier = Signature_verifier(settings=settings)
    
    body = await request.body()
    try:
        verifier.verify_signature(body=body, signature_header=x_hub_signature_256)
    except InvalidSignature as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return verifier