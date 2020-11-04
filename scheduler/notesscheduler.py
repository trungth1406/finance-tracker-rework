from abc import ABC, abstractmethod

from tinydb import TinyDB

from googleapi.sheetapi import GoogleService, GoogleSheetRequest
from scheduler.notes import NoteChanges
from model.state import *
import gspread


class Observer(ABC):

    def __init__(self):
        self.db = TinyDB("october.json")
        self.table = self.db.table("file_version")

    @abstractmethod
    def update(self, note_changes: NoteChanges) -> None:
        pass


class NewFileObserver(Observer):

    def update(self, note_changes: NoteChanges) -> None:
        gc = gspread.service_account(filename="credentials.json")
        spread_sheet = gc.open_by_key("12TqYhXjfbVDt6C8zUjyBbgUbGJmhNJ4Mly1Lgi8gsgk")
        try:
            work_sheet = spread_sheet.worksheet(note_changes.file_name)
        except gspread.exceptions.WorksheetNotFound:
            work_sheet = spread_sheet.add_worksheet(title=note_changes.file_name, rows=100, cols=10)
        new_ver = note_changes.new_version
        for new_record in new_ver.lines:
            work_sheet.update(new_record.state.range(), [new_record.state.get_content()])
        self.table.insert({"content": new_ver.to_json()})


class ExistingFileObserver(Observer):
    """Class used for create and update db caching"""

    def update(self, note_changes: NoteChanges) -> None:
        if note_changes.change_type == 'MODIFIED':
            pass


class NotesWatcher:

    def __init__(self):
        self.observers = dict()
        self.observers.update({"NEW": NewFileObserver()})
        self.observers.update({"MODIFIED": ExistingFileObserver()})

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self, note_changes: NoteChanges):
        print("Notifying observers...")
        observer = self.observers.get(note_changes.change_type)
        observer.update(note_changes)
