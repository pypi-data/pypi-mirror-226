from unagi.collections import *
from unagi.fileapi import FileAPI


def main():
	(
		GreenParLazyList(range(0, 1000))
		.foreach(lambda x: print(x))
	)

	file = FileAPI(".")
	LazyList(file.list_children()).foreach(lambda x: print(x))


if __name__ == '__main__':
	main()
