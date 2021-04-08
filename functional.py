from functools import reduce, partial, wraps, lru_cache, singledispatch
from collections import namedtuple
from types import FunctionType

builtinMap = map

def cache(fun):
	return lru_cache(maxsize=None)(fun)

def pluck(key):
	def pluck(D):
		if isinstance(D, dict):
			return D[key]
		return D.__getattribute__(key)
	pluck.__name__ = 'pluck_' + key
	return pluck

def curry(fun):
	def attach(things):
		@wraps(fun)
		def wrapper(*first):
			try:
				return fun(*(things + first))
			except TypeError:
				return attach(things + first)
		return wrapper
	return attach(tuple())
		

def compose(*functions):
	def composed(*args, **kwargs):
		res = functions[-1](*args, **kwargs)
		for fun in reversed(functions[:-1]):
			res = fun(res)
		return res
	return composed

def flow(*functions):
	return compose(*reversed(functions))
	
@singledispatch
def map(T, fun):
	raise NotImplementedError()	

@map.register(tuple)
def _(T, fun):
	return tuple((fun(elem) for elem in T))

@singledispatch
def flat(T):
	raise NotImplementedError()
	
@flat.register(tuple)
def _(T):
	return sum(T, ())

@singledispatch
def pure(fun):
	raise NotImplementedError()
	
@pure.register(FunctionType)
def _(fun):
	return (fun,)
	
@singledispatch
def apply(TF, T):
	raise NotImplementedError()
	
@apply.register(tuple)
def _(TF, T):
	return tuple([fun(elem) for fun in TF for elem in T])
	
def bind(T, fun):
	return flat(map(T, fun))
	
data = namedtuple

if __name__ == '__main__':
    Person = data('Person', ['name', 'age'])

    quentin = Person(name='Quentin', age=38)

    print(quentin)
    
    def add(a):
    	def add(b):
    		return a+b
    	return add
    	
    @curry
    def mult(a, b):
    	return a*b
