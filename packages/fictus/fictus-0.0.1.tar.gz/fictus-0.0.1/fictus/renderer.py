from abc import ABCMeta, abstractmethod

class Renderer(metaclass=ABCMeta):
    """A Renderer is a representation of how a tree should be printed."""
    @property
    @abstractmethod
    def doc_open(self):
        ...

    @property
    @abstractmethod
    def doc_close(self):
        ...

    @property
    @abstractmethod
    def file_open(self):
        """Returns the start tag for a file."""
        ...

    @property
    @abstractmethod
    def file_close(self):
        """Returns the end tag for a file."""
        ...

class DefaultRenderer(Renderer):
    """A DefaultRenderer is a representation of how a tree should be printed."""
    def __init__(self):
        self._doc_open = ''
        self._doc_close = ''
        self._file_open = ''
        self._file_close = ''

    @property
    def doc_open(self) -> str:
        return self._doc_open
    
    
    @property
    def doc_close(self) -> str:
        return self._doc_close

    @property
    def file_open(self):
        return self._file_open

    @property
    def file_close(self):
        return self._file_close

class MarkdownRenderer(Renderer):
    """A MarkdownRenderer is a representation of how a tree should be printed in markdown."""
    def __init__(self):
        super().__init__()

        self._doc_open = '<pre style="line-height:17px">'
        self._doc_close = '</pre>'
        self._file_open = '<span style="color:gray">'
        self._file_close = '</span>'


    @property
    def doc_open(self) -> str:
        return self._doc_open

    @property
    def doc_close(self) -> str:
        return self._doc_close

    @property
    def file_open(self) -> str:
        return self._file_open

    @property
    def file_close(self) -> str:
        return self._file_close
