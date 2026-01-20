import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base, Article, Comment
from seeders.seeder import run_seeder
from sqlalchemy.orm import sessionmaker

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

# Initialize SQLAlchemy engine
engine = create_engine(database_url)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

# Create session factory once
Session = sessionmaker(bind=engine)


def print_available_articles(session):
    """Display all available articles in the database."""
    all_articles = session.query(Article).all()
    
    if not all_articles:
        print("\nNo articles found in the database.")
        return False
    
    print("\n" + "="*50)
    print("AVAILABLE ARTICLES FOR TESTING:")
    print("="*50)
    for article in all_articles:
        print(f"  ID: {article.id} - Title: {article.title}")
    print("="*50)
    return True


def get_user_input():
    """Prompt user for article ID and return it. Returns 'exit' if user wants to quit."""
    while True:
        article_id = input("\nEnter an Article ID to view details (or 'exit' to quit): ").strip()
        
        if article_id.lower() == 'exit':
            return 'exit'
        
        try:
            return int(article_id)
        except ValueError:
            print("Invalid input. Please enter a valid number or 'exit' to quit.")
            # Loop continues to ask again


def print_article_details(session, article_id):
    """Retrieve and print article details with comments."""
    article = session.query(Article).filter(Article.id == article_id).first()
    
    if article:
        print("\n" + "="*50)
        print("ARTICLE DETAILS:")
        print("="*50)
        print(f"Article ID: {article.id}")
        print(f"Article Title: {article.title}")
        print(f"Number of comments: {len(article.comments)}")
        print("\nCOMMENTS:")
        print("-"*50)
        for comment in article.comments:
            print(f"  Comment ID: {comment.id}")
            print(f"  Content: {comment.content}")
            print("-"*50)
    else:
        print(f"\nArticle with ID {article_id} not found.")


# Your application code goes here
if __name__ == "__main__":
    print("FastAPI Demo App - Environment variables loaded successfully!")
    
    session = Session()

    # Seed only if there are no articles yet
    existing_count = session.query(Article).count()
    if existing_count == 0:
        print("No articles found. Seeding sample data...")
        run_seeder(engine)
    else:
        print(f"{existing_count} article(s) already present. Skipping seeder.")

    try:
        # Display available articles once
        if not print_available_articles(session):
            print("Cannot continue without articles in database.")
        else:
            # Loop until user types 'exit'
            while True:
                # Get article ID from user
                input_value = get_user_input()      
                          
                # Check if user wants to exit
                if input_value == 'exit':
                    print("\nExiting application. Goodbye!")
                    break
                article_id = input_value
                
                # Print article details
                print_article_details(session, article_id)
    
    finally:
        session.close()
