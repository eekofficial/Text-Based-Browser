from collections import deque
import sys, os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

def correct_url(url):
    return url.count('.') >= 1

def short_url(url):
    url =  url.split('.')[0]
    if url.split('//')[0] == 'https:':
        return url.split('//')[1]
    return url

def show_page(request, stack, back=False):
    if not correct_url(request):
        return 'Error: Incorrect URL'
    else:
        if request.split('//')[0] != 'https:':
            request = 'https://' + request
        r = requests.get(request)
        soup = BeautifulSoup(r.content, 'html.parser')
        soup = soup.find_all(['p', 'a', 'ul', 'ol', 'li'])
        formatted_soup = []
        for tag in soup:
            if tag.name == 'a':
                formatted_soup.append('<{}>'.format(tag.get_text()))
            else:
                formatted_soup.append(tag.get_text())
        with open('{}/{}'.format(args[1], short_url(request)), 'w') as f:
            print(*formatted_soup, file=f)
        if not back:
            stack.append(request)
        print_with_color(formatted_soup)

def print_with_color(repr):
    for tag in repr:
        if len(tag) > 0 and tag[0] == '<' and tag[len(tag) - 1] == '>':
            print(Fore.BLUE + tag[1:len(tag) - 1], end=' ')

        else:
            print(tag, end=' ')
    print()

my_stack = deque()

init(autoreset=True)

args = sys.argv
if not os.path.exists(args[1]):
    os.mkdir(args[1])
while True:
    request = input()
    if request == 'exit':
        break
    elif request == 'back' and len(my_stack) >= 2:
        my_stack.pop()
        show_page(my_stack.pop(), my_stack, True)
    else:
        show_page(request, my_stack)




