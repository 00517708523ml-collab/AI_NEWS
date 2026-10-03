import os
import time

from dotenv import load_dotenv
from exa_py import Exa
from firecrawl import Firecrawl
from tavily import TavilyClient


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# API KEYS
# ============================================================

EXA_API_KEY = os.getenv("EXA_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# ============================================================
# CHECK API KEYS
# ============================================================

if not EXA_API_KEY:
    raise ValueError("EXA_API_KEY is missing in .env")

if not FIRECRAWL_API_KEY:
    raise ValueError("FIRECRAWL_API_KEY is missing in .env")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing in .env")


# ============================================================
# INITIALIZE CLIENTS
# ============================================================

exa = Exa(
    api_key=EXA_API_KEY
)

firecrawl = Firecrawl(
    api_key=FIRECRAWL_API_KEY
)

tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)


# ============================================================
# AI NEWS URLS
# ============================================================

urls_to_scrape = [

    # --------------------------------------------------------
    # Official AI Companies
    # --------------------------------------------------------

    "https://openai.com/news/",
    "https://deepmind.google/discover/blog/",
    "https://www.anthropic.com/news",
    "https://blogs.nvidia.com/blog/category/deep-learning/",
    "https://ai.meta.com/blog/",
    "https://blogs.microsoft.com/ai/",

    # --------------------------------------------------------
    # Chinese / Asian AI
    # --------------------------------------------------------

    "https://qwen.ai/",
    "https://www.deepseek.com/",
    "https://www.moonshot.cn/",
    "https://www.minimaxi.com/",
    "https://z.ai/",

    # --------------------------------------------------------
    # AI News
    # --------------------------------------------------------

    "https://techcrunch.com/category/artificial-intelligence/",
    "https://www.theverge.com/ai-artificial-intelligence",
    "https://venturebeat.com/category/ai/",
    "https://the-decoder.com/",
    "https://www.marktechpost.com/",

    # --------------------------------------------------------
    # Research / Open Source AI
    # --------------------------------------------------------

    "https://huggingface.co/blog",
    "https://huggingface.co/papers",
    "https://arxiv.org/list/cs.AI/recent",
    "https://arxiv.org/list/cs.LG/recent",
]





# ============================================================
# SCRAPE AI NEWS
# ============================================================

def dashboard():

    all_news = []

    print("\n" + "=" * 70)
    print("STARTING AI NEWS STREAM")
    print("=" * 70)

    for index, url in enumerate(urls_to_scrape, start=1):

        print(f"\n[{index}/{len(urls_to_scrape)}] Scraping:")
        print(url)

        try:

            response = firecrawl.scrape(
                url,
                formats=["markdown"]
            )

            markdown = response.markdown

            if markdown:

                news_item = {
                    "source": url,
                    "content": markdown
                }

                all_news.append(news_item)

                print("SUCCESS")

                # IMPORTANT:
                # Send current data to frontend immediately
                yield all_news

            else:

                print("No markdown content found.")

        except Exception as error:

            print(f"ERROR: {error}")

        if index < len(urls_to_scrape):

            print("Waiting 7 seconds...")

            time.sleep(7)

    print("\n" + "=" * 70)
    print("SCRAPING COMPLETED")
    print(f"Successful sources: {len(all_news)}")
    print("=" * 70)

# ============================================================
# SEARCH USING EXA + TAVILY
# ============================================================

def chat(query):

    print(f"\nSearching for: {query}")

    # --------------------------------------------------------
    # EXA
    # --------------------------------------------------------

    exa_results = exa.search(
        query,
        type="auto",
        contents={
            "highlights": True
        }
    )

    # --------------------------------------------------------
    # TAVILY
    # --------------------------------------------------------

    tavily_results = tavily.search(
        query=query,
        max_results=5
    )

    return exa_results, tavily_results


# ============================================================
# FUNCTION USED BY FRONTEND
# ============================================================

def ask_query(user_query):

    return chat(user_query)