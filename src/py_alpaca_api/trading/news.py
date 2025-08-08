import json
import logging
import textwrap
import time
import math
from typing import Dict, List
import pendulum
from bs4 import BeautifulSoup as bs
import yfinance as yf
from py_alpaca_api.http.requests import Requests





logger = logging.getLogger("yfinance")
logger.disabled = True
logger.propagate = False


START_DATE = pendulum.now().subtract(days=14).to_date_string()
END_DATE = pendulum.now().to_date_string()


class News:
    def __init__(self, headers: Dict[str, str]) -> None:
        self.news_url = "https://data.alpaca.markets/v1beta1/news"
        self.headers = headers

    @staticmethod
    def strip_html(content: str):
        """
        Removes HTML tags and returns the stripped content.

        Args:
            content (str): The HTML content to be stripped.

        Returns:
            str: The stripped content without HTML tags.
        """
        soup = bs(content, "html.parser")
        for data in soup(["style", "script"]):
            data.decompose()
        return " ".join(soup.stripped_strings)

    @staticmethod
    def scrape_article(url: str) -> str:
        """
        Scrapes the article text from the given URL.

        Args:
            url (str): The URL of the article.

        Returns:
            str: The text content of the article, or None if the article body is not found.
        """
        time.sleep(1)  # Sleep for 1 second to avoid rate limiting
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "referer": "https://www.google.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
                like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44",
        }
        request = Requests().request(method="GET", url=url, headers=headers)
        soup = bs(request.text, "html.parser")
        return (
            soup.find(class_="caas-body").text
            if soup.find(class_="caas-body")
            else None
        )

    ########################################################
    # ////////////  static _truncate method  //////////////#
    ########################################################
    @staticmethod
    def truncate(text: str, length: int) -> str:
        """
        Truncates a given text to a specified length.

        Args:
            text (str): The text to be truncated.
            length (int): The maximum length of the truncated text.

        Returns:
            str: The truncated text.
        """
        return (
            textwrap.shorten(text, length, placeholder="")
            if len(text) > length
            else text
        )

    def get_news(self, symbol: str, limit: int = 6) -> List[Dict[str, str]]:
        """
        Retrieves news articles related to a given symbol from Benzinga and Yahoo Finance.

        Note: Yahoo Finance has implemented anti-scraping measures that prevent fetching 
        full article content. Yahoo news will include title, URL, publish date, and 
        summary/description when available, but not full article text.

        Args:
            symbol (str): The symbol for which to retrieve news articles.
            limit (int, optional): The maximum number of news articles to retrieve. Defaults to 6.

        Returns:
            list: A list of news articles, sorted by publish date in descending order.
        """
        benzinga_news = self._get_benzinga_news(symbol=symbol, limit=limit)
        yahoo_news = self._get_yahoo_news(
            symbol=symbol, limit=(limit - len(benzinga_news[: (math.floor(limit / 2))])), scrape_content=False
        )

        news = benzinga_news[: (math.floor(limit / 2))] + yahoo_news

        sorted_news = sorted(
            news, key=lambda x: pendulum.parse(x["publish_date"]), reverse=True
        )

        return sorted_news[:limit]

    def _get_yahoo_news(self, symbol: str, limit: int = 6, scrape_content: bool = False) -> List[Dict[str, str]]:
        """
        Retrieves the latest news articles related to a given symbol from Yahoo Finance.

        Args:
            symbol (str): The symbol for which to retrieve news articles.
            limit (int, optional): The maximum number of news articles to retrieve. Defaults to 6.
            scrape_content (bool, optional): Whether to attempt scraping full article content. 
                                            Defaults to False due to Yahoo's anti-scraping measures.

        Returns:
            list: A list of dictionaries containing the news article details, including title, URL, source, 
                  content (if available), publish date, and symbol.
        """
        ticker = yf.Ticker(symbol)
        news_response = ticker.news

        yahoo_news = []
        news_count = 0
        for news in news_response[:limit]:  # Limit the iteration
            try:
                news_content = news.get('content', {})
                
                # Extract the summary/description if available
                content = None
                if scrape_content:
                    # Only attempt scraping if explicitly requested
                    try:
                        scraped_article = self.scrape_article(news_content.get("canonicalUrl", {}).get('url', ''))
                        if scraped_article:
                            content = self.truncate(self.strip_html(scraped_article), 8000)
                    except Exception as scrape_error:
                        logging.debug(f"Could not scrape article content: {scrape_error}")
                
                # Use the summary from the API if scraping failed or wasn't attempted
                if not content:
                    # Try to get summary from the news data itself
                    summary = news_content.get('summary', '')
                    if not summary:
                        # Some news items have description instead of summary
                        summary = news.get('summary', '')
                    content = self.truncate(summary, 8000) if summary else None
                
                yahoo_news.append(
                    {
                        "title": news_content.get("title", news.get("title", "No title")),
                        "url": news_content.get("canonicalUrl", {}).get('url', news.get("link", "")),
                        "source": "yahoo",
                        "content": content,
                        "publish_date": pendulum.from_timestamp(
                            news_content.get("pubDate", news.get("providerPublishTime", 0))
                        ).to_datetime_string() if news_content.get("pubDate") or news.get("providerPublishTime") else pendulum.now().to_datetime_string(),
                        "symbol": symbol,
                    }
                )
                news_count += 1
                
            except Exception as e:
                logging.error(f"Error processing Yahoo news item: {e}")
                continue
                
            if news_count >= limit:
                break

        return yahoo_news

    def _get_benzinga_news(
        self,
        symbol: str,
        start_date: str = START_DATE,
        end_date: str = END_DATE,
        include_content: bool = True,
        exclude_contentless: bool = True,
        limit: int = 10,
    ) -> List[Dict[str, str]]:
        """
        Retrieves Benzinga news articles for a given symbol and date range.

        Args:
            symbol (str): The symbol for which to retrieve news articles.
            start_date (str, optional): The start date of the news articles. Defaults to START_DATE.
            end_date (str, optional): The end date of the news articles. Defaults to END_DATE.
            include_content (bool, optional): Whether to include the content of the news articles. Defaults to True.
            exclude_contentless (bool, optional): Whether to exclude news articles with no content. Defaults to True.
            limit (int, optional): The maximum number of news articles to retrieve. Defaults to 10.

        Returns:
            list: A list of dictionaries representing the retrieved news articles. Each dictionary contains the following keys:
                - "title": The title of the news article.
                - "url": The URL of the news article.
                - "source": The source of the news article (in this case, "benzinga").
                - "content": The content of the news article, or None if there is no content.
                - "publish_date": The publishing date of the news article.
                - "symbol": The symbol associated with the news article.
        """
        url = f"{self.news_url}"
        params = {
            "symbols": symbol,
            "start": start_date,
            "end": end_date,
            "include_content": include_content,
            "exclude_contentless": exclude_contentless,
            "limit": limit,
        }
        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        benzinga_news = []
        for news in response["news"]:
            benzinga_news.append(
                {
                    "title": news["headline"],
                    "url": news["url"],
                    "source": "benzinga",
                    "content": self.strip_html(news["content"])
                    if news["content"]
                    else None,
                    "publish_date": pendulum.parse(
                        news["created_at"]
                    ).to_datetime_string(),
                    "symbol": symbol,
                }
            )

        return benzinga_news
