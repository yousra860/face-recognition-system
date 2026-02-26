import sys
sys.path.append('.')

from src.core.database import SessionLocal
from src.core.security import get_password_hash
from src.models.face import User

def create_admin():
    db = SessionLocal()
    
    # Check if admin exists
    if db.query(User).filter(User.username == "admin").first():
        print("Admin user already exists!")
        return
    
    admin = User(
        username="admin",
        email="admin@university.dz",
        hashed_password=get_password_hash("admin123"),
        full_name="System Administrator",
        role="admin"
    )
    
    db.add(admin)
    db.commit()
    print("✅ Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")

if __name__ == "__main__":
    create_admin()
