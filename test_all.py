import sys

sys.path.append('.')

import tests.TerminalesYNoTerminales as tyntTest
import tests.FirstsYFollows as fyfTest

def main():
  print("TerminalesYNoTerminales:")
  tyntTest.test(indent = True)
  print()
  print("FirstYFollows:")
  fyfTest.test(indent = True)

if __name__ == "__main__":
  main()