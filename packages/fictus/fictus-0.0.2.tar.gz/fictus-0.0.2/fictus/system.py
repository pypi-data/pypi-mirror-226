import os.path
import sys
from typing import List, Union, Set, Optional

from .constants import PIPE, SPACE_PREFIX, ELBOW, TEE
from .file import File
from .folder import Folder
from .renderer import Renderer, DefaultRenderer

"""
A System is created to simulate and generate a listing of directory/files.
"""


class System:
    """A System is a representation of a file system. Generates a tree structure to be printed."""

    def __init__(self, name: str):
        self.level = 0
        self.root = Folder(name, self.level)
        self.current: Folder = self.root
        self.ignore: Set[int] = set()
        self._renderer: Renderer = DefaultRenderer()

    @property
    def renderer(self) -> Optional[Renderer]:
        return self._renderer

    @renderer.setter
    def renderer(self, renderer: Renderer) -> None:
        self._renderer = renderer

    @staticmethod
    def _normalize(path: str) -> List[str]:
        normalized = os.path.normpath(path.replace("\\", "/"))
        return normalized.split(os.sep)

    def mkdirs(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and adds the directories
        one at a time."""

        visited = {d.name: d for d in self.current.folders()}

        # hold onto the current directory
        current = self.current
        current_level = self.level

        path_parts = self._normalize(path)
        for part in path_parts:
            if part not in visited:
                visited[part] = Folder(part, self.level + 1, parent=self.current)
                self.current.folder(visited[part])
            self.cd(visited[part].name)
            visited = {d.name: d for d in self.current.folders()}

        # return to starting directory
        self.current = current
        self.level = current_level

    def mkfiles(self, files: List[str]) -> None:
        """Takes one or more filenames and adds them to the cwd."""
        visited = {f.name for f in self.current.files()}
        for file in files:
            if file not in visited:
                visited.add(file)
                self.current.file(file, self.level + 1)

    def rename(self, old: str, new: str) -> None:
        for f in self.current.contents():
            if f.name == old:
                f.name = new
                break

    def cwd(self):
        """Returns the current working directory."""
        r = []
        visited = set()
        q = [self.current]
        while q:
            n = q.pop()
            if n.name is not None:
                r.append(n.name)
            visited.add(n)
            if n.parent not in visited:
                q.append(n.parent)

        return "/".join(r[::-1])

    def cd(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and changes the current"""
        if path == "/":
            # go to root
            while self.current.parent != self.current:
                self.current = self.current.parent
            return None

        path_parts = self._normalize(path)
        for part in path_parts:
            if part == "..":
                self.current = self.current.parent
                self.level = self.current.level
            else:
                # is it in the current folder?
                for folder in self.current.folders():
                    if folder.name == part:
                        self.current = folder
                        self.level = self.current.level
                        break
        return None

    def _pp(self, node: Union[File, Folder]) -> str:
        """
        Pretty print the node passed in. Bookkeeping of dead and last items are tracked
        to reveal content information in an aesthetic way.
        """

        parts = [PIPE + SPACE_PREFIX for _ in range(node.level)]
        for index in self.ignore:
            if len(parts) > index - 1:
                parts[index - 1] = " " + SPACE_PREFIX

        if parts:
            parts[-1] = ELBOW if node.last is True else TEE

        is_file = isinstance(node, File)
        file_open = self._renderer.file_open if is_file else ""
        file_close = self._renderer.file_close if is_file else ""

        # checking for Folder type
        end = "\\" if not is_file else ""

        return f'{"".join(parts)}{file_open}{node.name}{file_close}{end}'

    def _display_header(self) -> int:
        """Writes the CWD to stdout with forward slashes and
        returns the length of."""

        parts = self.cwd().split("/")
        if len(parts) > 1:
            header = "" if len(parts) <= 1 else "\\".join(parts[:-1])
            sys.stdout.write(header + "\\" + "\n")
            return len(header) - len(parts[-1])
        return 0

    def display(self) -> None:
        """Prints the directory structure to stdout."""
        sys.stdout.write(self._renderer.doc_open + "\n")
        header_length = self._display_header()

        q: List[Union[File, Folder]] = [self.current]
        self.ignore = {i for i in range(self.level)}
        while q:
            node = q.pop()
            if node.last is False:
                if node.level in self.ignore:
                    self.ignore.remove(node.level)
            line = self._pp(node)
            new_line = line.lstrip(" ")
            max_s = max((len(line) - len(new_line)), header_length)

            sys.stdout.write((max_s * " ") + new_line + "\n")
            if node.last is True:
                # track the nodes that no longer have children.
                self.ignore.add(node.level)

            if isinstance(node, Folder):
                q += node.contents()

        sys.stdout.write(self._renderer.doc_close + "\n")
