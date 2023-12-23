from habr.models import Article, Author


def analyze_articles(articles: list[dict]) -> list:
    """
    Compares a list of parsed articles with articles stored in the database
    and returns only those not present in the database.
    """
    db_articles = Article.objects.all()

    return [article for article in articles if all(article['article_url'] != db_article.url for db_article in db_articles)]


def add_articles_in_db(analyze_articles: list[dict]) -> None:
    """
    Adds parsed articles and their authors to the database,
    ensuring no duplicates are created.
    """

    for article_data in analyze_articles:
        author_data = {
            "name": article_data["author_name"],
            "profile_url": article_data["author_profile_url"]
        }

        author, created = Author.objects.get_or_create(**author_data)

        if not created:
            print(f"[INFO]: Author '{author.name}' already exists in db.")

        article = Article(
            header=article_data["article_header"],
            content=article_data["article_content"],
            posted_at=article_data["article_post_datetime"],
            url=article_data["article_url"],
            author=author
        )

        article.save()
