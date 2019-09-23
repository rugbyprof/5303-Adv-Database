#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys


urls = [
"https://www.quackit.com/mongodb/tutorial/how_to_access_mongodb.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_create_a_database.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_create_a_collection.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_create_a_document.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_query_a_collection.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_projection_queries.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_limit_query_results.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_sort_query_results.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_create_a_relationship.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_update_a_document.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_export_data.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_delete_a_document.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_drop_a_collection.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_import_data.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_create_a_backup.cfm",
"https://www.quackit.com/mongodb/tutorial/mongodb_drop_a_database.cfm"]

print(urls)
contents = []
for url in urls:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    a = soup.find('article')

    contents.append(a.text)


tut = ''.join(contents)

f = open("tutorial.md","w")

f.write(tut)

