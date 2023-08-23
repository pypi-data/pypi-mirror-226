from __future__ import annotations


class File:
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level
        self.last = False

    def __lt__(self, other: File) -> bool:
        return self.name > other.name
