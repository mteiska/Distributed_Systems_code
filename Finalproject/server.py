import json
import time
import requests
import argparse
import helper
import database

WIKIPEDIA_URL = 'https://en.wikipedia.org/w/api.php'
def main():

    print("This a program to search shortest path between wikipedia pages.")
    source_title =input("Input source title: ")
    target_title = input("Target source title: ")
  

    
    #helper.fetch_wikipedia_pages_info(page_ids)
    try:
        path = database.shortest_search(source_title, target_title)
        print("Shortest path is", path,"With lenght of", len(path))
    except Exception as e:
        print("Error occured with a name of ", e)
        pass
main()
