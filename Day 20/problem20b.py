# This program takes as input a map of a racetrack
# with a marked starting point (S) and end point (E).
# From the shortest path (each step taking 1 pico-
# second), a cheat allows the runner to travel through
# walls for some distance (within 20 steps away).
# Determine all of the cheats and the time saved for
# each cheat. Then, sum the total number of cheats
# that would save at least 100 picoseconds


# Define constants.
MIN_CHEAT = 2
MAX_CHEAT = 20
SAVE_THRESHOLD = 100 # 50

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


# Generate a set of all endpoints within a given
# Manhattan distance from the starting location.
def genEndpoints(track, location):
   # For storing endpoints.
   endpoints = set()

   # The legal vertex values.
   x_range = set([ x for x in range(len(track[0])) ])
   y_range = set([ y for y in range(len(track)) ])
   
   x, y = location

   # Iterate through all possible x,y locations and
   # store those that are within MAX_CHEAT Manhattan
   # distance of location and not a wall (#).
   for offset_y in range(-MAX_CHEAT, MAX_CHEAT + 1):
      for offset_x in range(-MAX_CHEAT, MAX_CHEAT + 1):
         end_x = x + offset_x
         end_y = y + offset_y
         distance = abs(offset_x) + abs(offset_y)
         if (distance >= MIN_CHEAT) and (distance <= MAX_CHEAT):
            if (end_x in x_range) and (end_y in y_range) and (track[end_y][end_x] != '#'):
               endpoints.add((end_x, end_y))

   # Return the set of endpoints.
   return endpoints


            
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

   # For each vertex in the path, calculate all
   # possible cheat endpoints and the time savings for
   # each. Only store those whose savings are over the
   # SAVE_THRESHOLD.
   for key in path:
      # Generate list of cheat end locations
      endpoints = genEndpoints(track, key)
      for point in endpoints:
         if path[point] > path[key]:
            diff_x = abs(point[0] - key[0])
            diff_y = abs(point[1] - key[1])
            saved = (path[point] - path[key]) - (diff_x + diff_y)
            if saved >= SAVE_THRESHOLD:
               if saved not in cheats:
                  cheats[saved] = 1
               else:
                  cheats[saved] += 1

   # Sum the total number of cheats saving at least
   # SAVE_THRESHOLD picoseconds.
   num_cheats = 0
   for key in cheats:
      if key >= SAVE_THRESHOLD:
         num_cheats += cheats[key]

   # Display the results.
   print('Number of cheats saving at least ' + str(SAVE_THRESHOLD) + ' picoseconds = ' + str(num_cheats))
   

   
