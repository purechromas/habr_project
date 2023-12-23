import asyncio
from celery import shared_task

from .services import add_articles_in_db, analyze_articles
from .async_parser import (
    fetch_five_by_five_articles_data,
    fetch_habr_page_articles_data,
    parse_habr_articles_data,
    parse_habr_articles_url
)


@shared_task
def run_habr_parser() -> None:
    """
    Celery task to run the Habr parser, collect, parse,
    and save articles to the database.
    """
    url = "https://habr.com/ru/feed/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    habr_page_articles_data = fetch_habr_page_articles_data(url, headers)
    habr_articles_urls = parse_habr_articles_url(habr_page_articles_data)
    loop = asyncio.get_event_loop()
    articles_data = loop.run_until_complete(
        fetch_five_by_five_articles_data(habr_articles_urls)
    )
    articles = parse_habr_articles_data(articles_data=articles_data)
    analyzed_articles = analyze_articles(articles)
    add_articles_in_db(analyzed_articles)
