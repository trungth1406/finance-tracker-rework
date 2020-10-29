from model.state import *
from algorithm import lcs


class Line:

    def __init__(self, line_number=None, content=None):
        self.line_number = line_number + 1
        self.content = content
        self.state = Create(line_number, content)

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


class FileVersion:

    def __init__(self, version_name=None, all_lines=None, current_version=1):
        self.version_name = version_name
        self.current_version = current_version
        self.lines = deque()
        for num, content in enumerate(all_lines):
            line_obj = Line(num, content)
            self.lines.append(line_obj)

    def compare_line(self, new_version):
        counts = []
        last_line_count = 1
        while len(self.lines) != 0:
            new_line = self.lines.popleft().compare_with(new_version.lines.popleft())
            counts.append(new_line)
            last_line_count = last_line_count + 1
        for remain in new_version.lines:
            remain._line_number = last_line_count
            counts.append(remain)
        return counts


class File:

    def __init__(self, file_name, lines):
        self.file_name = file_name
        self.file_version = FileVersion(file_name, lines)

    def total_lines(self):
        return len(self.file_version.lines)

    def current_version(self):
        return self.file_version.current_version

    def compare(self, another_file):
        return self.file_version.compare_line(another_file.file_version)
