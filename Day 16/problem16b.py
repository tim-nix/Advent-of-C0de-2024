# Find the lowest cost associated with traveling in a
# graph. The Reindeer start on the Start Tile (marked
# S) facing East and need to reach the End Tile
# (marked E). They can move forward one tile at a time
# (increasing their score by 1 point), but never into
# a wall (#). They can also rotate clockwise or
# counterclockwise 90 degrees at a time (increasing
# their score by 1000 points).

# Along all possible best paths through the maze; that
# is, multiple paths can have the same lowest cost,
# determine which tiles are part of any best path
# through the maze, including the S and E tiles.

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


# Convert the list of strings representing the maze
# into a list of list of characters representing the
# maze.
def parseInput(values):
   maze = []
   for line in values:
      maze.append(list(line))

   return maze


# Find a location within the maze (used to determine
# the start (S) and the end (E) of the maze).
def findLocation(maze, marker):
   for y in range(len(maze)):
      for x in range(len(maze[y])):
         if maze[y][x] == marker:
            return (x, y)

   return None


# Generate the set of vertices for the graph by
# iterating through each position and, if the
# position has more than 2 paths to it, add it
# to a set of vertices.
def getVertices(maze):
   vertices = set()
   # Iterate through each x, y in the maze.
   for y in range(len(maze)):
      for x in range(len(maze[y])):
         if maze[y][x] != '#':
            paths = 0
            # Check each cardinal direction for a path.
            if maze[y][x - 1] != '#':
               paths += 1

            if maze[y + 1][x] != '#':
               paths += 1

            if maze[y][x + 1] != '#':
               paths += 1

            if maze[y - 1][x] != '#':
               paths += 1

            # If more than two paths lead to the point
            # then add it to the set of vertices.
            if paths == 1:
               vertices.add((x, y))
            elif (paths == 2) and (maze[y][x - 1] == '#') and (maze[y][x + 1] != '#'):
               vertices.add((x, y))
            elif (paths == 2) and (maze[y + 1][x] == '#') and (maze[y - 1][x] != '#'):
               vertices.add((x, y))
            elif (paths == 2) and (maze[y][x + 1] == '#') and (maze[y][x - 1] != '#'):
               vertices.add((x, y))
            elif (paths == 2) and (maze[y - 1][x] == '#') and (maze[y + 1][x] != '#'):
               vertices.add((x, y))
            elif paths > 2:
               vertices.add((x, y))

   # Return the set of vertices.
   return list(vertices)


# Calculate the length of the straight path from the
# start (of the path) vertex to the end (of the path)
# verted. This path length is stored in the adjacency
# matrix representing the maze.
def getPathLength(maze, start, end):
   s_x, s_y = start
   e_x, e_y = end
   if (abs(s_x - e_x) > 0) and (abs(s_y - e_y) > 0):
      return 0
   else:
      # Iterate through the sequence of non-wall
      # spaces in the same direction until either a
      # wall is encountered or the end vertex is
      # reached.
      length = 0
      edge_exists = False
      while maze[s_y][s_x] != '#' and ((s_x, s_y) != end):
         if (abs(s_y - e_y) == 0) and (s_x < e_x):
            s_x += 1
         elif (abs(s_y - e_y) == 0) and (s_x > e_x):
            s_x -= 1
         elif (abs(s_x - e_x) == 0) and (s_y < e_y):
            s_y += 1
         elif (abs(s_x - e_x) == 0) and (s_y > e_y):
            s_y -= 1

         # Increment the path length.
         length += 1

      # If a wall is encountered, then no edge exists.
      if maze[s_y][s_x] == '#':
         return 0
      # Otherwise, return the edge length.
      else:
         return length
   

# Generate an adjacency matrix for the given maze.
def genGraph(maze, vertices):
   # Create an empty adjacency matrix of correct size.
   graph = [ [ 0 for x in range(len(vertices)) ] for y in range(len(vertices)) ]
   
   for i in range(len(vertices) - 1):
      for j in range(i + 1, len(vertices)):
         length = getPathLength(maze, vertices[i], vertices[j])
         # The graph is undirected, so add both ways.
         graph[j][i] = length
         graph[i][j] = length

   # Return the constructed adjacency matrix.
   return graph


