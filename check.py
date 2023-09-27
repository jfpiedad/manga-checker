from bs4 import BeautifulSoup
from tinydb import TinyDB, Query


def check_new_chapters():
    print(get_manga_titles())


def get_manga_titles():
    with TinyDB("mangas.json") as db:
        titles_arr = []
        for entry in db.all():
            titles_arr.append([entry["title"], entry["url"]])

    return titles_arr


if __name__ == "__main__":
    check_new_chapters()
