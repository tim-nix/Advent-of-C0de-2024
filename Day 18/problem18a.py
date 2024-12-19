# The file input is a list of coordinates of 'fallen'
# bytes. The map is an n x n grid. The program finds
# the shortest path from a start location to an end
# location around some number of 'fallen' bytes.

# Defined constants
MAX_GRID = 73 # 9
NUM_BYTES = 1024 # 12

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


# Convert the list of x,y coordinates as strings into
# a list of tuples where the x and y values are
# integers.
def parseInput(values):
   coords = []
   for line in values:
      c = line.split(',')
      coords.append((int(c[0]), int(c[1])))

   # Return the list of integer pairs.
   return coords

# Set up the grid of the map. Grid is bordered by a
# wall (#) and the first NUM_BYTES bytes have 'fallen'
# and blocked the path (marked as walls). All other
# locations are marked as open (.).
def makeGrid(coords):
   # Create open grid bordered by wall (#).
   grid = []
   for y in range(MAX_GRID):
      row = []
      for x in range(MAX_GRID):
         if (x in (0, MAX_GRID - 1)) or (y in (0, MAX_GRID - 1)):
            row.append('#')
         else:
            row.append('.')
            
      grid.append(row)

   # Add the fallen bytes as walls (#).
   for i in range(NUM_BYTES):
      x = coords[i][0]
      y = coords[i][1]
      grid[y + 1][x + 1] = '#'

   # Return the constructed grid.
   return grid


# This function uses breadth-first search to find the
# distance of the shortest path from the start node to
# the end node.
def bfs(grid, start, end):
   toVisit = [ (start, 0) ]
   visited = set()
   
   # Keep searching (search will end when end vertex
   # is 'visited'.
   while True:
      current, distance = toVisit.pop(0)
      if current not in visited:
         visited.add(current)
         x, y = current

         # If the current vertex is the end, then
         # return the distance.
         if (x, y) == end:
            return distance

         # Plan to visit any neighbor that is not a
         # wall and has not already been visited.
         if (grid[y][x - 1] != '#') and ((x - 1, y) not in visited):
            toVisit.append(((x - 1, y), distance + 1))
         if (grid[y][x + 1] != '#') and ((x + 1, y) not in visited):
            toVisit.append(((x + 1, y), distance + 1))
         if (grid[y - 1][x] != '#') and ((x, y - 1) not in visited):
            toVisit.append(((x, y - 1), distance + 1))
         if (grid[y + 1][x] != '#') and ((x, y + 1) not in visited):
            toVisit.append(((x, y + 1), distance + 1))


if __name__ == '__main__':
   # Read and parse input to a list containing the
   # coordinates of the falling bytes.
   values = readFile("input18b.txt")
   coords = parseInput(values)

   # Create the grid representation of the map.
   grid = makeGrid(coords)

   # Start location is the top-left corner (open spot).
   start = (1, 1)
   # End location is the bottom-right corner (open spot).
   end = (MAX_GRID - 2, MAX_GRID - 2)

   # Find and print the number of steps in the
   # shortest path from start to end.
   num_steps = bfs(grid, start, end)
   print('Shortest path contains ' + str(num_steps) + ' steps.')

      
