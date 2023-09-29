import re


def check_chapter_number_validity(string):
    integer_pattern = r"^\d+$"
    special_pattern = r"\d+([.-]\d+)+"

    integer_pattern_validation = bool(re.match(integer_pattern, string, re.IGNORECASE))
    special_pattern_validation = bool(re.match(special_pattern, string, re.IGNORECASE))

    return integer_pattern_validation or special_pattern_validation


if __name__ == "__main__":
    print(check_chapter_number_validity("173"))
