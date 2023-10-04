import argparse
import asyncio
import time

import utility
from check import check_new_chapters


parser = argparse.ArgumentParser(description="Check New Manga Chapters")
subparser = parser.add_subparsers(title="commands", dest="command")

check_parser = subparser.add_parser("check", help="check for new chapters")
add_parser = subparser.add_parser("add", help="Add new manga to the list")
update_parser = subparser.add_parser("update", help="update last read chapters")

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == "check":
        start = time.time()
        asyncio.run(check_new_chapters())
        end = time.time() - start
        print(f"Time To Finish: {end: .2f}s")
    elif args.command == "add":
        try:
            while True:
                manga_title = input("Manga Title: ")

                if utility.check_manga_title_validity(manga_title):
                    break

                print("Title cannot be an empty string!")
            while True:
                last_read_chapter = input("Last Chapter Read: ")

                if utility.check_chapter_number_validity(last_read_chapter):
                    break

                print("Please enter a valid number between 0 and 1000!")

            while True:
                manga_url = input("Manga Website URL: ")

                if utility.check_manga_url_validity(manga_url):
                    break

                print("Please enter a valid URL!")

            manga_info = {
                "title": manga_title,
                "last_chapter": last_read_chapter,
                "url": manga_url,
            }

            utility.add_manga_in_list(manga_info)
            print("Manga successfully added to the list!")
        except KeyboardInterrupt:
            print("\nAdding manga is cancelled.")
    elif args.command == "update":
        try:
            while True:
                manga_title = input("Manga Title: ")

                if not utility.check_manga_title_validity(manga_title):
                    print("Title cannot be an empty string!")
                    continue

                if utility.check_manga_in_list(manga_title):
                    break

                print("Manga is not in the list!")

            while True:
                last_read_chapter = input("Last Chapter Read: ")

                if utility.check_chapter_number_validity(last_read_chapter):
                    break

                print("Please enter a valid number between 0 and 1000!")

            while True:
                manga_url = input("Manga URL: ")

                if utility.check_manga_url_validity(manga_url):
                    break

                print("Please enter a valid URL!")

            manga_info = {
                "title": manga_title,
                "last_chapter": last_read_chapter,
                "url": manga_url,
            }

            utility.update_manga_in_list(manga_info)
            print("Manga successfully updated to the list!")
        except KeyboardInterrupt:
            print("\nUpdating manga is cancelled.")
