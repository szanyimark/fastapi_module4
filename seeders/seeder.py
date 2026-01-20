from sqlalchemy.orm import sessionmaker
from seeders.article_seeder import seed_articles
from seeders.comment_seeder import seed_comments


def run_seeder(engine):
    """Main seeding logic to populate database with sample data."""
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Create articles
        articles = seed_articles(Session)
        article = articles[0]

        # Create comments
        comments = seed_comments(Session)

        # Associate comments with the article
        article.comments = comments

        # Add and commit the article (with comments)
        session.add(article)
        session.commit()

        print(f"✓ Seeded article: '{article.title}'")
        print(f"✓ Seeded {len(comments)} comments")
        print("✓ Database seeded successfully!")

    except Exception as e:
        session.rollback()
        print(f"✗ Error seeding database: {e}")

    finally:
        session.close()
