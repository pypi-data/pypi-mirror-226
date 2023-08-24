from __future__ import annotations
from typing import List, Union, Sequence, Optional

from .file import File


class Folder:
    """A Folder is a node in a tree structure. It can contain other Folders and Files."""

    def __init__(self, name: str, level: int, parent=None):
        self.name = name
        self.level = level
        self._folders: List[Folder] = []
        self._files: List[File] = []
        self.last = False
        self._parent: Optional[Folder] = parent

    def __lt__(self, other: Folder) -> bool:
        return self.name > other.name

    @property
    def parent(self) -> Folder:
        """Don't allow the user to go further than root."""
        if self._parent is None:
            return self
        return self._parent

    @parent.setter
    def parent(self, other: Optional[Folder]) -> None:
        self._parent = other

    def file(self, file: str, level: int) -> None:
        """Adds a file to the current Folder."""
        self._files.append(File(file, level))

    def folder(self, folder: Folder) -> None:
        """Adds a direct sub-folder to the current Folder."""
        self._folders.append(folder)

    def contents(self) -> Sequence[Union[File, Folder]]:
        """Returns an alphabetized list of folders and files found in the current Folder."""
        items: List[Union[File, Folder]] = []
        items += sorted(self._files[::])
        items += sorted(self._folders[::])
        if items:
            items[0].last = True
        return items

    def folders(self) -> List[Folder]:
        """Returns an alphabetized list of folders found in the current Folder."""
        return sorted(self._folders[::])

    def files(self) -> List[File]:
        """Returns an alphabetized list of files found in the current Folder."""
        return sorted(self._files[::])
