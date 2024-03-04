import typing
import math
import random
from common import logger

ODD_MOVES = [1, 3, 5, 7, 9]
EVEN_MOVES = [2, 4, 6, 8]

# random.seed(0)

class Board:
	state = []
	rule: list = None
	
	myNumbersLeft = []
	negativeUsed: bool = None
	size: int = None
	odd: bool = None

	def __init__(self, size: int, rules: list):
		self.size = size
		self.rules = rules.copy()

		self.reset()

	def reset(self):
		"""
		This more or less defines how the board is set up and the rules used for calculating stuff works.
		"""

		self.state = [i-i for i in range(self.size**2)]
		self.myNumbersLeft = []
		self.enemyNumbersLeft = []
		self.negativeUsed = False
		self.odd = None

	def printBoard(self):
		rows = []
		
		for i in range(0, len(self.state)):
			rowIndex = math.floor(i / self.size)
			if len(rows)-1 < rowIndex:
				rows.append([])
			row = rows[rowIndex]
			row.append((self.state[i]))
		
		
		logger.info("-" * 14)

		for x in rows:
			# https://docs.python.org/3/library/stdtypes.html#printf-style-bytes-formatting
			rowStr = "% 3d % 3d % 3d" % (x[0], x[1], x[2])
			logger.info(rowStr)
		
		logger.info("-" * 14)

	def printBoardAsInputString(self):
		logger.info(",".join([str(x) for x in self.state]))


	def getRulesInvolvingPosition(self, position: int):
		selected = []

		for r in self.rules:
			if r.a == position or r.b == position or r.c == position:
				selected.append(r)
		

	def isValidMove(self, oldState: list, newState: list) -> typing.Tuple[bool, str|None]:
		change = None
		for i,v in enumerate(newState):
			if v != oldState[i]:
				if change:
					return False, f"Illegal number of changes."
				change = i
		
		if change is None:
			return False, "No move was made."

		# Check if they're trying to replace a number.
		if oldState[change] != 0:
			return False, "Illegally trying to change an existing space."
		
		# Check if they're allowed to use that number.
		numberUsed = newState[change]
		isTheirNumber = False
		if self.odd:
			# They're even.
			isTheirNumber = abs(numberUsed) in EVEN_MOVES
		else:
			# They're odd.
			isTheirNumber = abs(numberUsed) in ODD_MOVES
		
		if not isTheirNumber:
			return False, f"Using a number ({numberUsed}) that isn't theirs."
		
		# Check if it's negative and negative is available.
		if numberUsed < 0 and self.negativeUsed:
			return False, "Negative has already been used."
		
		# Check if they're trying to use a number that's already been used.
		for v in oldState:
			if abs(v) == abs(numberUsed):
				return False, f"Using a number that's already been placed."
		
		self.enemyNumbersLeft.remove(abs(numberUsed))

		return True, None
		
	def updateState(self, newState: list) -> bool:
		"""

		:return: Gameover.
		"""
		self.state = newState

		for rule in self.rules:
			a = self.state[rule.a]
			b = self.state[rule.b]
			c = self.state[rule.c]

			if a < 0 or b < 0 or c < 0:
				self.negativeUsed = True

			if a > 0 and b > 0 and c > 0 and a + b + c == 15:
				logger.critical(f"Game is over. {a} + {b} + {c} = 15")
				return True

		return False

	def chooseMove(self) -> typing.Tuple[int, int]:
		
		for rule in self.rules:
			a = self.state[rule.a]
			b = self.state[rule.b]
			c = self.state[rule.c]

			# Check how many spaces this rule has open.
			openSpaces = []
			if a == 0: openSpaces.append(rule.a)
			if b == 0: openSpaces.append(rule.b)
			if c == 0: openSpaces.append(rule.c)
			
			# logger.debug(f"Rule evaluation: Open spaces: {len(openSpaces)} | rule.a={rule.a} rule.b={rule.b} rule.c={rule.c}")
			
			if len(openSpaces) == 0:
				logger.debug(f"Skipping rule | rule.a={rule.a} rule.b={rule.b} rule.c={rule.c}")
				# Skipping this rule since it's useless.
				continue

			if len(openSpaces) == 1:
				logger.debug(f"Evaluating rule | rule.a={rule.a} rule.b={rule.b} rule.c={rule.c}")
				openPosition = openSpaces[0]

				"""
				if openPosition is None:
					logger.critical(f"Unable to find an open position on rule: rule.a={rule.a} rule.b={rule.b} rule.c={rule.c}")
					self.printBoard()
				"""

				# Let's look for a winning move first.
				ruleValue = a + b + c
				neededValue = 15 - ruleValue
				# 9+7 = 16, 15-16=-1

				logger.debug(f"\tCurrent rule value: {ruleValue} | Needed value: {neededValue}")

				if abs(neededValue) in self.myNumbersLeft:
					logger.info("\tWe have the needed value in our available numbers.")
					# The value matches up, but check if it's negative and if a negative is available.
					moveValid = neededValue > 0 or (neededValue < 0 and not self.negativeUsed)
					
					if moveValid:
						logger.info("Winning.")
						return neededValue, openPosition
					else:
						logger.info("\t\tWe don't have a negative though.")
				
				# We didn't find a winning move.
				# Let's see if we need to deny a win.
				if abs(neededValue) in self.enemyNumbersLeft:
					logger.info("\tThe enemy has the needed value.")
					# The enemy might be able to do something here.
					theyCanWin = neededValue > 0 or (neededValue < 0 and not self.negativeUsed)
					
					if theyCanWin:
						logger.info("\t\tDenying win.")
						# Just place something here.
						# blocker = self.myNumbersLeft[math.randint(1, len(self.myNumbersLeft)) - 1]
						blocker = random.choice(self.myNumbersLeft)
						if not self.negativeUsed:
							blocker = -blocker
						
						return blocker, openPosition
					else:
						logger.info("\tThey don't have a negative though.")
		

		# We didn't reach a conclusion yet.
		# Do something random.
		openPositions = []
		for i,v in enumerate(self.state):
			if v == 0:
				openPositions.append(i)
		

		if len(openPositions) == 0:
			return None, None

		return random.choice(self.myNumbersLeft), random.choice(openPositions)

			

	def proposeState(self, desiredState: list):
		logger.debug(f"updateState: {desiredState}")

		# Make sure we know what side we're on if it's the first state update.
		skipCheck = False
		if self.odd is None:
			logger.info("Checking what side we are on.")

			self.odd = all(x == 0 for x in desiredState)
			if self.odd:
				skipCheck = True
				logger.info("\tLooks like we're playing as odd.")
				self.myNumbersLeft = ODD_MOVES.copy()
				self.enemyNumbersLeft = EVEN_MOVES.copy()
				
			else:
				logger.info("\tLooks like we're playing as even.")
				self.myNumbersLeft = EVEN_MOVES.copy()
				self.enemyNumbersLeft = ODD_MOVES.copy()
		

		# Check if the move is valid.
		(isValidMove, reason) = self.isValidMove(self.state, desiredState)
		if skipCheck is False and not isValidMove:
			logger.critical(f"Not a valid move: {reason}")
			return

		gameOver = self.updateState(desiredState)
		self.printBoard()

		if gameOver:
			exit(0)
		
		# Come up with our move.
		logger.info("Thinking of a move...")
		
		value, position = self.chooseMove()
		if value == None:
			logger.info("Board is full?")
			return

		self.state[position] = value
		if value < 0:
			self.negativeUsed = True
		self.myNumbersLeft.remove(abs(value))
		
		self.printBoard()
		self.printBoardAsInputString()
