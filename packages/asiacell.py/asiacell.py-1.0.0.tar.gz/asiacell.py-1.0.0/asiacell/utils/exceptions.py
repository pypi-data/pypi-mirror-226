class AsiaCellBaseException(Exception):
	"""Base Class for AsiaCell Exceptions"""
	...


def handle_exception(message):
	raise AsiaCellBaseException(message)
