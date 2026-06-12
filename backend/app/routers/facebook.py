import json
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode, quote
import httpx
import jwt

from app.core.config import settings
from app.core.database import get_db
from app.core.crypto import encrypt_token, decrypt_token
from app.services.auth import get_current_user
from app.models.user import User
from app.models.facebook import FacebookPage
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/facebook", tags=["facebook"])

def _create_state_token(user_id: str) -> str:
    return jwt.encode({"sub": str(user_id)}, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

def _verify_state_token(state: str) -> str:
    try:
        payload = jwt.decode(state, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid state token")

@router.get("/connect-url")
def get_connect_url(current_user: User = Depends(get_current_user)):
    state = _create_state_token(current_user.id)
    scopes = "pages_show_list,pages_read_engagement,pages_manage_posts"
    params = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
        "state": state,
        "scope": scopes,
        "response_type": "code"
    }
    url = f"https://www.facebook.com/v19.0/dialog/oauth?{urlencode(params)}"
    return {"url": url}

@router.get("/callback")
async def facebook_callback(code: str = Query(...), state: str = Query(...), db: Session = Depends(get_db)):
    # Verify user
    user_id = _verify_state_token(state)
    
    # Exchange code for user token
    async with httpx.AsyncClient() as client:
        token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        token_params = {
            "client_id": settings.FACEBOOK_APP_ID,
            "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "code": code
        }
        resp = await client.get(token_url, params=token_params)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        data = resp.json()
        short_lived_user_token = data.get("access_token")
        
        # Exchange short lived user token for long lived user token
        long_lived_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        ll_params = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "fb_exchange_token": short_lived_user_token
        }
        resp_ll = await client.get(long_lived_url, params=ll_params)
        if resp_ll.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get long lived token")
        ll_data = resp_ll.json()
        long_lived_user_token = ll_data.get("access_token")
        
        # Fetch pages
        pages_url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={long_lived_user_token}"
        pages_resp = await client.get(pages_url)
        if pages_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch pages")
        pages_data = pages_resp.json()
        accounts = pages_data.get("data", [])
        
        if len(accounts) == 0:
            return RedirectResponse(f"{settings.FRONTEND_URL}/settings/facebook?error=no_pages")
        elif len(accounts) == 1:
            page = accounts[0]
            # Exchange for long lived page token (since user token is LL, the page token returned here is also LL usually, but we can use the one returned)
            page_token = page.get("access_token")
            page_id = page.get("id")
            page_name = page.get("name")
            
            # Save to db
            fb_page = db.query(FacebookPage).first()
            if not fb_page:
                fb_page = FacebookPage()
                db.add(fb_page)
            
            fb_page.page_id = page_id
            fb_page.page_name = page_name
            fb_page.access_token_encrypted = encrypt_token(page_token)
            fb_page.is_active = True
            db.commit()
            return RedirectResponse(f"{settings.FRONTEND_URL}/settings/facebook?connected=true")
        else:
            # multiple pages, encode as json and redirect
            pages_list = [{"id": p["id"], "name": p["name"], "token": encrypt_token(p["access_token"])} for p in accounts]
            pages_json = json.dumps(pages_list)
            safe_pages = quote(pages_json)
            return RedirectResponse(f"{settings.FRONTEND_URL}/settings/facebook?pages={safe_pages}")

class SelectPageRequest(BaseModel):
    page_id: str
    page_name: str
    encrypted_token: str

@router.post("/select-page")
def select_page(req: SelectPageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fb_page = db.query(FacebookPage).first()
    if not fb_page:
        fb_page = FacebookPage()
        db.add(fb_page)
    
    fb_page.page_id = req.page_id
    fb_page.page_name = req.page_name
    fb_page.access_token_encrypted = req.encrypted_token # already encrypted from callback
    fb_page.is_active = True
    db.commit()
    return {"success": True}

@router.get("/status")
def get_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fb_page = db.query(FacebookPage).filter(FacebookPage.is_active == True).first()
    if not fb_page:
        return {"is_connected": False}
    return {
        "is_connected": True,
        "page_id": fb_page.page_id,
        "page_name": fb_page.page_name,
        "connected_at": fb_page.connected_at
    }

@router.delete("/disconnect")
def disconnect(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fb_page = db.query(FacebookPage).filter(FacebookPage.is_active == True).first()
    if fb_page:
        fb_page.is_active = False
        db.commit()
    return {"success": True}

