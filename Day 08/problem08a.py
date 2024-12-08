# Given a map of various antennas, determine how
# many unique locations within the bounds of the
# map contain an antinode.

# Each antenna is tuned to a specific frequency
# indicated by a single lowercase letter, uppercase
# letter, or digit.

# An antinode occurs at any point that is perfectly
# in line with two antennas of the same frequency -
# but only when one of the antennas is twice as far
# away as the other. This means that for any pair of
# antennas with the same frequency, there are two
# antinodes, one on either side of them.

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
def calcAntinodes(antens):
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

            # Calculate the x-value for both antinodes
            if a[0] < b[0]:
               new_x1 = a[0] - diffx
               new_x2 = b[0] + diffx
            else:
               new_x1 = a[0] + diffx
               new_x2 = b[0] - diffx

            # The first antenna is always higher (lower
            # index) than the second antenna; so,
            # calculate the y-value for both.
            new_y1 = a[1] - diffy
            new_y2 = b[1] + diffy

            # Add the two antinodes to the set.
            antis.add((new_x1, new_y1))
            antis.add((new_x2, new_y2))

   # Return the set of antinodes.
   return antis
         

# Iterate through the set of antinodes and
# count only those that are on the map.
def countAntinodes(antis, x_bound, y_bound):
   count = 0
   for a in antis:
      if (a[0] >= 0) and (a[0] < x_bound) and (a[1] >= 0) and (a[1] < y_bound):
         count += 1

   return count
   
   
if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input8b.txt")
   antens = parseInput(values)

   # Determine the bounds of the map.
   x_bound = len(values[0])
   y_bound = len(values)

   # Count the number of unique antinodes on the map.
   antis = calcAntinodes(antens)
   count = countAntinodes(antis, x_bound, y_bound)

   # Print the result.
   print('Number of antinodes = ' + str(count))

   
