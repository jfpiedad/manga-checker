from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

import asyncio
import aiohttp


async def check_new_chapters():
    titles, urls = 0, 1
    mangas = [[manga[titles], manga[urls]] for manga in get_manga_titles()]

    tasks = []

    # for manga in mangas:
    #     for url in manga[urls]:
    #         data = await fetch_manga_data(url)
    #         task = asyncio.create_task(parse_data(data))
    #         tasks.append(task)
    html_data = await fetch_manga_data("https://manganato.com/manga-uh998064")
    task = asyncio.create_task(parse_data(html_data))
    tasks.append(task)

    results = await asyncio.gather(*tasks)

    for manga, total in zip(mangas, results):
        if total != 0:
            print(f"{manga[0]} : {total} new chapters")


async def fetch_manga_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_data(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    manga_title = soup.find("div", class_="story-info-right").find("h1")

    chapters_section = soup.find("ul", class_="row-content-chapter")
    list_of_chapters = chapters_section.find_all("a")

    last_read_chapter = retrieve_last_read_chapter(manga_title.text)

    count = 0
    for chapter in list_of_chapters:
        chapter_number = int(chapter.text.split(" ")[1])
        if chapter_number != last_read_chapter:
            count += 1
        elif chapter_number == last_read_chapter:
            break

    return count


def retrieve_last_read_chapter(title):
    Manga = Query()
    with TinyDB("mangas.json") as db:
        try:
            manga = db.get(Manga.title == title)
            return int(manga["last_read_chapter"])
        except Exception as e:
            return f"An error ocurred when retrieving the last read chapter. {e}"


def get_manga_titles():
    with TinyDB("mangas.json") as db:
        titles_arr = []
        for entry in db.all():
            titles_arr.append([entry["title"], entry["url"]])

    return titles_arr


if __name__ == "__main__":
    asyncio.run(check_new_chapters())
