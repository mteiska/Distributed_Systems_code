import requests

#Helper for searching through nodes

WIKIPEDIA_URL = 'https://en.wikipedia.org/w/api.php'



def fetch_wikipedia_pages_info(page_ids):
  
  page_route_info = {}
  pages_index = 0
  #Query wikipedia
  while pages_index < len(page_ids):
    end_page_index = min(pages_index + 50, len(page_ids))

    query_params = {
        'action': 'query',
        'format': 'json',
        'pageids': '|'.join(page_ids[pages_index:end_page_index]),
        'prop': 'info|pageimages|pageterms',
        'inprop': 'url|displaytitle',
        'pllimit': 500,
        'wbptterms': 'description',
    }

    pages_index = end_page_index

    headers = {
        'User-Agent': 'mteiska/1.0 ; mika123450@hotmail.com',
    }

    request = requests.get(WIKIPEDIA_URL, params=query_params, headers=headers)

    result = request.json().get('query', {}).get('pages')

    print(result)



def fetch_links(source_title):
    page_titles = source_title
    page_ids = []
 
    
    URL = 'https://en.wikipedia.org/w/api.php'
    PARAMS = {
    "action": "query",
    "format": "json",
     "titles": source_title,
     "pllimit": 500,
     "prop": "links"
 }
    Session = requests.Session()
    Result = Session.get(url=URL, params=PARAMS)
    DATA = Result.json()

    PAGES = DATA["query"]["pages"]

    for key, value in PAGES.items(): 
        for link in value["links"]:
            page_ids.append(link["title"])
    return page_ids
	

