# Bernardo Estrada Fuentes
# A01704320
# To run this script, you need to have the test_cases_2 folder in the same directory as this script and FirstsYFollows.py
# You can run python FirstsYFollows.test.py to run all tests or python FirstsYFollows.test.py n to run a single test n

import os
from sys import argv
import FirstsYFollows as ff
import re
NUMBER_OF_TESTS = 5


def runSingleTest(i: int, indent = False):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  if i > NUMBER_OF_TESTS or i <= 0:
    print("Test number out of range")
    return

  with open(dir_path + '/../test_cases/2/input%i.txt' % i) as f:
    lines = f.read().strip().splitlines()
  lines.pop(0)

  with open(dir_path + '/../test_cases/2/output%i.txt' % i) as f:
    expected = f.read().strip().splitlines()

  expectedObj = {}
  for k in range(len(expected)-1):
    l = expected[k].split('=')
    expectedObj[l[0].strip()] = {'FIRST': set(), 'FOLLOW': set()}

    firstSearch = re.search('{(.*)}', l[2])
    followSearch = re.search('{(.*)}', l[3])

    if firstSearch == None or followSearch == None: return -1
  
    expectedObj[l[0].strip()]['FIRST'] = firstSearch[0].replace('{', '').replace('}', '').split(',')
    expectedObj[l[0].strip()]['FOLLOW'] = followSearch[0].replace('{', '').replace('}', '').split(',')

  firstAndFollow = ff.FirstAndFollow(lines)
  firstAndFollow.calculateFirsts()
  firstAndFollow.calculateFollows()
  result = firstAndFollow.resultToString().split('\n')
  resultObj = firstAndFollow.getResult()
  result.pop(-1)
  # result.append('LL(1)? ' + 'Yes' if firstAndFollow.calculateIsLL1() else 'No')

  correct = True
  for k in expectedObj:
    try:
      if set(expectedObj[k]['FIRST']) != set(resultObj[k]['first']):
        correct = False
        break
      if set(expectedObj[k]['FOLLOW']) != set(resultObj[k]['follow']):
        correct = False
        break
    except:
      correct = False
      break

  prefix = "  " if indent else ""
  if correct:
    print(prefix + "Test %i passed" % i)
  else:
    print(prefix + "Test %i failed" % i)
    print(prefix + "  Expected:", expected)
    print(prefix + "  Output:  ", result)

def test(indent = False):
  if (len(argv) == 2 and argv[1].isdigit()):
    runSingleTest(int(argv[1]))
  else:
    for i in range(1, NUMBER_OF_TESTS + 1):
      runSingleTest(i, indent)

if __name__ == "__main__":
  test()
