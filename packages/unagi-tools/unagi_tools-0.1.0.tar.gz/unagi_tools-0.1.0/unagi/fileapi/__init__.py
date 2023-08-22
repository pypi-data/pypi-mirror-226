import contextlib
from typing import Union, AnyStr
from .fileapi import FileAPI

__all__ = [
	"FileAPI",
	# "CacheType",
	# "FileType",
	# "open"
]


@contextlib.contextmanager
def open(path: Union[AnyStr, FileAPI], *args, **kwargs):
	pass
	# file = FileAPI.get_file_api(path)
	# with file.open(*args, **kwargs) as f:
	# 	yield f
