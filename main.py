import argparse
import asyncio

from check import check_new_chapters
from utility import check_chapter_number_validity

parser = argparse.ArgumentParser(description="Check New Manga Chapters")
subparser = parser.add_subparsers(title="commands", dest="command")

check_parser = subparser.add_parser("check", help="check for new chapters")
add_parser = subparser.add_parser("add", help="Add new manga to the list")
update_parser = subparser.add_parser("update", help="update last read chapters")

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == "check":
        try:
            asyncio.run(check_new_chapters())
        except Exception as e:
            print(f"There was an error: {e}")
    elif args.command == "add":
        """
        ISUD PANI NAKOG FUNCTION PARA DI GUBOT OG PARA MABUHATAN OG TESTS
        """
        try:
            # while True:
            #     manga_title = input("Manga Title: ")

            #     if manga_title == "":
            #         print("Title cannot be empty or null")
            #         continue
            #     else:
            #         break
            while True:
                last_read_chapter = input("Last Chapter Read: ")

                valid = check_chapter_number_validity(last_read_chapter)

                if not valid:
                    print("Please enter a valid number")
                    continue

                validation_only_number = float(last_read_chapter.replace("-", ".", 1))
                if validation_only_number < 0 or validation_only_number > 1000:
                    print("Chapter number must not be negative or greater than 1000")

                break

        except KeyboardInterrupt:
            print("Adding manga is cancelled. Ok bye!")
    elif args.command == "update":
        pass
