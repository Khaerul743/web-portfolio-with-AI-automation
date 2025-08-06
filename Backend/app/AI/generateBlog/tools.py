from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from tavily import TavilyClient
from firecrawl import FirecrawlApp
import requests
import os
import textwrap
import arxiv
from dotenv import load_dotenv
load_dotenv()

# load_dotenv()  # Load your SERPER_API_KEY, TAVILY_API_KEY, etc.

class SearchTools:
    def __init__(self):
        self.serper_api_key = os.environ.get("SERPER_API_KEY")  # dari .env
        self.serper_url = "https://google.serper.dev/scholar"  # endpoint tetap
        self.headers = {
            "X-API-KEY": "33eb8016586a1703a087e0457251baf45556e5ec",
            "Content-Type": "application/json"
        }
        self.gnews_api_key = os.getenv("GNEWS_API_KEY")

    def serper_search(self, query: str):
        """Manual call ke Serper (bisa search, scholar, news, dll)"""
        payload = {"q": query}
        try:
            res = requests.post(self.serper_url, json=payload, headers=self.headers)
            res.raise_for_status()
            data = []
            for item in res.json()["organic"][:4]:
                try:
                    scholar = {
                        "title":item["title"],
                        "publicationInfo":item["publicationInfo"],
                        "snippet":item["snippet"],
                        "year":item["year"],
                        "pdfUrl":item["pdfUrl"]
                    }
                    data.append(scholar)
                except:
                    data.append({
                        "title": "kosong",
                        "publicationInfo": "kosong",
                        "snippet": "kosong",
                        "year": "kosong",
                        "pdfUrl": "kosong"
                    })
            return data

        except Exception as e:
            print(f"Terjadi kesalahan di tool serper search: {e}")
            return [{"error":str(e)}]
    
    def wikipedia_search(self, query:str):
        try:
            wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
            return WikipediaQueryRun(api_wrapper=wikipedia_wrapper).run(query)
        except Exception as e:
            print(f"Terjadi kesalahan di tool wikipedia search: {e}")
            return f"error:{str(e)}"
    
    def tavily_search(self, query:str):
        try:
            tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
            response = tavily_client.search(query=query, search_depth="basic")["results"] # atau "advanced"
            result = []

            for item in response:
                data = {
                    "url":item.get("url"),
                    "content":item.get("content"),
                }
                result.append(data)
            
            return result
        except Exception as e:
            print(f"Terjadi kesalahan di tool tavily search: {e}")
            return [{"error":str(e)}]

    def gnews_search(self, query:str):
        try:
            res = requests.get(url=f"https://gnews.io/api/v4/search/?q={query}&lang=en&country=us&max=1&apikey={self.gnews_api_key}")
            print(res.json())
            res.raise_for_status()
            data = []
            for item in res.json()["articles"]:
                news = {
                    "title":item["title"],
                    "description":item["description"],
                    "content":item["content"],
                    "url":item["url"],
                    "publishedAt":item["publishedAt"]
                }
                data.append(news)
            return data
        except Exception as e:
            print(f"Terjadi kesalahan di tool gnews_search: {e}")
            return [{"error":str(e)}]

    def scrape_with_firecrawl(self,url:str):
        # Inisialisasi Firecrawl
        try:
            app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))
            scrape_result = app.scrape_url(url, formats=['markdown'])
            wrapped = textwrap.fill(scrape_result.markdown, width=100)
            return wrapped
        except Exception as e:
            print(f"Terjadi kesalahan di tool firecrawl: {e}")
            return [{"error":str(e)}]
    
    def search_arxiv(self,keyword: str) -> str:
        search = arxiv.Search(query=keyword, max_results=2, sort_by=arxiv.SortCriterion.Relevance)
        results = []
        for result in search.results():
            results.append(f"{result.title}\n{result.summary}")
        return "\n\n".join(results)

    def unsplash_picture(self, keyword:str) :
        try:
            url = f"https://api.unsplash.com/search/photos?page=1&query={keyword}&client_id={os.environ.get('UNSPLASH_API_KEY')}"
            result = requests.get(url).json()
            data = []
            for item in result["results"]:
                if item["urls"]:
                    data.append(item["urls"])
                    break

            return f"{data[0]['raw']}&w=500&h=300&fit=crop"
        except:
            return "Thumbnail"

if __name__ == "__main__":
    tool = SearchTools()
    print(tool.unsplash_picture("office"))