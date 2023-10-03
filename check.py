from bs4 import BeautifulSoup
from tinydb import TinyDB
from urllib.parse import urlparse

import asyncio
import aiohttp

import re


async def check_new_chapters():
    """
    Checks if there are new manga chapters available.
    """
    last_read_chapter = 1
    url = 2
    mangas_info = [info for info in get_manga_info()]

    tasks = []

    for manga in mangas_info:
        html_data = await fetch_manga_data(manga[url])
        task = asyncio.create_task(
            parse_data(html_data, manga[last_read_chapter], manga[url])
        )
        tasks.append(task)

    # html_data = await fetch_manga_data(
    #     "https://immortalupdates.com/manga/i-became-an-evolving-space-monster/"
    # )
    # task = asyncio.create_task(
    #     parse_data(
    #         html_data,
    #         "14",
    #         "https://immortalupdates.com/manga/i-became-an-evolving-space-monster/",
    #     )
    # )
    # tasks.append(task)

    results = await asyncio.gather(*tasks)

    for manga, total in zip(mangas_info, results):
        if total != 0:
            print(f"{manga[0]} : {total} new chapters")

    if not any(results):
        print("There Are No New Chapters At The Moment.")


async def fetch_manga_data(manga_url):
    """
    Fetches the HTML of the website.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(manga_url) as response:
            return await response.text()


async def parse_data(html_data, last_read_chapter, manga_url):
    """
    Parse the HTML data using Beautiful Soup.
    """
    classification = classify_manga_url(manga_url)

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
    chapters_section = soup.find("ul", class_=kwargs["ul_class"])
    list_of_chapters = chapters_section.find_all("a")

    count = 0
    for chapter in list_of_chapters:
        parsed_chapter = chapter.text.lower().strip()
        try:
            chapter_number = (
                re.search(r"chapter\s+\d+([.-]\d+)?", parsed_chapter, re.IGNORECASE)
                .group(0)
                .split(" ")[1]
            )
            if chapter_number != kwargs["last_read_chapter"]:
                count += 1
            elif chapter_number == kwargs["last_read_chapter"]:
                break
        except IndexError:
            continue
        except AttributeError:
            continue

    return count


def classify_manga_url(manga_url):
    """
    Classifies different manga websites for parsing data.\n
    Websites have different format, so it is classified to
    parse according to the classification.
    """
    parsed_manga_url = urlparse(manga_url)
    domain = parsed_manga_url.netloc

    parsed_manga_url_name = domain.split(".")[0]

    return parsed_manga_url_name.strip()


def get_manga_info():
    """
    Retrieves all manga info.\n
    Title and url are extracted.
    """
    with TinyDB("mangas.json") as db:
        titles_arr = []
        try:
            for entry in db.all():
                titles_arr.append(
                    [entry["title"], entry["last_read_chapter"], entry["url"]]
                )
        except Exception as e:
            return f"An error occurred when retrieving the manga title. {e}"

    return titles_arr


if __name__ == "__main__":
    asyncio.run(check_new_chapters())
