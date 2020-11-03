from typing import Any, Mapping

from model.serializer import Serializer

from model.state import *
from algorithm import lcs
from caching.jsondb import *
from json import JSONEncoder
from tinydb import TinyDB, Query


class Line(Serializer):

    def __init__(self, line_number=None, content=None,**kwargs):
        self.line_number = line_number + 1
        self.content = content
        self.state = Create(line_number, content)

    @classmethod
    def from_json(cls, json_dict):
        return cls(**json_dict)

    def current_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def compare_with(self, line_object):
        diff_tbl = self.diff_table(line_object)
        first = len(self.content)
        second = len(line_object.content)
        changes = lcs.get_changes_content(diff_tbl, self.content, line_object.content, first, second, [])
        changes.reverse()
        self.change_state(changes)
        self.state._content = " ".join(changes)
        return self

    def change_state(self, changes: []):
        changes_str = "".join(changes)
        if "+" in changes_str and "-" in changes_str:
            self.set_state(Update(self.line_number, self.content))
        elif "+" in changes_str:
            self.set_state(Create(self.line_number, self.content))
        elif "-" in changes_str:
            self.set_state(Delete(self.line_number, self.content))

    def diff_table(self, line_obj) -> []:
        """
        :rtype: lis,
        """
        return lcs.diff_table(self.content, line_obj.content, len(self.content), len(line_obj.content))


class FileVersion(Serializer, JSONEncoder):

    def __init__(self, version_name=None, all_lines=None, current_version=1,**kwargs):
        self.version_name = version_name
        self.current_version = current_version
        self.lines = []
        if all_lines is not None:
            for num, content in enumerate(all_lines):
                line_obj = Line(num, content)
                self.lines.append(line_obj)
        else:
            self.lines = kwargs['loaded_lines']

    def compare_line(self, new_version) -> [Line]:
        counts = []
        while len(self.lines) != 0 and len(new_version.lines) != 0:
            old_line = self.lines.pop(0)
            new_line = new_version.lines.pop(0)
            counts.append(old_line.compare_with(new_line))
        if len(self.lines) > 0:
            for remain in self.lines:
                line_number = remain.line_number
                content = remain.content
                line = Line(line_number, content)
                line.state = Delete(line_number, content)
                counts.append(line)
        if len(new_version.lines) > 0:
            for remain in new_version.lines:
                line_number = remain.line_number
                content = remain.content
                line = Line(line_number, content)
                line.state = Create(line_number, content)
                counts.append(line)
        return counts

    @staticmethod
    def handle_remain(lines, state: Modification):
        remain_counts = []
        for remain in lines.lines:
            line_number = remain.line_number
            content = remain.content
            line = Line(line_number, content)
            line.state = state
            remain_counts.append(line)
        return remain_counts


class File(Serializer):

    def __init__(self, file_name, lines):
        self.file_name = file_name
        self.file_version = FileVersion(file_name, lines)

    def total_lines(self):
        return len(self.file_version.lines)

    def current_version(self):
        return self.file_version.current_version

    def compare(self, another_file):
        lines = self.file_version.compare_line(another_file.file_version)
        return lines
