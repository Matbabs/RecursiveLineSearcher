import os
import re
import argparse

SRC_FOLDER = "."
ELEMENTS = ["d00a070e20fd4f298349810e6b26"]
PATTERN = re.compile(rf'"controller-id": "({"|".join(ELEMENTS)})"')
founded_results = {}

parser = argparse.ArgumentParser(description="Search for elements in files.")
parser.add_argument(
    "--show-paths",
    action="store_true",
    help="Display the file paths along with the elements.",
)
parser.add_argument(
    "--print-lines",
    action="store_true",
    help="Print the matching lines along with the file paths.",
)
args = parser.parse_args()


if __name__ == "__main__":
    for root, dirs, files in os.walk(SRC_FOLDER):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r") as file:
                for line in file:
                    if PATTERN.search(line):
                        element = PATTERN.search(line).group(1)
                        if args.print_lines:
                            print(line.strip())
                        founded_results.setdefault(element, set()).add(file_path)
    if founded_results:
        for element, files_path in founded_results.items():
            if args.show_paths:
                print(f"\n\n* {element}:\t{len(files_path)}\n")
                for path in files_path:
                    print(path)
            else:
                print(f"* {element}:\t{len(files_path)}")
    else:
        print("No results found")
