# Given a garden plot (the file input) calculate
# the area and perimeter of each crop plot. Each
# crop plot grows only a single type of plant,
# indicated by a single letter on the map. When
# multiple garden plots are growing the same type
# of plant and are touching (horizontally or
# vertically), they form a region.

# The area of a plot is simply the number of points
# that the plot contains.

# The perimeter of a region is the number of sides of
# points in the plot that do not touch another point
# in the same plot; that is, the neighboring point
# contains a different type of plant.

# The price of fence required for a region is found by
# multiplying that region's area by its perimeter. The
# total price of fencing all regions on a map is found
# by adding together the price of fence for every
# region on the map.


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


# Convert the list containing strings into a list
# of lists containing characters.
def parseInput(values):
   garden = [ list(x) for x in values ]
   
   return garden


# Recursively determine the points within the plot.
def getPlot(garden, x, y, crop, points):
   # If the point is outside the garden, then done.
   if (x < 0) or (x >= len(garden[0])) or (y < 0) or (y >= len(garden)):
      return points
   # If a different crop => done.
   elif garden[y][x] != crop:
      return points
   else:
      # Add current point to set of visited points
      points.add((x, y))
      
      # For unvisited neighbors, recurse.
      if (x - 1, y) not in points:
         plots = getPlot(garden, x - 1, y, crop, points)
      if (x + 1, y) not in points:
         plots = getPlot(garden, x + 1, y, crop, points)
      if (x, y - 1) not in points:
         plots = getPlot(garden, x, y - 1, crop, points)
      if (x, y + 1) not in points:
         plots = getPlot(garden, x, y + 1, crop, points)

      # Return points within plot.
      return points


# Determine the number of edges for the given convex
# corner. The input point (x, y) is part of the plot.
# Determine if it is an outside corner point for
# multiple edges.
def numConvexCorners(x, y, plot):
   corners = 0
   if ((x - 1, y) not in plot) and ((x, y - 1) not in plot):
      corners += 1
   if ((x - 1, y) not in plot) and ((x, y + 1) not in plot):
      corners += 1
   if ((x + 1, y) not in plot) and ((x, y - 1) not in plot):
      corners += 1
   if ((x + 1, y) not in plot) and ((x, y + 1) not in plot):
      corners += 1

   return corners


# Determine the number of edges for the given concave
# corner. The input point (x, y) is part of the plot.
# Determine if it is an inside corner point for
# multiple edges.
def numConcaveCorners(x, y, plot):
   corners = 0
   if ((x - 1, y) in plot) and ((x, y - 1) in plot) and ((x - 1, y - 1) not in plot):
      corners += 1
   if ((x - 1, y) in plot) and ((x, y + 1) in plot) and ((x - 1, y + 1) not in plot):
      corners += 1
   if ((x + 1, y) in plot) and ((x, y - 1) in plot) and ((x + 1, y - 1) not in plot):
      corners += 1
   if ((x + 1, y) in plot) and ((x, y + 1) in plot) and ((x + 1, y + 1) not in plot):
      corners += 1

   return corners


# Calculate the number of sides for the given plot.
# This is done by determining the corner points and
# the number of edges associated with each corner.
def calcSides(plot):
   # Convert the set of plot points for iteration.
   points = list(plot)

   num_corners = 0
   for p in points:
      x, y = p
      # Handle convex corners
      update = numConvexCorners(x, y, plot)
      num_corners += update

      # Handle concave corners
      update = numConcaveCorners(x, y, plot)
      num_corners += update

   return num_corners

   
if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input12b.txt")
   garden = parseInput(values)

   # Create a list of unvisited points (all points).
   plots = []
   for y in range(len(garden)):
      for x in range(len(garden[y])):
         plots.append((x, y))

   # While unassigned plot points remain, get the next
   # plot.
   price = 0
   while len(plots) > 0:
      # Get next unvisited point and its associated plot.
      x, y = plots.pop(0)
      points = getPlot(garden, x, y, garden[y][x], set())

      # Determine the number of sides in the plot.
      num_sides = calcSides(points)

      # Calculate the cost of fencing the plot.
      price += len(points) * num_sides
      
      # Remove the found plot points from the set of
      # unvisited points.
      plots_set = set(plots)
      plots_diff = plots_set.difference(points)
      plots = list(plots_diff)

   # Print the total cost of fencing.
   print('price = ' + str(price))
      
      
   
