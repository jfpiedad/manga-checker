import argparse

from check import check_new_chapters

parser = argparse.ArgumentParser(description="Check New Manga Chapters")
subparser = parser.add_subparsers(title="commands", dest="command")

check_parser = subparser.add_parser("check", help="check for new chapters")

add_parser = subparser.add_parser("add", help="Add new manga to the list")
add_parser.add_argument("add_title", type=str, help="title of the manga to be added")

update_parser = subparser.add_parser("update", help="update last read chapters")
update_parser.add_argument(
    "update_title", type=str, help="title of the manga to be updated"
)

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == "check":
        check_new_chapters()
    elif args.command == "add":
        pass
    elif args.command == "update":
        pass
