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
# wall (#) and the first num_dropped bytes have
# 'fallen' and blocked the path (marked as walls).
# All other locations are marked as open (.).
def makeGrid(coords, num_dropped):
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
   for i in range(num_dropped):
      x = coords[i][0]
      y = coords[i][1]
      grid[y + 1][x + 1] = '#'

   # Return the constructed grid.
   return grid


# This function uses breadth-first search to find if a
# path exists from the start node to the end node.
def bfs(grid, start, end):
   toVisit = [ start ]
   visited = set()
   
   # Keep searching until either the end is found or
   # no vertices are left to search (thus, no path
   # exits from start to end).
   done = False
   while len(toVisit) > 0:
      current = toVisit.pop(0)
      if current not in visited:
         visited.add(current)
         x, y = current

         # If the current vertex is the end, then
         # return the distance.
         if (x, y) == end:
            return True

         # Plan to visit any neighbor that is not a
         # wall and has not already been visited.
         if (grid[y][x - 1] != '#') and ((x - 1, y) not in visited):
            toVisit.append((x - 1, y))
         if (grid[y][x + 1] != '#') and ((x + 1, y) not in visited):
            toVisit.append((x + 1, y))
         if (grid[y - 1][x] != '#') and ((x, y - 1) not in visited):
            toVisit.append((x, y - 1))
         if (grid[y + 1][x] != '#') and ((x, y + 1) not in visited):
            toVisit.append((x, y + 1))

   return False


if __name__ == '__main__':
   # Read and parse input to a list containing the
   # register values and a list containing the
   # program.
   values = readFile("input18b.txt")
   coords = parseInput(values)

   # Start location is the top-left corner.
   start = (1, 1)
   # End location is the bottom-right corner.
   end = (MAX_GRID - 2, MAX_GRID - 2)

   # Use binary search to determine the smallest index
   # of the coords list for which a path does not exit.
   low = NUM_BYTES + 1
   high = len(coords)
   while (low != high):
      # Calculate the middle point
      middle = (low + high) // 2

      # Create the grid representation of the map with
      # middle being the number of fallen bytes in the
      # coords list blocking the path.
      grid = makeGrid(coords, middle)
      
      # Determine if a path exits from start to end.
      path_exists = bfs(grid, start, end)

      # If a path exists then shift down (drop more
      # bytes).
      if path_exists:
         low = middle + 1
      # If a path does not exist then shift left (drop
      # fewer bytes).
      else:
         high = middle

   # Print the result.
   print('The byte ' + str(coords[middle]) + ' blocks the path.')

      
