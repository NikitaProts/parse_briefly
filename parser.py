import requests
import json
from bs4 import BeautifulSoup as BS


def request_and_bs4(url):

    r = requests.get(url)
    html = BS(r.content, 'html.parser')

    return html



def fill_authors_list(url, url_request):
    """  Функция заполнения массива с ссылками на авторов  """
    authors_links = []
    html = request_and_bs4(url_request)
    surname_alphabet = html.select(".alphabetic-index > .letter")

    for letter in surname_alphabet:
        all_authors = letter.find_all("a")
        for a in all_authors:
            authors_links.append(url + a.get("href"))

    return authors_links

def fill_authors_works_list(url, authors_list):
    """  Функция заполнения массива с ссылками на работы авторов  """
    works_links = []
    c = 0

    for author in authors_list:

        c+=1
        print(f"{c} / {len(authors_list)} \n")

        author_html = request_and_bs4(author)
        if "surnames" in author.split("/"):
            author_works = author_html.select(".author .works")

        elif author_html.find("div", class_="w-set"):
            author_works = author_html.select(".author_works") 

        else:
            author_works = author_html.select(".author_works .w-featured")
        
        if len(author_works) == 0:
            try:
                author_name = author_html.find("span", class_="author_name normal").text # имя автора
                print(f"У автора {author_name} {author} нет работ \n")
            except:
                pass
        for work in author_works:
            for work_link in work.find_all("a"):
                works_links.append(url + work_link.get("href"))
                print(url + work_link.get("href"))


    return works_links

def collect_data(works_links):
    """  Функция сбора информации с страницы произведения (работы автора) """
    data_list = []
    c = 0 

    for work in works_links:

        print(work)
        c += 1
        print(f"{c} / {len(works_links)}")

        work_html = request_and_bs4(work)

        author_name = work_html.find("div", class_="breadcrumb__name").text # имя автора
        book_name = work_html.find("span", class_="main").text # название книги
        url = work
        text = work_html.find("div", {"id": "text"}).text # текст книги

        data = {
                "author" : author_name,
                "book" : book_name,
                "text" : text,
                "url" : url
                }
        data_list.append(data)

    return data_list

def save(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)
        
        

def start():

    url = "https://briefly.ru"

    authors_url = url + "/authors/"
    authors_list = fill_authors_list(url, authors_url)

    works_list = fill_authors_works_list(url, authors_list)

    data_list = collect_data(works_list)

    save("briefly_25_06.json", data_list)



if __name__ == "__main__":
    start()