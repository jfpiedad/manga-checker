import re

from tinydb import TinyDB, Query

import utility


def add_manga():
    try:
        manga_info = manga_info_inputs(1)
        insert_manga_in_db(manga_info)

        print("Manga successfully added to the list!")
    except KeyboardInterrupt:
        print("\nAdding manga is cancelled.")


def update_manga():
    try:
        manga_info = manga_info_inputs(2)
        keys_arr = []
        for key, value in manga_info.items():
            if value == "":
                keys_arr.append(key)

        for key in keys_arr:
            manga_info.pop(key)

        update_manga_in_db(manga_info)

        print("Manga successfully updated to the list!")
    except KeyboardInterrupt:
        print("\nUpdating manga is cancelled.")


def insert_manga_in_db(manga_info):
    with TinyDB("mangas.json", indent=4, separators=(",", ": ")) as db:
        db.insert(manga_info)


def update_manga_in_db(manga_info):
    manga_regex = utility.manga_title_regex_matcher(manga_info["title"])
    Manga = Query()
    with TinyDB("mangas.json", indent=4, separators=(",", ": ")) as db:
        db.update(manga_info, Manga.title.matches(manga_regex, re.IGNORECASE))


def manga_info_inputs(operation):
    """
    Ask user input for manga information.

    :param int operation: 1 = add; 2 = update
    """
    last_read_chapter = ""
    manga_url = ""
    flag = 4

    while True:
        manga_title = input("Manga Title: ")

        if not utility.manga_title_validity(manga_title):
            print("Title cannot be an empty string!")
            continue

        if operation == 1:
            break

        if utility.check_manga_existence(manga_title):
            break

        print("Manga is not in the list!")

    if operation == 2:
        while True:
            try:
                print("Input Number For Update Details: (1 - 3)")
                print("1 -> last chapter read only")
                print("2 -> manga url only")
                print("3 -> both chapter and url")
                flag = int(input(("Choice: ")))

                if flag >= 1 and flag <= 3:
                    break

                print("Please enter a number between 1 and 3 inclusive")
            except ValueError:
                print("Input only accepts an integer")

    if not flag == 2:
        while True:
            last_read_chapter = input("Last Chapter Read: ")

            if utility.manga_chapter_validity(last_read_chapter):
                break

            print("Please enter a valid number between 0 and 1000!")
    if not flag == 1:
        while True:
            manga_url = input("Manga URL: ")

            if utility.manga_url_validity(manga_url):
                break

            print("Please enter a valid URL!")

    manga_info = {
        "title": manga_title.title(),
        "last_read_chapter": last_read_chapter,
        "url": manga_url,
    }

    return manga_info


if __name__ == "__main__":
    print(utility.manga_title_regex_matcher("Castle 2: Pinnacle"))
