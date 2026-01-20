import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models.article_comment_onetomany import Base
from seeders.seeder import run_seeder

# Load environment variables from .env file
load_dotenv()

# Access environment variables
db_user = os.getenv("POSTGRES_USER", "fastapi_user")
db_password = os.getenv("POSTGRES_PASSWORD", "fastapi_password")
db_name = os.getenv("POSTGRES_DB", "fastapi_week4")
db_host = os.getenv("DB_HOST", "postgres")  # Default to localhost if not set
db_port = os.getenv("DB_PORT", "5432")  # Default to 5432 if not set

# Construct database URL
#database_url = f"postgresql://<DB_USER>:<DB_PASS>@localhost/fastapi_week4"
database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

print(f"Database URL: {database_url}")
print(f"User: {db_user}")
print(f"Database: {db_name}")

# Initialize SQLAlchemy engine
engine = create_engine(database_url)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

# Your application code goes here
if __name__ == "__main__":
    print("FastAPI Demo App - Environment variables loaded successfully!")
    
    # Seed the database with sample data
    run_seeder(engine)
