class InvalidExpression(Exception):
	def __str__(self):
		return 'Invalid expression'


class UnknownCommand(Exception):
	def __str__(self):
		return "Unknown command"


class Exit(Exception):
	def __str__(self):
		return "Bye!"


class InvalidIdentifier(Exception):
	def __str__(self):
		return "Invalid identifier"


class InvalidAssignment(Exception):
	def __str__(self):
		return 'Invalid assignment'


class UnknownVariable(Exception):
	def __str__(self):
		return 'Unknown variable'
