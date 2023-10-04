import re

import validators
from tinydb import TinyDB, Query


def check_manga_title_validity(manga_title):
    if manga_title:
        return True

    return False


def check_chapter_number_validity(chapter_number):
    integer_pattern = r"^\d+$"
    special_pattern = r"\d+([.-]\d+)+"

    integer_pattern_validation = bool(
        re.match(integer_pattern, chapter_number, re.IGNORECASE)
    )
    special_pattern_validation = bool(
        re.match(special_pattern, chapter_number, re.IGNORECASE)
    )

    valid = integer_pattern_validation or special_pattern_validation

    if not valid:
        return False

    valid_float_integer = float(chapter_number.replace("-", ".", 1))
    if valid_float_integer > 0 and valid_float_integer < 1000:
        return True

    return False


def check_manga_url_validity(manga_url):
    is_valid = validators.url(manga_url)

    if is_valid:
        return True

    return False


def add_manga_in_list(manga_info):
    with TinyDB("mangas.json", indent=4, separators=(",", ": ")) as db:
        db.insert(manga_info)


def update_manga_in_list(manga_info):
    manga_regex = manga_title_regex_matcher(manga_info["title"])
    Manga = Query()
    with TinyDB("mangas.json", indent=4, separators=(",", ": ")) as db:
        db.update(
            {"last_read_chapter": manga_info["last_chapter"]},
            Manga.title.matches(manga_regex, re.IGNORECASE),
        )


def check_manga_in_list(manga_title):
    manga_regex = manga_title_regex_matcher(manga_title)
    Manga = Query()

    with TinyDB("mangas.json") as db:
        is_present = db.contains(Manga.title.matches(manga_regex, re.IGNORECASE))

    return is_present


def manga_title_regex_matcher(manga_title):
    regex = r""

    for manga in manga_title.split():
        regex += rf"{re.escape(manga)}\s"

    regex = regex.rstrip("\\s")

    return regex


if __name__ == "__main__":
    print(check_manga_in_list("I became an evolving space monster"))
