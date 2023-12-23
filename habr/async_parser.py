import asyncio
import httpx

from bs4 import BeautifulSoup


def fetch_habr_page_articles_data(url: str, headers: dict) -> str:
    """
    Fetches the HTML content of the main page of Habr (https://habr.com)
    and returns it as a string.
    """
    try:
        response = httpx.get(url=url, headers=headers)
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        print(f"[ERROR]: Failed to send request on {url}. {e}")


def parse_habr_articles_url(habr_page_articles_data: str) -> list:
    """
    Parses the HTML content of the Habr page and extracts URLs of articles.
    """
    articles_urls = []
    data = BeautifulSoup(habr_page_articles_data, 'lxml')

    try:
        articles = data.find_all(
            "div", class_="tm-article-snippet tm-article-snippet"
        )

        for article in articles:
            article_url = "https://habr.com" + \
                article.find("a", class_="tm-title__link").get("href")
            articles_urls.append(article_url)

        return articles_urls
    except Exception as e:
        print(
            f"[ERROR]: Failed to parse data from the habr page articles. {e}")


async def fetch_five_by_five_articles_data(urls: list) -> list[str]:
    """
    Asynchronously fetches HTML content from a list of article URLs.
    """
    async with httpx.AsyncClient() as session:
        articles_data = []
        total_urls = len(urls)

        while urls:
            batch = urls[:min(5, len(urls))]
            urls = urls[len(batch):]

            batch_responses = await asyncio.gather(*[session.get(url) for url in batch])

            for response, url in zip(batch_responses, batch):
                try:
                    response.raise_for_status()
                    data = response.text
                    articles_data.append((url, data))
                except httpx.HTTPStatusError as e:
                    print(f"[ERROR]: Failed to send request. {e}")

            fetched_count = len(articles_data)
            print(
                f"[INFO]: Fetched successfully {fetched_count}/{total_urls} articles."
            )
            await asyncio.sleep(2)

    return articles_data


def parse_habr_articles_data(articles_data: list[tuple]) -> list[dict]:
    """
    Parses data from a list of tuples containing str content of Habr articles.
    """
    articles = []

    for article_number, (article_url, article) in enumerate(articles_data, 1):
        data = BeautifulSoup(article, 'lxml')

        article_info = data.find("a", class_="tm-user-info__username")
        author_name = article_info.text.strip()
        author_profile_url = "https://habr.com" + \
            data.find("a", class_="tm-user-info__username").get("href")
        article_post_datetime = data.find("time").get("datetime")
        article_header = data.find(
            "h1", class_="tm-title tm-title_h1").text
        article_content = data.find(
            "div", class_="article-formatted-body").text

        article_data = {
            "author_name": author_name,
            "author_profile_url": author_profile_url,
            "article_url": article_url,
            "article_post_datetime": article_post_datetime,
            "article_header": article_header,
            "article_content": article_content
        }

        print(
            f"[INFO]: {article_number}/{len(articles_data)} article was successfully parsed"
        )

        articles.append(article_data)

    return articles
