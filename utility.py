import re
import validators


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


def add_manga_to_list():
    pass


if __name__ == "__main__":
    print(
        check_manga_url_validity(
            "https://github.com/jfpiedad/manga-checker#manga-checker"
        )
    )
