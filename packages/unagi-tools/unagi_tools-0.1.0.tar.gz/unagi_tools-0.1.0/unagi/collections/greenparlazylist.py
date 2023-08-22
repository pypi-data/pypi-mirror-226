# Importing necessary components from the existing classes
from typing import Iterable, Union, Callable, Any, Iterator, List, TypeVar, Generator

import gevent
from gevent import monkey

from unagi.collections import AbstractList, GreenParList, LazyList

# Patching all to enable green threads
monkey.patch_all()

# Defining the type variables
T = TypeVar("T")
U = TypeVar("U")


class GreenParLazyList(GreenParList[T], LazyList[T]):
	def __init__(self, iterator: Union[Iterable[T], Callable[[], Iterator[T]]]) -> None:
		# Initializing GreenParList (parent class)
		GreenParList.__init__(self, [])
		# Initializing LazyList attributes
		LazyList.__init__(self, iterator)

	def map(self, func: Callable[[T], U]) -> 'GreenParLazyList[U]':
		# Mapping the function using green threads, with truly lazy evaluation
		def map_generator():
			for item in self:
				greenlet = gevent.spawn(func, item)
				gevent.joinall([greenlet])
				yield greenlet.value

		return GreenParLazyList(map_generator)

	def flatmap(self, func: Callable[[T], List[U]]) -> 'GreenParLazyList[U]':
		# Flatmapping the function using green threads, with truly lazy evaluation
		def flatmap_generator():
			for item in self:
				greenlet = gevent.spawn(func, item)
				gevent.joinall([greenlet])
				for subitem in greenlet.value:
					yield subitem

		return GreenParLazyList(flatmap_generator)
