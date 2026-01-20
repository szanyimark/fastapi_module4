from models import Comment


def seed_comments(Session):
    """Create and return sample Comment objects."""
    comments = [
        Comment(
            content="This is the first comment on the sample article.",
        ),
        Comment(
            content="This is the second comment on the sample article.",
        ),
    ]
    return comments
