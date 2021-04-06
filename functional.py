from functools import reduce, partial, wraps, lru_cache
from collections import namedtuple

def cache(fun):
	return lru_cache(maxsize=None)(fun)

def pluck(key):
	def pluck(D):
		return D[key]
	return pluck

def curry():
	pass

def compose(*functions):
	def composed(*args, **kwargs):
		res = functions[-1](*args, **kwargs)
		for fun in reversed(functions[:-1]):
			res = fun(res)
		return res
	return composed

def flow(*functions):
	return compose(*reversed(functions))

def record(*args, **kwargs):
	if len(args) > 0:
		raise ValueError('record do not support positional arguments')
	T = namedtuple('record', kwargs.keys())
	return T(**kwargs)

class Promise():
	def __init__(self, fun):
		self.__status = 'pending'
		self.__value = None
		self.__error = None
		self.__resolver = None
		self.__rejecter = None

		def resolve(value):
			if self.__status == 'pending': 
				self.__value = value
				self.__status = 'resolved'
				if self.__resolver is not None:
					self.__resolver(value)

		def reject(error):
			if self.__status == 'pending':
				self.__error = error
				self.__status = 'rejected'
				if self.__rejecter is not None:
					self.__rejecter(error)

		fun(resolve, reject)

	def then(self, fun):
		def promiseBuilder(resolve, reject):
			def resolver(value):
				res = fun(value)
				if isinstance(res, Promise):
					res.then(resolve)
				else:
					resolve(res)
			self.__resolver = resolver
		promise = Promise(promiseBuilder)
		return promise

	def catch(self, fun):
		if self.__status != 'rejected':
			self.__rejecter = fun
		else:
			fun(self.__error)
		#must return a new Promise

class createStore():
	pass

if __name__ == '__main__':
	r = None
	
	def f(resolve, reject):
		global r
		r = resolve

	p = Promise(f)

	p.then(lambda v: 2*v).then(lambda v: print(v))

	r('hello')
