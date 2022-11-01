import sys

sys.path.append('.')

import TerminalesYNoTerminales.TerminalesYNoTerminales as tynt
import TerminalesYNoTerminales.TerminalesYNoTerminales_test as tyntTest
import FirstsYFollows.FirstsYFollows as fyf
import FirstsYFollows.FirstsYFollows_test as fyfTest


def main():
  print("Choose a module:")
  choice = int(input("1. Terminales y no terminales\n2. Firsts y follows\n"))
  print()
  test = int(input("1. Main\n2. Test\n")) != 2
  print()

  if choice == 1:
    sys.path.append('TerminalesYNoTerminales')
    tynt.main() if test else tyntTest.test()
  elif choice == 2:
    sys.path.append('FirstsYFollows')
    fyf.main() if test else fyfTest.test()
  else:
    print("Invalid choice")

if __name__ == "__main__":
  main()