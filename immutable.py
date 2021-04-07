class List:
	def __init__(self, iterable=[]):
		self.__items = tuple(iterable)

	def append(self, item):
		return List(self.__items + (item,))

	def __getitem__(self, index):
		if isinstance(index, slice):
			return List(self.__items[index])
		return self.__items[index]

	def __len__(self):
		return len(self.__items)

	def set(self, index, value):
		return List(self.__items[:index] + (value,) + self.__items[index+1:])

	def update(self, index, fun):
		return self.set(index, fun(self[index]))

	def __str__(self):
		return 'List' + str(self.__items)

	def __repr__(self):
		return str(self)

	def __add__(self, other):
		return List(self.__items + other.__items)

	def __contains__(self, item):
		return item in self.__items

	def index(self, item):
		return self.__items.index(item)

	def __copy__(self):
		return self

	def remove(self, index):
		return List(self.__items[:index] + self.__items[index+1:])

	def pop(self, index=-1):
		elem = self[index]
		return self.remove(index), elem

	def __python__(self):
		res = []
		for elem in self:
			res.append(toPython(elem))
		return res
        
	def apply(self, L):
		res = []
		for fun in self.__items:
			for elem in L:
				res.append(fun(elem))
		return List(res)

	def map(self, fun):
		return List(map(fun, self.__items))

	def join(self):
		res = []
		for elem in self.__items:
			res += elem
		return List(res)

	def bind(self, fun):
		return self.map(fun).join()


class Map:
	def __init__(self, *args, **kwargs):
		self.__map = dict(*args, **kwargs)

	def __getitem__(self, key):
		return self.__map[key]

	def __len__(self):
		return len(self.__map)

	def __iter__(self):
		return iter(self.__map)

	def items(self):
		return self.__map.items()

	def values(self):
		return self.__map.values()

	def keys(self):
		return self.__map.keys()

	def set(self, key, value):
		map = dict(self.__map)
		map[key] = value
		return Map(map)

	def update(self, key, fun):
		return self.set(key, fun(self[key]))

	def __str__(self):
		return 'Map' + str(self.__map)

	def __repr__(self):
		return str(self)

	def __contains__(self, key):
		return key in self.__map

	def __copy__(self):
		return self

	def remove(self, key):
		map = dict(self.__map)
		del(map[key])
		return Map(map)

	def pop(self, key):
		value = self[key]
		return self.remove(key), value

	def __python__(self):
		res = {}
		for key, value in self.items():
			res[key] = toPython(value)
		return res

if __name__ == '__main__':
	L = List([1, 2, 3])
	def add(a):
		def adda(b):
			return a + b
		return adda
	print(L.map(add).apply([1, 2, 3]))

def append(item):
	def fun(L: List):
		return L.append(item)
	return fun

def set(keyOrIndex, value):
	def fun(ListOrMap):
		return ListOrMap.set(keyOrIndex, value)
	return fun

def remove(keyOrIndex):
	def fun(ListOrMap):
		return ListOrMap.remove(keyOrIndex)
	return fun

def pop(keyOrIndex, callback):
	def fun(ListOrMap):
		state, result = ListOrMap.pop(keyOrIndex)
		callback(result)
		return state
	return fun

def add(value):
	def fun(item):
		return item + value
	return fun

def toPython(a):
	if '__python__' in dir(a):
		return a.__python__()
	return a
