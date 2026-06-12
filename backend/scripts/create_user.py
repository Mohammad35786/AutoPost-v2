import os
import sys

# Add the parent directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User

def create_admin_user():
    Base.metadata.create_all(bind=engine)
    email = settings.ADMIN_EMAIL
    password = settings.ADMIN_PASSWORD
    
    if not email or not password:
        print("ADMIN_EMAIL and ADMIN_PASSWORD must be set in the environment.")
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User with email {email} already exists.")
            return

        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        print(f"Successfully created user {email}.")
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
