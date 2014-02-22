


class Singleton():
	instance = None
	def __init__(self):
		print('init Singleton')
	def getInstance():
		if Singleton.instance is None:
			print('create Singleton')
			Singleton.instance = Singleton()
		return Singleton.instance;




Singleton.getInstance()
Singleton.getInstance()
Singleton.getInstance()
Singleton.getInstance()
Singleton.getInstance()
Singleton.getInstance()
