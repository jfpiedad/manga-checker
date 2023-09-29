from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from urllib.parse import urlparse

import asyncio
import aiohttp

import re


async def check_new_chapters():
    """
    Checks if there are new manga chapters available.
    """
    url = 1
    mangas = [entry for entry in get_manga_titles()]

    tasks = []

    for manga in mangas:
        html_data = await fetch_manga_data(manga[url])
        task = asyncio.create_task(parse_data(html_data, manga[url]))
        tasks.append(task)

    # html_data = await fetch_manga_data(
    #     "https://immortalupdates.com/manga/i-became-an-evolving-space-monster/"
    # )
    # task = asyncio.create_task(
    #     parse_data(
    #         html_data,
    #         "https://immortalupdates.com/manga/i-became-an-evolving-space-monster/",
    #     )
    # )
    # tasks.append(task)

    results = await asyncio.gather(*tasks)

    for manga, total in zip(mangas, results):
        if total != 0:
            print(f"{manga[0]} : {total} new chapters")

    if not any(results):
        print("There Are No New Chapters At The Moment.")


async def fetch_manga_data(url):
    """
    Fetches the HTML of the website.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_data(html_data, url):
    """
    Parse the HTML data using Beautiful Soup.
    """
    classification = classify_manga_url(url)

    soup = BeautifulSoup(html_data, "html.parser")

    if classification in ["manganato", "chapmanganato"]:
        return parse_similar_data(
            soup, div_class="story-info-right", ul_class="row-content-chapter"
        )
    elif classification == "immortalupdates":
        return parse_similar_data(soup, div_class="post-title", ul_class="version-chap")
    elif classification == "culturedworks":
        manga_title = soup.find("div", class_="info-desc").find("h1")

        chapters_section = soup.find("div", class_="eplister")
        list_of_chapters = chapters_section.find_all("span", class_="chapternum")

        last_read_chapter = get_last_read_chapter(manga_title.text)

        count = 0
        for chapter in list_of_chapters:
            parsed_chapter = chapter.text.lower().strip()
            try:
                chapter_number = (
                    re.search(r"chapter\s+\d+([.-]\d+)?", parsed_chapter)
                    .group(0)
                    .split(" ")[1]
                )
                if chapter_number != last_read_chapter:
                    count += 1
                elif chapter_number == last_read_chapter:
                    break
            except IndexError:
                continue
            except AttributeError:
                continue

        return count


def parse_similar_data(soup: BeautifulSoup, **kwargs):
    """
    Parse HTML Data with similar formats.\n
    Created this function to reduce boilerplate code.
    """
    manga_title = soup.find("div", class_=kwargs["div_class"]).find("h1")

    chapters_section = soup.find("ul", class_=kwargs["ul_class"])
    list_of_chapters = chapters_section.find_all("a")

    last_read_chapter = get_last_read_chapter(manga_title.text)

    count = 0
    for chapter in list_of_chapters:
        parsed_chapter = chapter.text.lower().strip()
        try:
            chapter_number = (
                re.search(r"chapter\s+\d+([.-]\d+)?", parsed_chapter, re.IGNORECASE)
                .group(0)
                .split(" ")[1]
            )
            if chapter_number != last_read_chapter:
                count += 1
            elif chapter_number == last_read_chapter:
                break
        except IndexError:
            continue
        except AttributeError:
            continue

    return count


def classify_manga_url(url):
    """
    Classifies different manga websites for parsing data.\n
    Websites have different format, so it is classified to
    parse according to the classification.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    parsed_url_name = domain.split(".")[0]

    return parsed_url_name.strip()


def get_last_read_chapter(title):
    """
    Retrieves last read chapter of a given title.
    """
    Manga = Query()
    with TinyDB("mangas.json") as db:
        try:
            manga = db.get(Manga.title == title.strip())
            return manga["last_read_chapter"].strip()
        except Exception as e:
            return f"An error occurred when retrieving the last read chapter. {e}"


def get_manga_titles():
    """
    Retrieves all manga info.\n
    Title and url are extracted.
    """
    with TinyDB("mangas.json") as db:
        titles_arr = []
        try:
            for entry in db.all():
                titles_arr.append([entry["title"], entry["url"]])
        except Exception as e:
            return f"An error occurred when retrieving the manga title. {e}"

    return titles_arr


if __name__ == "__main__":
    asyncio.run(check_new_chapters())
