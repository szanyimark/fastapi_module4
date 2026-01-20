from models import Article


def seed_articles(Session):
    """Create and return sample Article objects."""
    articles = [
        Article(
            title="Sample Article",
        ),
    ]
    return articles
