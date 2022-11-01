# Bernardo Estrada Fuentes
# A01704320

# Inputs:
# 5
# goal -> A
# A -> (A)
# A -> two
# two -> a
# two -> b

# Outputs:
# goal => FIRST = {(, a, b}, FOLLOW = {$}
# A => FIRST = {(, a, b}, FOLLOW = {$, )}
# two => FIRST = {a, b}, FOLLOW = {$, )}

from math import prod
from typing import List
import TerminalesYNoTerminales.TerminalesYNoTerminales as tnt
import Utils.SplitRows as sr

class FirstAndFollow:
  def __init__(self, rows: List[str]):
    [self.t, self.nt] = tnt.parseTerminalsAndNonTerminals(rows)
    self.result = {}
    self.productions = {}
    self.LL1 = True
    for k in self.nt:
      self.productions[k] = []
      self.result[k] = {
        'first': set(),
        'follow': set(),
        'calculatedFirst': False,
        'calculatedFollow': False
      }
    [leftList, rightList] = sr.parseRowsToLists(rows, False)
    for (l, r) in zip(leftList, rightList):
      self.addToProductions(l, r)


# 6
# E -> E + T
# E -> T
# T -> T * F
# T -> F
# F -> id
# F -> (E)

# E = > FIRST = {id, (}, FOLLOW={$, +,)}
# T = > FIRST = {id, (}, FOLLOW={$, +, *,)}
# F = > FIRST = {id, (}, FOLLOW={$, +, *,)}
# LL(1)? No

  def addToProductions(self, key, value):
    self.productions[key].append(value)

  def getResult(self):
    return self.result

  def resultToString(self):
    resStr = ""
    for k in self.result:
      resStr += '{0} => FIRST = {1}, FOLLOW = {2}\n'.format(
        k,
        '{' + ','.join((self.result[k]['first'])) + '}',
        '{' + ','.join((self.result[k]['follow'])) + '}'
      )
    return resStr #.replace('{}', '{$}')

  def calculateFirst(self, productor):
    if productor in self.t: return set([productor])
    if self.result[productor]['calculatedFirst']: return self.result[productor]['first']

    if len(self.productions[productor]) != 0:
      for prod in self.productions[productor]:
        token = prod[0]
        if token in self.t:
          self.result[productor]['first'].add(token)
        elif token in self.nt and token != productor:
          tokenFirsts = self.calculateFirst(token)
          self.result[productor]['first'] |= tokenFirsts
      self.result[productor]['calculatedFirst'] = True
      return self.result[productor]['first']
    self.result[productor]['first'] = set()
    return set()

  def calculateFirsts(self):
    for k in self.productions:
      if(not self.result[k]['calculatedFirst']):
        self.calculateFirst(k)

  def calculateFollow(self, curr):
    if curr in self.t: return set([curr]) if curr != sr.EPSILON else set()
    if self.result[curr]['calculatedFollow']: return self.result[curr]['follow']

    for productor in self.productions:
      for production in self.productions[productor]:
        if curr in production:
          currIndex = production.index(curr)
          prodLen = len(production)
          if currIndex == prodLen - 1:
            self.result[curr]['follow'] |= self.calculateFollow(productor) if productor != curr else set()
          else:
            nextToken = production[currIndex + 1]
            self.result[curr]['follow'] |= set(self.calculateFirst(nextToken)).difference(set([sr.EPSILON]))
            if nextToken in self.nt and sr.EPSILON in self.result[nextToken]['first']:
              self.result[curr]['follow'] |= self.calculateFollow(productor)
    self.result[curr]['calculatedFollow'] = True
    return self.result[curr]['follow']

  
  def calculateFollows(self):
    firstProduction = next(iter(self.productions))
    self.result[firstProduction]['follow'].add('$')
    for prod in self.productions:
      self.calculateFollow(prod)
  
  def isLL1(self):
    return self.isLL1

  def calculateIsLL1(self):
    for k in self.productions:
      if self.result[k]['first'].intersection(self.result[k]['follow']) != set():
        self.LL1 = False
        return False
    
    self.LL1 = True
    return True

def main():
  rows: List[str] = []
  n = int(input("Enter the number of rows: "))
  for i in range(n):
    rows.append(input())

  firstAndFollow = FirstAndFollow(rows)

  print()
  print(firstAndFollow.productions)
  firstAndFollow.calculateFirsts()
  firstAndFollow.calculateFollows()
  print()
  print(firstAndFollow.resultToString())

if __name__ == "__main__":
  main()
