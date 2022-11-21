import copy
from typing import List
import TerminalesYNoTerminales as tnt
import FirstsYFollows as fyf
import Utils.SplitRows as sr

class SLRTables:
  def __init__(self, rows: List[str]):
    fnf = fyf.FirstAndFollow(rows)
    fnf.calculateFirsts()
    fnf.calculateFollows()
    prod = next(iter(fnf.productions))
    i0 = I(0, [IProd(prod+'\'', prod, fnf)])
    i = 1
    ISections = [i0]
    for iSection in ISections:  
      for p in iSection.lookahead:
        if p != '$':
          newI = iSection.getFollowingI(p, i)
          try:
            existingI = ISections.index(newI)
            iSection.paths[p] = existingI
          except:
            ISections.append(newI)
            i += 1
    self.ISections = ISections
    self.fnf = fnf

  def generateTable(self):
    actions: List[List[str]] = []
    for i, iSection in enumerate(self.ISections):
      actions.append([])
      for p in [*self.fnf.t, '$']:
        try:
          shift = str(iSection.paths[p])
          shift = 'S'+shift if shift != 'ACC' else shift
          actions[i].append(shift)
        except:
          actions[i].append('  ')

    goto: List[List[str]] = []
    for i, iSection in enumerate(self.ISections):
      goto.append([])
      for p in self.fnf.nt:
        try:
          shift = 'S'+str(iSection.paths[p])
          goto[i].append(shift)
        except:
          goto[i].append('  ')

    self.actions = actions
    self.goto = goto
    return goto, actions

  def printISections(self):
    for iSection in self.ISections:
      print(iSection)
  def printTable(self):
    table = 'I ||  '
    table += ' |  '.join([*self.fnf.t, '$']) + '  || '
    table += ' |  '.join(self.fnf.nt) + '\n'
    table += '-'*(len(table)) + '\n'

    for i in range(len(self.ISections)):
      table += str(i) + ' || '
      table += ' | '.join(self.actions[i])
      table += ' || ' if self.actions[i][-1] == "ACC" else '  || '
      table += ' | '.join(self.goto[i]) + '\n'
    print(table)

class IProd:
  def __init__(self, productor, product, fnf: fyf.FirstAndFollow, dot = 0):
    self.final = False
    self.dot = dot
    self.productor = productor
    self.product = product
    self.fnf = fnf
    if self.dot >= len(self.product):
      self.final = True

  def __repr__(self) -> str:
    return self.__str__()

  def __str__(self) -> str:
    res: str = self.productor
    res += " ->"
    for i, p in enumerate(self.product):
      if i == self.dot: res += " ."
      res += " " + p
    if self.final: res += " ."
    return res

  def __eq__(self, __o: object) -> bool:
    if not isinstance(__o, IProd): return False
    return self.productor == __o.productor and self.product == __o.product and self.dot == __o.dot
  
  # Next productor to add to the stack
  def getNextProductor(self):
    if self.final:
      return '$'
    return self.product[self.dot]
  def getNextToken(self):
    if self.dot < len(self.product):
      return self.product[self.dot]
    return '$'

  def moveAhead(self):
    self.dot += 1
    if self.dot >= len(self.product):
      self.final = True

class I:
  def __init__(self, number, firstProds: List[IProd]):
    self.number = number
    self.done = False
    self.nextIsTerminal = False
    self.fnf = firstProds[0].fnf
    if [p.final for p in firstProds].count(True) == len(firstProds):
      self.done = True
    self.kernel = firstProds
    self.prods = firstProds
    self.paths = { }
    self.nextProductors = [p.getNextProductor() for p in firstProds]
    # if self.nextProductor == '$':
    #   self.nextIsTerminal = True
    self.generateNecessaryProds()
    self.lookahead = self.followingTokens()
    if (len(self.lookahead) == 0):
      self.done = True

  def __str__(self) -> str:
    res = "I" + str(self.number) + "\n  "
    res += "\n  ".join(str(pr) for pr in self.prods)
    return res
  def __repr__(self) -> str:
    return self.__str__()

  def __eq__(self, __o: object) -> bool:
    if not isinstance(__o, I): return False
    return self.kernel == __o.kernel

  def generateNecessaryProds(self):
    for productor in self.nextProductors:
      if productor != '$' and not self.done and productor not in self.fnf.t:
        for prod in self.fnf.productions[productor]:
          newProd = IProd(productor, prod, self.fnf)
          if newProd not in self.prods:
            self.prods.append(newProd)
      elif productor == '$':
        self.paths['$'] = 'ACC'
    
  def followingTokens(self):
    tokens = []
    for prod in self.prods:
      tokens.append(prod.getNextToken())
    return list(dict.fromkeys(tokens))

  def getFollowingI(self, token, n):
    newProds = []
    for prod in self.prods:
      if prod.getNextToken() == token and prod not in newProds:
        newProds.append(copy.deepcopy(prod))
    for p in newProds:
      p.moveAhead()
    newI = I(n, newProds)
    self.lookahead = self.followingTokens()
    newI.generateNecessaryProds()
    self.paths[token] = newI.number
    if list(self.paths) == self.lookahead:
      self.done = True
    return newI

if __name__ == "__main__":
  rows: List[str] = []
  stringTests: List[str] = []
  nums = input("Enter the number of rows: ").split()
  n = int(nums[0])
  strs = int(nums[1])
  for i in range(n):
    rows.append(input())
  for i in range(strs):
    stringTests.append(input())

  print()
  table = SLRTables(rows)
  table.generateTable()
  table.printTable()

