from collections import deque


class Modification:
    total_length = 4

    def __init__(self, line_number, content):
        self._line_number = line_number
        self._content = content

    def get_content(self, total_cell=4):
        if "+" or "-" in self._content:
            self._content = self._content.replace('+', "")
            self._content = self._content.replace('-', "")
            self._content = self._content.replace("  ", "")
        split = deque(filter(None, self._content.split(" ")))
        final_list = deque(['' for _ in range(total_cell)])
        while len(split) != 0:
            possible_word = split.popleft()
            if not possible_word.isnumeric():
                final_list[1] += possible_word + ' '
            else:
                final_list[3] = possible_word
        return list(final_list)

    def range(self, column='A'):
        next_char = chr(ord(column) + Modification.total_length - 1)
        return f'{column}{self._line_number}:{next_char}{self._line_number}'


class Create(Modification):

    def get_content(self):
        self._content.replace("+", "") if "+" in self._content else self._content
        return super().get_content()


class Update(Modification):

    def get_content(self):
        content_arr = self._content.split(" ")
        for item in content_arr:
            if "-" in item:
                content_arr.remove(item)
        self._content = " ".join(content_arr)
        return super().get_content()


class Delete(Modification):

    def get_content(self):
        self._content = ""
        return super().get_content()


class Unchanged(Modification):
    pass
