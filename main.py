import argparse
import asyncio
import time

from check import check_new_chapters
from commands import add_manga, update_manga


parser = argparse.ArgumentParser(description="Check New Manga Chapters")
subparser = parser.add_subparsers(title="commands", dest="command")

check_parser = subparser.add_parser("check", help="check for new chapters")
add_parser = subparser.add_parser("add", help="Add new manga to the list")
update_parser = subparser.add_parser("update", help="update last read chapters or url")

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == "check":
        start = time.time()
        asyncio.run(check_new_chapters())
        end = time.time() - start
        print(f"Time To Finish: {end: .2f}s")
    elif args.command == "add":
        add_manga()
    elif args.command == "update":
        update_manga()
