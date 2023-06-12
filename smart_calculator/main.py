import re
from errors import *


class CommandManager:
	def execute(self, command):
		if command == "exit":
			raise Exit()
		elif command == 'help':
			return "Help text"
		else:
			raise UnknownCommand()


class Calculator:
	def __init__(self):
		self.operators = {'+', '-', '*', '/', '(', ')', '^'}
		self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
		self.memory = {}
	
	def save_to_memory(self, exp):
		exp = exp.replace(" ", "").split("=")
		
		if len(exp) > 2:
			raise InvalidAssignment()
		
		for sign in exp[0]:
			if sign.isalpha():
				continue
			else:
				raise InvalidIdentifier()
		
		if len(exp) == 1:
			return
		
		try:
			float(exp[1])
		except (ValueError, IndexError):
			if exp[1] not in self.memory.keys():
				raise InvalidAssignment()
		
		self.memory[exp[0]] = self.memory[exp[1]] if exp[1] in self.memory.keys() else exp[1]
	
	def text_to_infix(self, text):
		if "**" in text or "//" in text:
			raise InvalidExpression()
		
		text = text.replace(" ", "")
		
		text = re.sub(r"\++", "+", text)
		
		text = re.split("(-+)", text)
		for i in range(len(text)):
			if "-" in text[i]:
				if len(text[i]) % 2 == 0:
					text[i] = "+"
				else:
					text[i] = "-"
		text = "".join(text)
		
		text = re.split("([+\\-*/()])", text)
		
		while "" in text:
			text.remove("")
		
		return text
	
	def infix_to_postfix(self, exp):
		reversed_notation = []
		operators = []
		signs = "+-/*"
		
		for item in exp:
			if item == "(":
				operators.append(item)
			elif item == ")":
				left_missing = True
				while operators:
					if operators[-1] != "(":
						reversed_notation.append(operators.pop())
					else:
						operators.pop()
						left_missing = False
						break
				if left_missing:
					raise InvalidExpression()
			elif item in signs:
				if not operators or operators[-1] == "(" or \
						item in signs[2:] and operators[-1] in signs[:2]:
					operators.append(item)
				else:
					while operators:
						if operators[-1] in signs[:2] and item in signs[2:] or operators[-1] == "(":
							break
						else:
							reversed_notation.append(operators.pop())
					operators.append(item)
			else:
				reversed_notation.append(item)
		
		while operators:
			reversed_notation.append(operators.pop())
		
		if "(" in reversed_notation or ")" in reversed_notation:
			raise InvalidExpression()
		
		return reversed_notation
	
	def evaluate(self, postfix):
		stack = []
		for item in postfix:
			if item.isdigit():
				stack.append(item)
			elif item in self.memory:
				stack.append(self.memory[item])
			elif len(stack) > 1:
				if item == "+":
					b = int(stack.pop())
					a = int(stack.pop())
					stack.append(a + b)
				elif item == "-":
					b = int(stack.pop())
					a = int(stack.pop())
					stack.append(a - b)
				elif item == "*":
					b = int(stack.pop())
					a = int(stack.pop())
					stack.append(a * b)
				elif item == "/":
					b = int(stack.pop())
					a = int(stack.pop())
					stack.append(a // b)
		return stack[0]
	
	def calculate(self, exp):
		if '=' in exp:
			self.save_to_memory(exp)
			return
		
		if exp in self.memory.keys():
			return self.memory[exp]
		
		infix = self.text_to_infix(exp)
		if len(infix) == 1:
			try:
				print(int(exp))
			except ValueError:
				if self.save_to_memory(exp) is None:
					raise UnknownVariable()
				else:
					raise InvalidExpression()
		postfix = self.infix_to_postfix(infix)
		try:
			return self.evaluate(postfix)
		except (TypeError, ValueError):
			raise InvalidExpression()


calculator = Calculator()
commandManager = CommandManager()

while True:
	try:
		text = input().strip()
		result = ""
		isExit = False
		
		if text == "":
			continue
		elif text.startswith("/"):
			result = commandManager.execute(text[1:])
		else:
			result = calculator.calculate(text)
		
		if result is not None:
			print(result)
	except Exception as e:
		print(e)
		if isinstance(e, Exit):
			break
