# 


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


# Convert the list of strings (from the file input) to
# a list of list of input key presses.
def parseInput(values):
   codes = []
   for v in values:
      codes.append(list(v))

   return codes


# Find the location within the grid (the x, y
# coordinates) of the marker.
def findLocation(grid, marker):
   for y in range(len(grid)):
      for x in range(len(grid[y])):
         if grid[y][x] == marker:
            return (x, y)

   return None


# This function uses breadth-first search to find ALL
# shortest path from the start node to the end node.
# It returns a list of the sequence of directions
# needed to traverse along the shortest path from the
# start to the end.
def bfs(grid, start, end):
   toVisit = [ start ]
   visited = set()
   path = dict()

   y_range = set([ y for y in range(len(grid)) ])
   x_range = set([ x for x in range(len(grid[0])) ])
   # Keep searching (search will end when end vertex
   # is 'visited'.
   while True:
      current = toVisit.pop(0)
      if current not in visited:
         visited.add(current)
         x, y = current

         if current == end:
            break

         # Plan to visit any neighbor that is not
         # blank (B) and has not already been visited.
         if (x - 1 in x_range) and (grid[y][x - 1] != 'B') and ((x - 1, y) not in visited):
            toVisit.append((x - 1, y))
            if (x - 1, y) not in path:
                path[(x - 1, y)] = (current, '<')
         if (x + 1 in x_range) and (grid[y][x + 1] != 'B') and ((x + 1, y) not in visited):
            toVisit.append((x + 1, y))
            if (x + 1, y) not in path:
                path[(x + 1, y)] = (current, '>')
         if (y - 1 in y_range) and (grid[y - 1][x] != 'B') and ((x, y - 1) not in visited):
            toVisit.append((x, y - 1))
            if (x, y - 1) not in path:
                path[(x, y - 1)] = (current, '^')
         if (y + 1 in y_range) and (grid[y + 1][x] != 'B') and ((x, y + 1) not in visited):
            toVisit.append((x, y + 1))
            if (x, y + 1) not in path:
                path[(x, y + 1)] = (current, 'v')

   # From the path, generate the sequence of
   # directions needed navigate the keypad.
   current = end
   sequence = []
   while current != start:
      next_node, direction = path[current]
      sequence.insert(0, direction)
      current = next_node

   # Return the dictionary of nodes on the path and
   # their corresponding distance from the start node.
   return sequence

            
if __name__ == '__main__':
   # Read and parse input to list of lists of char.
   values = readFile("input21a.txt")
   codes = parseInput(values)

   keypad = [ [ '7', '8', '9' ], [ '4', '5', '6' ], ['1', '2', '3' ], [ 'B', '0', 'A' ] ]
   dirpad = [ [ 'B', '^', 'A' ], [ '<', 'v', '>' ] ]

   # First robot pushing numeric keypad to unlock the
   # door.
   locationA = findLocation(keypad, 'A')
   sequences = []
   for code in codes:
      sequence = []
      start = locationA
      for key in code:
         end = findLocation(keypad, key)
         toButton = bfs(keypad, start, end)
         print(toButton)
         sequence += toButton
         sequence.append('A')
         start = end
      sequences.append(sequence)

   for line in sequences[:1]:
      print(''.join(line))
   print()

   """
   # Second robot pushing the directional keypad to
   # control the first robot.
   start = findLocation(dirpad, 'A')
   r1_sequences = []
   for sequence in sequences:
      r1_sequence = []
      for key in sequence:
         end = findLocation(dirpad, key)
         toButton = bfs(dirpad, start, end)
         r1_sequence += toButton
         r1_sequence.append('A')
         start = end
      r1_sequences.append(r1_sequence)

   for r_s in r1_sequences[:1]:
      print(''.join(r_s))
   print()


   # Human pushing the directional keypad to control
   # the second robot.
   start = findLocation(dirpad, 'A')
   r2_sequences = []
   for r1_sequence in r1_sequences:
      r2_sequence = []
      for key in r1_sequence:
         print('next key = ' + key)
         end = findLocation(dirpad, key)
         toButton = bfs(dirpad, start, end)
         print('sequence = ' + ''.join(toButton))
         r2_sequence += toButton
         r2_sequence.append('A')
         start = end
      r2_sequences.append(r2_sequence)

   for r_s in r2_sequences[:1]:
      print(''.join(r_s))

   for r_s in r2_sequences[:1]:
      print(len(r_s))
      
   """
   
   