# Determine the number tiles that are part of any best
# path through the maze, including the S and E tiles.
def searchGraph(graph, vertices, start, end):
   # For each vertex to visit, keep track of its
   # position, direction faced to reach it, and the
   # cost of reaching it.
   toVisit = [ (start, 'E', 0) ]
   visited = set()
   paths = dict()

   # Generate a dictionary in which each key is a
   # vertex and its assigned value is the vertex
   # along the shortest path back to the start.
   while len(toVisit) > 0:
      # Find the vertex to visit with the lowest cost.
      min_cost = toVisit[0][2]
      min_v = 0
      for i in range(len(toVisit)):
         if toVisit[i][2] < min_cost:
            min_cost = toVisit[i][2]
            min_v = i

      current, facing, cost = toVisit.pop(min_v)

      # Visit the vertex, if not already visited.
      if current not in visited:
         # Add the vertex to the visited set.
         visited.add(current)

         # Convert the vertex to the index in the
         # adjacency matrix.
         v_i = vertices.index(current)

         # Find directly connected neighbors.
         for v_j in range(len(graph[v_i])):
            if graph[v_i][v_j] > 0:
               next_v = vertices[v_j]
               
               cost_delta = 0

               # Determine change in facing to
               # reach the neighbor.
               if next_v[0] > current[0]:
                  new_facing = 'E'
               elif next_v[0] < current[0]:
                  new_facing = 'W'
               elif next_v[1] < current[1]:
                  new_facing = 'N'
               elif next_v[1] > current[1]:
                  new_facing = 'S'
               
               # Calculate cost from the current
               # vertex to the next vertex.
               new_cost = cost
               if facing != new_facing:
                  new_cost += 1000
               new_cost += graph[v_i][v_j]

               # If the neighbor has not already
               # been visited, add it to visit.
               if next_v not in visited:
                  # Keep track of the cost to reach
                  # the next node, and that it was
                  # reached through the current node.
                  if next_v not in paths:
                     paths[next_v] = (new_cost, current)
                  # If the path to reach the next node
                  # is lower through the current node,
                  # then change the cost and the path.
                  elif paths[next_v][0] > new_cost:
                     paths[next_v] = (new_cost, current)
                  # If another path is found that costs
                  # the same, then track it, as well.
                  elif paths[next_v][0] == new_cost:
                     preds = list(paths[next_v])
                     preds.append(current)
                     paths[next_v] = tuple(preds)
                     
                  toVisit.append((next_v, new_facing, new_cost))
   
   # Calculate the number of good seats along all
   # possible good routes; that is, the size of the
   # set of tiles.
   toVisit = [ end ]
   visited = set()
   tiles = set()
   tiles.add(end)
   # Visit vertices as long as there are vertices
   # to visit, from the end vertex.
   while len(toVisit) > 0:
      current = toVisit.pop(0)
      # Skip the vertex if it is the start (no entry
      # in paths) or it has already been visited.
      if (current != start) and (current not in visited):
         visited.add(current)
         # Add all predecessor neighbors; that is, all
         # vertices through which the current node is
         # reached along the shortest paths.
         for pred in paths[current][1:]:
            toVisit.append(pred)
            c_x, c_y = current
            p_x, p_y = pred
            # For each edge alone a good path, add
            # all tiles within the edge (all points
            # in the maze along the straight path
            # between the current vertex and its
            # predecessor).
            for y in range(min(c_y, p_y), max(c_y, p_y) + 1):
               for x in range(min(c_x, p_x), max(c_x, p_x) + 1):
                  tiles.add((x, y))

   # Return the number of good seats along the route.
   return len(tiles)


if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input16b.txt")
   maze = parseInput(values)

   #for line in maze:
   #   print(''.join(line))
   #print()

   # Find start and end locations in the maze.
   start = findLocation(maze, 'S')
   end = findLocation(maze, 'E')

   #print('start = ' + str(start))
   #print('end = ' + str(end))

   # Find all maze vertices.
   vertices = getVertices(maze)
   #print('vertices = ' + str(vertices))

   # Generate the adjacency matrix representation of
   # the maze.
   graph = genGraph(maze, vertices)

   # Calculate the number of good seats along all
   # good routes from start to end.
   good_seats = searchGraph(graph, vertices, start, end)

   # Print the number of good seats.
   print('The number of good seats = ' + str(good_seats))
   

   

   
