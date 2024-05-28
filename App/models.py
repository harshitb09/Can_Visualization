from sqlalchemy import Boolean, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///users.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(20))  # Adjust length for phone number format
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    
    def get_id(self):
        return self.id

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Session factory for database interactions (can be moved to app.py if needed)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
