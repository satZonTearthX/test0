# -*- coding: utf8 -*-

class MultiCase(object):
	def __init__(self, *cases):
		"""
		:param tuple or list cases: MultiCase(['wo'], ['de'])
		"""
		self.cases = list(map(lambda i: tuple(i), cases))


	def __iter__(self):
		return iter(self.cases)
	
	def __getitem__(self, index):
		"""
		:param int index:
		:return:
		"""
		return self.cases[index]
	
	def __setitem__(self, index, value):
		"""
		:param int index:
		:param list or tuple value:
		:return:
		"""
		self.cases[index] = tuple(value)
	
	def __delitem__(self, index):
		"""
		:param int index:
		:return:
		"""
		self.cases.pop(index)
	
	def __len__(self):
		return len(self.cases)
	
	def __add__(self, other):
		"""
		:param tuple or list or MultiCase other:
		:return:
		"""
		if isinstance(other, MultiCase):
			other = other.cases
		elif not isinstance(other, list or tuple):
			raise NotImplemented()
		return MultiCase(*(self.cases + list(other)))
	
	def __iadd__(self, other):
		"""
		:param tuple or list or MultiCase other:
		:return:
		"""
		return self + other
	
	def __radd__(self, other):
		"""
		:param tuple or list or MultiCase other:
		:return:
		"""
		return self + other
	
	def __mul__(self, other):
		"""
		:param tuple or list or MultiCase other:
		:return:
		"""
		if isinstance(other, MultiCase):
			other = other.cases
		elif not isinstance(other, list or tuple):
			raise NotImplemented()
		res = MultiCase()
		for case in other:
			res += MultiCase(*map(lambda i: i + case, self.cases))
		return res
	
	def __rmul__(self, other):
		"""
		:param tuple or list or MultiCase other:
		:return:
		"""
		return self * other
	
	def __imul__(self, other):
		"""
		:param tuple or list or MultiCase other:
		:return:
		"""
		return self * other
	
	def __str__(self):
		return str(self.cases)


if __name__ == '__main__':
	add = MultiCase(['hao', 'de'], ['hao', 'di']) + MultiCase(['zai', 'jian'], ['zai', 'xian'])
	a1=['de','di','er']
	# a2=('de','di')
	# mul=MultiCase(a1)*MultiCase(a2)
	# mul=MultiCase(map(lambda i: tuple(i), ))
	mul = MultiCase([])
	mul = mul*MultiCase(*map(lambda i:[i,],a1))*MultiCase(*map(lambda i:[i,],a1))
	# mul = MultiCase(['hao', 'de'], ['hao', 'di']) * MultiCase(['zai', 'jian'], ['zai', 'xian'])
	# print(add)
	print(mul)
	s=list()
	# print(type(s))
	for i in range(len(mul)):
		tems=''
		for j in range(len(mul[i])):
			tems=tems+str(mul[i][j])
		s.append(tems)

	print(s)
	# print(mul[0].__str__())
	# for i in mul:
	# 	strs=''


		#写到未把元组合成字符串
    #
	# timestamp=str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
	# name=name+timestamp
	# print(timestamp)