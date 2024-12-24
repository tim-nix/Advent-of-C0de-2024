#

from collections import deque
from functools import cache
from itertools import pairwise


# Read in the data file and convert it to a list
# of strings.
def readFile(filename):
   lines = []
   try:
      with open(filename, "r") as file:
         line = file.readline()
         while line:
            lines.append(line.replace('\n', ''))
            line = file.readline()

         file.close()
            
   except FileNotFoundError:
      print("Error: File not found!")
   except:
      print("Error: Can't read from file!")
   
   return lines


num_pad = {
    "0": [("2", "^"), ("A", ">")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")],
    "3": [("2", "<"), ("6", "^"), ("A", "v")],
    "4": [("1", "v"), ("5", ">"), ("7", "^")],
    "5": [("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")],
    "6": [("3", "v"), ("5", "<"), ("9", "^")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("7", "<"), ("9", ">")],
    "9": [("6", "v"), ("8", "<")],
    "A": [("0", "<"), ("3", "^")],
}
dir_pad = {
    "^": [("A", ">"), ("v", "v")],
    "<": [("v", ">")],
    "v": [("<", "<"), ("^", "^"), (">", ">")],
    ">": [("v", "<"), ("A", "^")],
    "A": [("^", "<"), (">", "v")],
}


def bfs(u, v, g):
   q = deque([(u, [])])
   seen = {u}
   shortest = None
   res = []
   while q:
      cur, path = q.popleft()
      if cur == v:
         if shortest is None:
            shortest = len(path)
         if len(path) == shortest:
            res.append("".join(path + ["A"]))
         continue
      if shortest and len(path) >= shortest:
         continue
      for nei, d in g[cur]:
         seen.add(nei)
         q.append((nei, path + [d]))

   return res


@cache
def dfs(code, robot, isNumPad):
   if isNumPad:
      g = num_pad
   else:
      g = dir_pad
   
   res = 0
   code = "A" + code
   for u, v in pairwise(code):
      paths = bfs(u, v, g)
      if robot == 0:
         res += min(map(len, paths))
      else:
         res += min(dfs(path, robot - 1, False) for path in paths)

   return res


if __name__ == '__main__':
   # Read the file input as a list of strings.
   codes = readFile("input21b.txt")

   complexity = 0
   # Iterate through each door code.
   for code in codes:
      min_length = dfs(code, 25, True)

      # Calculate the complexity of this sequence and
      # add it to the sum.
      code_num = ''.join(code[:-1])
      complexity += int(code_num) * min_length

   # Display the results.
   print('complexity = ' + str(complexity))
