from sqlalchemy import Column, String, DateTime, LargeBinary, Boolean, Integer
from src.core.database import Base
from datetime import datetime
import uuid

class FaceRecord(Base):
    __tablename__ = "face_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True)
    department = Column(String(100), nullable=True)
    face_encoding = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, nullable=True)
    access_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "access_count": self.access_count,
            "is_active": self.is_active
        }

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
