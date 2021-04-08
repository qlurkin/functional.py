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
