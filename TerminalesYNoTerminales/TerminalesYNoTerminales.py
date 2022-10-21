# Bernardo Estrada Fuentes
# A01704320

# Input example:
# 5
# goal -> A
# A -> ( A )
# A -> two
# two -> a
# two -> b

# Output Example:
# Terminal: +, *, (, ), id
# Non terminal: E, EPrime, T, TPrime, F

import sys
from typing import List

sys.path.append('.')

import Utils.SplitRows as sr

def parseTerminalsAndNonTerminals(rows: List[str]):
  terminals: List[str] = []
  nonTerminals: List[str] = []

  [leftList, rightList] = sr.parseRowsToLists(rows)

  # Check if the right side is a terminal or a non terminal
  terminals = [x for x in rightList if x not in leftList]
  nonTerminals = leftList

  return [terminals, nonTerminals]



if __name__ == "__main__":
  rows: List[str] = []
  n = int(input("Enter the number of rows: "))
  for i in range(n):
    rows.append(input())

  [terminals, nonTerminals] = parseTerminalsAndNonTerminals(rows)
  print("Terminal: ", ', '.join(terminals))
  print("Non terminal: ", ', '.join(nonTerminals))
