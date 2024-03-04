import os
import math
import typing
import board
from common import logger
from dataclasses import dataclass

# The gist of how this is supposed to work is using the concept of a Space State Model. 
# ---------
# a | b | c
# d | e | f
# g | h | i
# ---------

# ---------
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8
# ---------

BOARD_SIZE = 3
BOARD_RULES = []

# Board rules do not inherently consider direction and therefore need to have their indexes established ahead of time.
@dataclass
class BoardRule: #typing.TypedDict
	a: int
	b: int
	c: int

# Vertical
BOARD_RULES.append(BoardRule(0, 3, 6))
BOARD_RULES.append(BoardRule(1, 4, 7))
BOARD_RULES.append(BoardRule(2, 5, 8))

# Horizontal
BOARD_RULES.append(BoardRule(0, 1, 2))
BOARD_RULES.append(BoardRule(3, 4, 5))
BOARD_RULES.append(BoardRule(6, 7, 8))

# Diagonal
BOARD_RULES.append(BoardRule(0, 4, 8))
BOARD_RULES.append(BoardRule(2, 4, 6))

gameBoard = None



def spacedInput(prompt):
	return input(("+" * 8) + " " + prompt)

def processInput(input: str):
	pieces = input.split(",")
	if len(pieces) != BOARD_SIZE**2:
		logger.error(f"Board state size is wrong: expected={BOARD_SIZE**2}, got={len(pieces)}")
		return
	
	state = []
	for x in pieces:
		state.append(int(x))
	
	gameBoard.proposeState(state)
	# gameBoard.printBoard()


def main():
	global gameBoard

	gameBoard = board.Board(BOARD_SIZE, BOARD_RULES)
	logger.info("Game has started.")
	while True:
		inputStr = spacedInput("Input: ")
		logger.debug(f"Input received: {inputStr}")
		processInput(inputStr)



# Init
if __name__ == "__main__":
	main()
