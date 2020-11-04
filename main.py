import time

import schedule

from macnotereader import notereader
from scheduler.notes import *
from scheduler.notesscheduler import *

"""find a way tp load document record to file_version_object"""


def main():
    schedule.every(3).seconds.do(watch_for_changes)
    while True:
        schedule.run_pending()
        time.sleep(1)


def watch_for_changes():
    table = init_db_table()
    file_name = f"Tháng {datetime.now().strftime('%m')}"
    optional_doc = table.get(doc_id=len(table))
    new_lines = query_notes_db(file_name)
    new_version = create_new_version(new_lines)
    if optional_doc is None or new_lines is None:
        changes = NoteChanges("NEW", new_version, file_name, datetime.now())
    else:
        changes = NoteChanges("MODIFIED", new_version, file_name, datetime.now())
    watcher = NotesWatcher()
    watcher.notify(changes)


def init_db_table(file_name=f"Tháng {datetime.now().strftime('%m')}"):
    db = TinyDB(f"{file_name}.json")
    table = db.table("file_version")
    return table


def create_new_version(new_lines):
    line_obj = []
    for index, line in enumerate(new_lines):
        line_obj.append(Line(index + 1, line))
    new_version = FileVersion(loaded_lines=line_obj)
    return new_version


def query_notes_db(possible_file_name: str) -> []:
    lines = notereader.get_new_contents()
    return lines


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
