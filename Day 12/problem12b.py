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


# Recursively determine the points within the plot and
# the perimeter of the plot.
def getPlot(garden, x, y, crop, points, perim):
   # If the point is outside the garden, then done.
   if (x < 0) or (x >= len(garden[0])) or (y < 0) or (y >= len(garden)):
      perim.add((x, y))
      return (points, perim)
   # If the point contains a different crop. then done.
   elif garden[y][x] != crop:
      perim.add((x, y))
      return (points, perim)
   else:
      # Add current point to set of visited points
      points.add((x, y))
      # For unvisited neighbors, recurse.
      perimeter = set()
      if (x - 1, y) not in points:
         plots, perim2 = getPlot(garden, x - 1, y, crop, points, perim)
         perimeter.union(perim2)
      if (x + 1, y) not in points:
         plots, perim2 = getPlot(garden, x + 1, y, crop, points, perim)
         perimeter.union(perim2)
      if (x, y - 1) not in points:
         plots, perim2 = getPlot(garden, x, y - 1, crop, points, perim)
         perimeter.union(perim2)
      if (x, y + 1) not in points:
         plots, perim2 = getPlot(garden, x, y + 1, crop, points, perim)
         perimeter.union(perim2)

      # Return points within plot and perimeter.
      return (points, perim.union(perimeter))

def numCorners(x, y, plot):
   if ((x - 1, y) in plot) and ((x + 1, y) in plot) and ((x, y - 1) in plot) and ((x, y + 1) in plot):
      return 4
   elif ((x - 1, y) in plot) and ((x + 1, y) in plot) and ((x, y - 1) in plot):
      return 3
   elif ((x - 1, y) in plot) and ((x + 1, y) in plot) and ((x, y + 1) in plot):
      return 3
   elif ((x - 1, y) in plot) and ((x, y - 1) in plot) and ((x, y + 1) in plot):
      return 3
   elif ((x + 1, y) in plot) and ((x, y - 1) in plot) and ((x, y + 1) in plot):
      return 3
   elif ((x + 1, y) in plot) and ((x, y - 1) in plot):
      return 1
   elif ((x + 1, y) in plot) and ((x, y + 1) in plot):
      return 1
   elif ((x - 1, y) in plot) and ((x, y - 1) in plot):
      return 1
   elif ((x - 1, y) in plot) and ((x, y + 1) in plot):
      return 1
   else:
      return 0


def calcSides(plot, perim):
   points = list(plot)
   corners = set()
   num_corners = 0
   for p in points:
      x, y = p
      # Handle convex
      if ((x - 1, y - 1) not in perim) and ((x - 1, y - 1) not in plot):
         if (x - 1, y - 1) not in corners:
            corners.add((x - 1, y - 1))
            num_corners += 1
      if (x - 1, y + 1) not in perim and ((x - 1, y + 1) not in plot):
         if (x - 1, y + 1) not in corners:
            corners.add((x - 1, y + 1))
            num_corners += 1
      if (x + 1, y - 1) not in perim and ((x + 1, y - 1) not in plot):
         if (x + 1, y - 1) not in corners:
            corners.add((x + 1, y - 1))
            num_corners += 1
      if (x + 1, y + 1) not in perim and ((x + 1, y + 1) not in plot):
         if (x + 1, y + 1) not in corners:
            corners.add((x + 1, y + 1))
            num_corners += 1

      # Handle concave
      if ((x - 1, y) in perim) and ((x - 1, y) not in corners):
         c = numCorners(x - 1, y, plot)
         if c > 0:
            corners.add((x - 1, y))
            num_corners += c
               
         
      if ((x + 1, y) in perim) and ((x + 1, y) not in corners):
         c = numCorners(x + 1, y, plot)
         if c > 0:
            corners.add((x + 1, y))
            num_corners += c
            
      if ((x, y - 1) in perim) and ((x, y - 1) not in corners):
         c = numCorners(x, y - 1, plot)
         if c > 0:
            corners.add((x, y - 1))
            num_corners += c
            
      if ((x, y + 1) in perim) and ((x, y + 1) not in corners):
         c = numCorners(x, y + 1, plot)
         if c > 0:
            corners.add((x, y + 1))
            num_corners += c

   print('corners = ' + str(corners))
   return num_corners

   
if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input12a2.txt")
   garden = parseInput(values)

   # Create a list of unvisited points (all points).
   plots = []
   for y in range(len(garden)):
      for x in range(len(garden[y])):
         plots.append((x, y))

   for line in values:
      print(line)

   # While unassigned plot points remain, get the next
   # plot.
   price = 0
   while len(plots) > 0:
      # Get next unvisited point, its associated plot
      # points, and its perimeter.
      x, y = plots.pop(0)
      print('crop = ' + garden[y][x])
      points, perim = getPlot(garden, x, y, garden[y][x], set(), set())

      print('points = ' + str(points))
      print('perim = ' + str(perim))
      num_sides = calcSides(points, perim)
      print('num sides = ' + str(num_sides))
      price += len(points) * num_sides
      
      # Remove the found plot points from the set of
      # unvisited points.
      plots_set = set(plots)
      plots_diff = plots_set.difference(points)
      plots = list(plots_diff)

   # Print the total cost of fencing.
   print('price = ' + str(price))
      
      
   
