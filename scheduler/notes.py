from dataclasses import dataclass
from datetime import datetime
from typing import List

from model.fileio import *


@dataclass
class NoteChanges:
    change_type: str
    new_version: FileVersion
    file_name: str
    date_of_execution: datetime
