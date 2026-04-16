from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 5):
    response = client.search(query=query, max_results=max_results)

    results = []
    for r in response["results"]:
        results.append({
            "title": r["title"],
            "url": r["url"],
            "snippet": r["content"]
        })

    return results