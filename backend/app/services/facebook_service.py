import httpx
from sqlalchemy.orm import Session
from app.models.facebook import FacebookPage
from app.core.crypto import decrypt_token

class FacebookTokenInvalidError(Exception):
    pass

def get_valid_page_token(db: Session) -> str:
    fb_page = db.query(FacebookPage).filter(FacebookPage.is_active == True).first()
    if not fb_page:
        raise FacebookTokenInvalidError("No active Facebook Page connected. Please connect from Settings.")
    
    token = decrypt_token(fb_page.access_token_encrypted)
    
    # Verify token validity via Graph API
    url = f"https://graph.facebook.com/v19.0/me?access_token={token}"
    response = httpx.get(url)
    
    if response.status_code != 200:
        # Token is invalid or expired
        raise FacebookTokenInvalidError("Your Facebook connection has expired or is invalid. Please reconnect from Settings.")
        
    return token

