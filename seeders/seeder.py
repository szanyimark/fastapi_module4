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
        articles = []
        for i in range(2):
            articles.extend(seed_articles(Session))

        for article in articles:
            # Create comments
            comments = seed_comments(Session)

            # Associate comments with the article
            article.comments = comments

        # Add and commit the articles (with comments)
        for article in articles:
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
