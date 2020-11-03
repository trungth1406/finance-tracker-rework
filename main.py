import binascii
import zlib

from tinydb.table import Document

from googleapi.sheetapi import GoogleService, GoogleSheetRequest
from macnotereader import notereader
from model.fileio import *
from pprint import pprint
import gspread
from caching.jsondb import *
import sqlite3
import ast
from munch import munchify

"""find a way tp load document record to file_version_object"""


def main():
    f = open("test.txt", "r")
    lines = notereader.get_new_contents(possible_file_name=f'Tháng 10')
    if len(lines) == 0: return
    new_file_version = FileVersion(all_lines=lines)
    db = TinyDB("db.json")
    table = db.table("file_version")
    if len(table) == 0:
        # with open("db-1.json","w") as out:
        #     json.dump(new_file_version.to_json(), out, indent=4)
        table.insert({"content": new_file_version.to_json(), "ver_name": u"Tháng 10"})
    else:
        # doc = json.load(out, cls=FileVersion)
        doc = table.get(doc_id=len(table))
        loaded = json.loads(json.dumps(doc['content']))
        from_json = json.loads(loaded)
        old_lines = []
        all_lines = from_json['lines']
        for each in all_lines:
            old_line = Line.from_json(each)
            old_lines.append(old_line)
        old_version = FileVersion(loaded_lines=old_lines)
        lines = old_version.compare_line(new_file_version)
        table.insert({"content": new_file_version.to_json(), "ver_name": u" Tháng 10"})


# f2 = open("test2.txt", "r")
# lines = f.readlines()
# file_version = File(f.name, lines)
# file_version_2 = File(f2.name, f2.readlines())
# new_lines = file_version.compare(file_version_2)
# db = TinyDB("db.json")
# table = db.table("file_version")
# table.insert({f"version": file_version_2.to_json()})
# res = table.get(doc_id=len(table))
# print(res)
# for line in new_lines:
#     print(line.state.get_content())
#     print(line.state.range())
#     print(line.state)
# encode(line.state)
# db = TinyDB('db.json')
# table = db.table("file_version")
# table
# res = decode("cache.json")
# pprint(res)
# google_service = GoogleService("/Users/trungtran/PycharmProjects/finance-core/credentials.json")
# request = GoogleSheetRequest(spreadsheet_id="12TqYhXjfbVDt6C8zUjyBbgUbGJmhNJ4Mly1Lgi8gsgk",
#                              sheet_name="Tháng 10")
#
# response = google_service.read(request)
# pprint(response)
# gc = gspread.service_account(filename="credentials.json", )
# spread_sheet = gc.open_by_key("12TqYhXjfbVDt6C8zUjyBbgUbGJmhNJ4Mly1Lgi8gsgk")
# spread_sheet.worksheet("Tháng 10").get_all_values()
# work_sheet = spread_sheet.worksheet("Tháng 10")
# union = work_sheet.get_all_values()
# pprint(union)
# body = [["", "aaa", "", "190"]]
# work_sheet.update("A70:D70", body)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
