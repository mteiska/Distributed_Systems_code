import helper
from collections import deque
def shortest_search(start, end):
    
    
    path = {}
    path[start] = [start]
    Q = deque([start]) #sort of linked list

    while len(Q) != 0:
        page = Q.popleft()
        
        links = helper.fetch_links(page) #Gets links

        for link in links:
            if link == end:
                return path[page] + [link]

            if (link not in path) and (link != page):
                path[link] = path[page] + [link]
                Q.append(link)
    print(Q)

    return None



    