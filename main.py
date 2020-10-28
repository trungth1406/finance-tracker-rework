from model.state import *
from model.fileio import *


def main():
    f = open("test.txt", "r")
    f2 = open("test2.txt", "r")
    lines = f.readlines()
    file_version = File(f.name, lines)
    file_version_2 = File(f2.name, f2.readlines())
    print(file_version.total_lines())
    new_lines = file_version.compare(file_version_2)
    for line in new_lines:
        print(line.state.get_content())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
