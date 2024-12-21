# This program takes as input a map of a racetrack
# with a marked starting point (S) and end point (E).
# From the shortest path (each step taking 1 pico-
# second), a cheat allows the runner to travel through
# a wall (one square in width). Determine all of the
# cheats and the time saved for each cheat. Then, sum
# the total number of cheats that would save at least
# 100 picoseconds


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


# Convert the list of strings representing the race-
# track into a list of list of characters representing
# the racetrack.
def parseInput(values):
   return [ list(line) for line in values ]


# Find a location within the maze (used to determine
# the start (S) and the end (E) of the maze).
def findLocation(maze, marker):
   for y in range(len(maze)):
      for x in range(len(maze[y])):
         if maze[y][x] == marker:
            return (x, y)

   return None


# This function uses breadth-first search to find the
# distance of the shortest path from the start node to
# the end node. It returns a set of all vertices along
# this path along with the corresponding distance of
# the vertex from the start node (S).
def bfs(grid, start, end):
   toVisit = [ (start, 0) ]
   visited = set()
   distances = dict()
   
   # Keep searching (search will end when end vertex
   # is 'visited'.
   while len(toVisit) > 0:
      current, distance = toVisit.pop(0)
      if current not in visited:
         visited.add(current)
         distances[current] = distance
         x, y = current

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

   # Return the dictionary of nodes on the path and
   # their corresponding distance from the start node.
   return distances

            
if __name__ == '__main__':
   # Read and parse input to list of lists of char.
   values = readFile("input20b.txt")
   track = parseInput(values)
   
   # Find start and end locations in the track.
   start = findLocation(track, 'S')
   end = findLocation(track, 'E')

   # Find the vertices in the shortest path and their
   # distance from the start node.
   path = bfs(track, start, end)

   # Find the cheats.
   cheats = dict()
   x_range = set([ x for x in range(len(track[0])) ])
   y_range = set([ y for y in range(len(track)) ])
   # For each vertex in the path, check to see if the
   # neighbor two locations away (N, S, E, W) is not
   # a wall and the neighbor one location away is a
   # wall. If so, calculate and store the time saved.
   for key in path:
      x, y = key
      # Check West.
      if (x - 2 in x_range) and (track[y][x - 2] != '#') and (track[y][x - 1] == '#'):
         if path[(x - 2, y)] > path[key]:
            saved = (path[(x - 2, y)] - path[key]) - 2
            if saved not in cheats:
               cheats[saved] = 1
            else:
               cheats[saved] += 1
      # Check East.
      if (x + 2 in x_range) and (track[y][x + 2] != '#') and (track[y][x + 1] == '#'):
         if path[(x + 2, y)] > path[key]:
            saved = (path[(x + 2, y)] - path[key]) - 2
            if saved not in cheats:
               cheats[saved] = 1
            else:
               cheats[saved] += 1
      # Check North.
      if (y - 2 in y_range) and (track[y - 2][x] != '#') and (track[y - 1][x] == '#'):
         if path[(x, y - 2)] > path[key]:
            saved = (path[(x, y - 2)] - path[key]) - 2
            if saved not in cheats:
               cheats[saved] = 1
            else:
               cheats[saved] += 1
      # Check South.
      if (y + 2 in y_range) and (track[y + 2][x] != '#') and (track[y + 1][x] == '#'):
         if path[(x, y + 2)] > path[key]:
            saved = (path[(x, y + 2)] - path[key]) - 2
            if saved not in cheats:
               cheats[saved] = 1
            else:
               cheats[saved] += 1

   # Sum the total number of cheats saving at least
   # 100 picoseconds.
   hundredPlus = 0
   for key in cheats:
      if key >= 100:
         hundredPlus += cheats[key]

   print('Number of cheats saving at least 100 picoseconds = ' + str(hundredPlus))

   
