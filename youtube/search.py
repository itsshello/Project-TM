from youtubesearchpython import VideosSearch

def search_youtube(query):
    videos_search = VideosSearch(query, limit=10)
    
    results = videos_search.result()
    
    for video in results['result']:
        title = video['title']
        link = video['link']
        print(f"Title: {title}")
        print(f"Link: {link}\n")

if __name__ == '__main__':
    search_query = input("Enter search query: ")
    search_youtube(search_query)
