# Bernardo Estrada Fuentes
# A01704320
# To run this script, you need to have the test_cases_1 folder in the same directory as this script and TerminalesYNoTerminales.py
# You can run python TerminalesYNoTerminales.test.py to run all tests or python TerminalesYNoTerminales.test.py n to run a single test n

import os
from sys import argv
import TerminalesYNoTerminales as tnt
import Utils.SplitRows as sr
NUMBER_OF_TESTS = 5

def runSingleTest(i: int, indent = False):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  if i > NUMBER_OF_TESTS or i <= 0:
    print("Test number out of range")
    return

  with open(dir_path + '/../test_cases/1/input%i.txt' % i) as f:
    lines = f.read().strip().splitlines()
  lines.pop(0)

  with open(dir_path + '/../test_cases/1/output%i.txt' % i) as f:
    expected = f.read().strip().splitlines()

  [terminal, nonTerminal] = tnt.parseTerminalsAndNonTerminals(lines)
  terminal = [x for x in terminal if x != sr.EPSILON]

  expectedTerminal = expected[0].split(': ')[1].split(', ')
  expectedNonTerminal = expected[1].split(': ')[1].split(', ')

  prefix = "  " if indent else ""
  if sorted(terminal) == sorted(expectedTerminal) and sorted(nonTerminal) == sorted(expectedNonTerminal):
    print(prefix + "Test %i passed" % i)
  else:
    print(prefix + "Test %i failed" % i)
    print(prefix + "  ExpectedTerminal:\t", expectedTerminal)
    print(prefix + "  OutputTerminal:\t", terminal)
    print(prefix + "  ExpectedNonTerminal:\t", expectedNonTerminal)
    print(prefix + "  OutputNonTerminal:\t", nonTerminal)

def test(indent = False):
  if (len(argv) == 2 and argv[1].isdigit()):
    runSingleTest(int(argv[1]))
  else:
    for i in range(1, NUMBER_OF_TESTS + 1):
      runSingleTest(i, indent)

if __name__ == "__main__":
  test()
