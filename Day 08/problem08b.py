# Given a map of various antennas, determine how
# many unique locations within the bounds of the
# map contain an antinode.

# Each antenna is tuned to a specific frequency
# indicated by a single lowercase letter, uppercase
# letter, or digit.

# An antinode occurs at any grid position exactly in
# line with at least two antennas of the same
# frequency, regardless of distance. This means that
# some of the new antinodes will occur at the position
# of each antenna (unless that antenna is the only one
# of its frequency).

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


# Iterate through the map and, for each antenna
# type (frequency), create a new dictionary entry.
# The dictionary will contain a list of (x, y)
# coordinates for each antenna type.
def parseInput(values):
   antens = dict()
   # Iterate through the map locations.
   for y in range(len(values)):
      for x in range(len(values[y])):
         # Is an antenna present?
         if values[y][x] != '.':
            # Add the antenna; different if it
            # is the first time the antenna type
            # is encountered.
            if values[y][x] not in antens:
               antens[values[y][x]] = [ (x, y) ]
            else:
               antens[values[y][x]].append((x, y))

   # Return the antenna locations, organized by
   # antenna type (frequency).
   return antens


# Generate the set of antinodes. This is done by
# iterating through the pairs of antennas and
# calculating the antinodes for each pair. These
# are added to the set of antinodes.
def calcAntinodes(antens, x_bound, y_bound):
   antis = set()
   # Iterate through each antenna type.
   for key in antens:
      # Iterate through each pair of antennas.
      for a_i in range(len(antens[key])):
         for b_i in range(a_i + 1, len(antens[key])):
            a = antens[key][a_i]
            b = antens[key][b_i]

            # Calculate the x and y difference
            diffx = abs(a[0] - b[0])
            diffy = abs(a[1] - b[1])

            # Since antinodes can be in line with at least
            # two antennas of the same frequency, regardless
            # of distance, calculate pairs of antinodes until
            # both are off the map.
            on_map = True
            iteration = 1
            while on_map:
               # Calculate the x-value for both antinodes
               if a[0] < b[0]:
                  new_x1 = a[0] - (iteration * diffx)
                  new_x2 = b[0] + (iteration * diffx)
               else:
                  new_x1 = a[0] + (iteration * diffx)
                  new_x2 = b[0] - (iteration * diffx)

               # The first antenna is always higher (lower
               # index) than the second antenna; so,
               # calculate the y-value for both.
               new_y1 = a[1] - (iteration * diffy)
               new_y2 = b[1] + (iteration * diffy)

               # Add the two antenna to the set.
               antis.add((a[0], a[1]))
               antis.add((b[0], b[1]))

               # If antinodes are on map, add them to the set.
               on_map = False
               if (new_x1 >= 0) and (new_x1 < x_bound) and (new_y1 >= 0) and (new_y1 < y_bound):
                  antis.add((new_x1, new_y1))
                  on_map = True

               if (new_x2 >= 0) and (new_x2 < x_bound) and (new_y2 >= 0) and (new_y2 < y_bound):
                  antis.add((new_x2, new_y2))
                  on_map = True

               iteration += 1
               
   # Return the set of antinodes.
   return antis
   
   
if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input8b.txt")
   antens = parseInput(values)

   # Determine the bounds of the map.
   x_bound = len(values[0])
   y_bound = len(values)

   # Count the number of unique antinodes on the map.
   antis = calcAntinodes(antens, x_bound, y_bound)
   count = len(antis)

   # Print the result.
   print('Number of antinodes = ' + str(count))

   
