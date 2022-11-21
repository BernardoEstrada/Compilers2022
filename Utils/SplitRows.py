from typing import List

SPACE_TOKEN = '0x20'
EPSILON = '\' \''

def parseRowsToLists(rows: List[str], flat = True):
  leftList: List[str] = []
  rightList: List[List[str]] = []
  rightListFlat: List[str] = []

  for r in rows:
    a = r.strip().split('->')
    leftList.append(a[0].strip())
    rightList.append(
      a[1]
      .strip()
      .replace(EPSILON, SPACE_TOKEN)
      .split()
    )

  # Switch back space token to space
  for i in rightList:
    for j in i:
      if j == SPACE_TOKEN:
        i[i.index(j)] = EPSILON

  # Remove duplicates & flatten
  if flat:
    leftList = list(dict.fromkeys(leftList))
    rightListFlat = [item for sublist in rightList for item in sublist]
    rightListFlat = list(dict.fromkeys(rightListFlat))
    return [leftList, rightListFlat]

  return [leftList, rightList]
