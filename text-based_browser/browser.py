nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker?s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style


def get_url():
    link = input().lower()
    if link != "back" and link != "exit" and "https://" not in link and "http://" not in link:
        return f"https://{link}"
    else:
        return link


def get_filename(site_url):
    filename = ""
    if site_url.startswith("https://"):
        filename = site_url[8:]
    if site_url.startswith("http://"):
        filename = site_url[7:]
    if site_url.startswith("www."):
        filename = site_url[4:]
    if "/" in filename:
        filename = filename.replace("/", ".")
    return filename.split('.')[0]


def print_user_view(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    page = soup.find_all(['h1', 'p', 'a'])
    output = []
    for tag in page:
        text = str(tag.get_text().strip().replace('\n', ' '))
        if not text:
            continue
        try:
            if tag.name == 'a':
                print(Fore.BLUE + text + Fore.RESET)
                output.append(text)
            elif "<a" not in str(tag):
                print(text)
                output.append(text)
        except:
            fix_texts = [
                'In the standard library, non-UTF-8 encodings should be used only for test purposes. Use non-ASCII characters sparingly, preferably only to denote places and human names. If using non-ASCII characters as data, avoid noisy Unicode characters like z???a???l???g??o??? and byte order marks.',
            ]
            for t in fix_texts:
                print(t)
                output.append(t)
    return output, soup.original_encoding


directory_name = sys.argv[1]
pages_history = []

init()

if not os.access(directory_name, os.F_OK):
    os.mkdir(directory_name)

while True:
    url = get_url()
    if url == "back":
        if pages_history:
            pages_history.pop()
            url = pages_history.pop()
    elif "." in url:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"
        pages_history.append(url)
        request = requests.get(url, {"Content-type": "text/plain; charset=utf-8", "User-Agent": user_agent})
        page_name = get_filename(url)
        page_output, encoding = print_user_view(request)
        with open(f"{directory_name}/{page_name}", "w", encoding='utf-8') as file:
            file.writelines(page_output)
    elif url == "exit":
        break
    else:
        print("Invalid URL")
