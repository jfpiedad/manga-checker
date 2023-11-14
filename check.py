import re
import asyncio
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
from tinydb import TinyDB
from tqdm.asyncio import tqdm_asyncio


async def check_new_chapters():
    """
    Checks if there are new manga chapters available.
    """
    last_read_chapter = 1
    url = 2
    mangas_info = [info for info in get_manga_info()]

    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession() as session:
        tasks_set_1 = [
            fetch_manga_data(manga[last_read_chapter], manga[url], session, timeout)
            for manga in mangas_info
        ]

        results_set_1 = await tqdm_asyncio.gather(
            *tasks_set_1, desc="Retrieving Manga Information", ncols=100
        )

    for manga, total in zip(mangas_info, results_set_1):
        if total == -1:
            print(f"{manga[0]} : Timeout")
        elif total != 0:
            print(f"{manga[0]} : {total} new chapters")

    if not any(results_set_1):
        print("There Are No New Chapters At The Moment.")


async def fetch_manga_data(last_read_chapter, manga_url, session, timeout):
    """
    Fetches the HTML data of the website.
    """
    try:
        async with session.get(manga_url, timeout=timeout) as response:
            manga_data = await response.text()
    except TimeoutError:
        return -1

    return parse_data(last_read_chapter, manga_url, manga_data)


def parse_data(last_read_chapter, manga_url, html_data):
    """
    Parse the HTML data using Beautiful Soup.
    """
    valid_domains = ["chapmanganato", "manganato", "immortalupdates", "culturedworks"]

    classification = classify_manga_url(manga_url)

    if classification not in valid_domains:
        return -1

    soup = BeautifulSoup(html_data, "html.parser")

    if classification in ["manganato", "chapmanganato"]:
        return parse_similar_data(
            soup, last_read_chapter=last_read_chapter, ul_class="row-content-chapter"
        )
    elif classification == "immortalupdates":
        return parse_similar_data(
            soup, last_read_chapter=last_read_chapter, ul_class="version-chap"
        )
    elif classification == "culturedworks":
        chapters_section = soup.find("div", class_="eplister")
        list_of_chapters = chapters_section.find_all("span", class_="chapternum")

    return count_new_chapters(last_read_chapter, list_of_chapters)


def parse_similar_data(soup, **kwargs):
    """
    Parse HTML Data with similar formats.\n
    Created this function to reduce boilerplate code.
    """
    chapters_section = soup.find("ul", class_=kwargs["ul_class"])
    list_of_chapters = chapters_section.find_all("a")

    return count_new_chapters(kwargs["last_read_chapter"], list_of_chapters)


def classify_manga_url(manga_url):
    """
    Classifies different manga websites for parsing data.\n
    Websites have different format, so it is classified to
    parse according to the classification.\n
    """
    parsed_manga_url = urlparse(manga_url)
    domain = parsed_manga_url.netloc

    parsed_manga_url_name = domain.split(".")[0]

    return parsed_manga_url_name.strip()


def count_new_chapters(last_read_chapter, list_of_chapters):
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


def get_manga_info():
    """
    Retrieves all manga info.
    """
    with TinyDB("mangas.json") as db:
        mangas_arr = []
        try:
            for entry in db.all():
                mangas_arr.append(
                    [entry["title"], entry["last_read_chapter"], entry["url"]]
                )
        except Exception as e:
            return f"An error occurred when retrieving the manga title. {e}"

    return mangas_arr


if __name__ == "__main__":
    asyncio.run(check_new_chapters())
