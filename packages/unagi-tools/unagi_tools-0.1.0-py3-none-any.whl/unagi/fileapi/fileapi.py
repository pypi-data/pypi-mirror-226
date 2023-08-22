from __future__ import annotations

import contextlib
import logging
import subprocess
from enum import Enum
from typing import *

import fsspec

log = logging.Logger(__name__)

_DEFAULT_CALLBACK = fsspec.callbacks.NoOpCallback()


@contextlib.contextmanager
def open(path: Union[AnyStr, FileAPI], *args, **kwargs):
	file = FileAPI.get_file_api(path)
	with file.open(*args, **kwargs) as f:
		yield f


class FileCache(Enum):
	SIMPLE = "simplecache"
	FILE = "filecache"
	BLOCK = "blockcache"
	NONE = None  # use for eg FTP


class FsSpecFileType(Enum):
	DIRECTORY = "directory"
	FILE = "file"


_DEFAULT_CACHE_TYPE = FileCache.SIMPLE
_DEFAULT_FILE_PATH = "/"


class FileAPI(object):

	def __init__(self, path: Union[AnyStr, Self], fs: fsspec.AbstractFileSystem = None,
			cache_type: FileCache = _DEFAULT_CACHE_TYPE, auto_make_dir: bool = True, details: Dict = None,
			**kwargs
	):  # FileCache.SIMPLE

		if isinstance(path, str):
			self.path_string = path
			self.fs, self.fs_path = (fs, self.path_string) if fs else self.get_file_system(
				path, cache_type,
				auto_make_dir, **kwargs
			)
			self.cache_type = cache_type
			self.kwargs = kwargs
			if details:
				self.details = details
				self.type = self.details.get("type", None)
			else:
				self.details, self.type = None, None

		elif isinstance(path, FileAPI):
			self.path_string = path.path_string
			self.fs, self.fs_path = (fs, self.path_string) if fs else (path.fs, path.fs_path)
			self.details = details if details else path.details

			self.type = (details if details else path.details).get("type", None)
			self.cache_type = cache_type if cache_type != _DEFAULT_CACHE_TYPE else path.cache_type
			self.kwargs = path.kwargs | kwargs

		else:
			raise TypeError(f"Unexpected type `{type(path)}`")

		if None is self.fs_path:
			self.fs_path = _DEFAULT_FILE_PATH

		if not self.details:
			self.update_details()

	@property
	def full_file_path(self):
		res = self.fs.unstrip_protocol(self.fs_path)
		new_res = res.replace("gcs://", "gs://", 1)
		return new_res

	def __str__(self):
		return self.full_file_path

	def du(self, total=True, maxdepth=None, **kwargs):
		return self.fs.du(self.fs_path, total, maxdepth, **kwargs)

	def update_details(self):
		try:
			self.details = self.fs.stat(self.fs_path)
			self.type = self.details.get("type", None)
			return True
		except:
			return False

	@property
	def is_dir(self):
		if not self.type:
			self.update_details()
		return FsSpecFileType.DIRECTORY.value == self.type

	@property
	def is_file(self):
		if not self.type:
			self.update_details()
		return FsSpecFileType.FILE.value == self.type

	def add_dir(self, other: str) -> FileAPI:
		return FileAPI(
			path=f"{self.fs_path.rstrip('/')}/{other.lstrip('/')}", fs=self.fs, cache_type=self.cache_type,
			**self.kwargs
		)

	def __floordiv__(self, other: str) -> FileAPI:
		return self.add_dir(other)

	def __truediv__(self, other: str) -> FileAPI:
		return self.add_dir(other)

	def add_file(self, other: str) -> FileAPI:
		return FileAPI(path=f"{self.fs_path}{other}", fs=self.fs, cache_type=self.cache_type, **self.kwargs)

	def __add__(self, other: AnyStr) -> FileAPI:
		return self.add_file(str(other))

	def exists(self, **kwargs) -> FileAPI:
		return self.fs.exists(self.fs_path, **kwargs)

	def checksum(self) -> int:
		return self.fs.checksum(self.fs_path)

	def size(self) -> int:
		return self.fs.size(self.fs_path)

	def download_locally(self, dest_path: AnyStr, recursive=True, callback=_DEFAULT_CALLBACK, **kwargs):
		return self.fs.get(self.fs_path, dest_path, recursive, callback, **kwargs)

	def list_filenames(self) -> list:

		if self.is_dir:
			# create temp list

			if "gs://" in self.full_file_path:

				bash_command = "gsutil ls " + self.full_file_path
			elif "s3://" in self.full_file_path:
				bash_command = "aws s3 ls " + self.full_file_path + "/"

			else:
				print("UNKNOWN FILE EXTENSION")
				raise NotImplementedError
			process_ = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
			output, error = process_.communicate()

			bytes_list_val = output.splitlines()
			string_list = [x.decode('utf-8') for x in bytes_list_val]
			if "s3://" in self.full_file_path:
				final_string_list = []
				for list_item in string_list:
					new_list_ = list_item.split(" ")
					endpoint = new_list_[-1]
					full_path = self.full_file_path + "/" + endpoint
					final_string_list.append(full_path)
				return final_string_list
			else:

				return string_list

	@property
	def dirname(self):
		if self.is_dir:
			return self.fs_path.split("/")[-1]
		return None

	@property
	def filename(self):
		if self.is_file:
			return self.fs_path.split("/")[-1]
		return None

	@property
	def filename_without_ext(self):
		if self.is_file:
			return ".".join(self.fs_path.split("/")[-1].split(".")[:-1])
		return None

	def glob(self, **kwargs) -> Generator[FileAPI, None, None]:
		children = self.fs.glob(self.fs_path, detail=True, **kwargs).values()
		for child in children:
			child_file = FileAPI(
				path=child["name"], fs=self.fs, cache_type=self.cache_type, details=child,
				**self.kwargs
			)
			yield child_file

	def list_children(self, recursive: bool = True, **kwargs) -> Generator[FileAPI, None, None]:
		if self.is_file:
			yield self
		elif self.is_dir:
			if "*" in self.fs_path or "?" in self.fs_path or "[" in self.fs_path:
				children = self.fs.glob(self.fs_path, detail=True, **kwargs).values()
			else:
				children = self.fs.ls(self.fs_path, detail=True, **kwargs)

			for child in children:
				child_file = FileAPI(
					path=child["name"], fs=self.fs, cache_type=self.cache_type, details=child,
					**self.kwargs
				)
				if child_file.fs_path == self.fs_path: continue
				if FsSpecFileType.FILE.value == child_file.type:
					yield child_file
				elif FsSpecFileType.DIRECTORY.value == "directory":
					if recursive:
						yield from child_file.list_children(recursive=recursive, **kwargs)
					else:
						yield child_file
				else:
					raise RuntimeError(f"File {child_file.__str__()} is not a file or directory")
		else:
			if "*" in self.fs_path or "?" in self.fs_path or "[" in self.fs_path:
				children = self.fs.glob(self.fs_path, detail=True, **kwargs).values()
				for child in children:
					child_file = FileAPI(
						path=child["name"], fs=self.fs, cache_type=self.cache_type, details=child,
						**self.kwargs
					)
					if child_file.fs_path == self.fs_path: continue
					if FsSpecFileType.FILE.value == child_file.type:
						yield child_file
					elif FsSpecFileType.DIRECTORY.value == "directory":
						if recursive:
							yield from child_file.list_children(recursive=recursive, **kwargs)
						else:
							yield child_file
					else:
						raise RuntimeError(f"File {child_file.__str__()} is not a file or directory")
			else:
				raise RuntimeError(f"File {self.__str__()} is not a file or directory")

	def read_lines(self, recursive: bool = True, *args, **kwargs) -> Generator[bytes, None, None]:
		for child in self.list_children(recursive, *args, **kwargs):
			with child.open("rb") as f:
				for line in f.readlines():
					yield line

	def num_lines(self) -> Optional[int]:
		length = None
		try:
			with self.open("rb") as f:
				length = len(f.readlines())
		except Exception as e:
			pass
		return length

	@property
	def parent_dir_str(self):
		return '/'.join(self.fs_path.split('/')[:-1])

	@property
	def parent_dir(self) -> FileAPI:
		return FileAPI(self.parent_dir_str, fs=self.fs, cache_type=self.cache_type, **self.kwargs)

	def exists(self) -> bool:
		return self.fs.exists(self.fs_path)

	def remove(self, recursive: bool = True, maxdepth: int = None):
		return self.fs.rm(self.fs_path, recursive=recursive, maxdepth=maxdepth)

	def open(self, mode: AnyStr = "rb", block_size: int = None, cache_options: Optional[Dict] = None,
			compression: AnyStr = None, **kwargs
	):
		if "w" in mode:
			self.fs.mkdirs(self.parent_dir_str, exist_ok=True)
		return self.fs.open(self.fs_path, mode, block_size, cache_options, compression, **kwargs)

	def make_dirs(self):
		self.fs.mkdirs(self.fs_path, exist_ok=True)
		return self

	@staticmethod
	def get_file_system(path, cache_type: FileCache = FileCache.SIMPLE, auto_make_dir: bool = True, **kwargs) -> Tuple[
		fsspec.AbstractFileSystem, str]:
		if auto_make_dir: kwargs.update({"auto_mkdir": kwargs.pop("auto_mkdir", True)})
		fs_path = f"{cache_type.value}::{path}" if cache_type else path
		res = fsspec.core.url_to_fs(fs_path, **kwargs)
		return res

	@staticmethod
	def get_file_api(path: Union[FileAPI, AnyStr], cache_type: FileCache = _DEFAULT_CACHE_TYPE) -> FileAPI:
		if isinstance(path, FileAPI):
			return path
		elif isinstance(path, str):
			return FileAPI(path)
		elif isinstance(path, bytes):
			return FileAPI(path.decode("utf-8"))
		else:
			raise TypeError(f"Invalid file path type, expecting `str` or `FileAPI` for {type(path)} of {path}")

	# auto increments the file name if it already exists
	def auto_incr(self, idx: int = 1, pad: int = 3):
		new_file = (self + str(idx).zfill(pad))
		if new_file.exists():
			return self.auto_incr(idx=idx + 1, pad=pad)
		else:
			return new_file

	# DOES NOT WORK, TODO get this working
	# Direct copy between buckets, etc. without using local file system
	# def copy_to(self, dest: FileAPI, recursive=True, on_error=None):
	#     self.fs.copy(self.full_file_path, dest.full_file_path)

	# Copy using local network IO
	def copy_file_contents(self, dest: FileAPI):
		with self.open("rb") as in_f:
			with dest.open("wb") as out_f:
				data = in_f.readlines()

				out_f.writelines(data)

	# @property
	# def detect_file_type(self) -> Optional[str]:
	#     """
	#     Detects the file type using the python-magic library
	#
	#     For macos, install libmagic using `brew install libmagic`
	#     For debian, install libmagic using `sudo apt-get install libmagic1`
	#     Then install python-magic using `poetry add python-magic`
	#     :return: the mime type of the file or None if the file does not exist
	#     """
	#     import magic
	#     if self.exists() and self.is_file:
	#         with self.open("rb") as f:
	#             return magic.from_buffer(f.read(2048), mime=True)
	#     else:
	#         return None

	@property
	def extension(self):
		return self.path_string.split(".")[-1]
