# Count the number of positions that, if an obstacle
# is added, the result is that the lab guard will
# walk in a loop within the lab area (as opposed to
# leaving the lab area).
#
# Lab guards start at a given location (indicated
# by '^') and move forward (up). If there is something
# directly in front of the guard (indicated by '#'),
# they turn right 90 degrees. Otherwise, they take a
# step forward.  This continues until they leave the
# area (the input grid).

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


# Convert list of strings into list of list
# of characters.
def parseInput(values):
   area = []
   for v in values:
      area.append(list(v))

   return area


# Search through the map to find the starting
# location of the guard.
def findStart(area):
   for y in range(len(area)):
      for x in range(len(area[y])):
         if area[y][x] == '^':
            return (x, y)

   return (-1, -1)


# Check position to ensure it is within the
# area.
def checkArea(x, y, area):
   return (x >= 0) and (x < len(area[0])) and (y >= 0) and (y < len(area))


if __name__ == '__main__':
   # Read and parse input to a grid of characters.
   values = readFile("input6b.txt")
   area = parseInput(values)
   
   # Find the starting location.
   start_x, start_y = findStart(area)
   area[start_y][start_x] = '.'

   # Define directions.
   directions = [ 'up', 'right', 'down', 'left' ]

   # Initialize count.
   count = 0

   # Check the guard path if an obstacle is added to a single
   # location on the area.
   for j in range(len(area)):
      for i in range(len(area[j])):
         # Modify area by adding obstacle.
         if ((i, j) != (start_x, start_y)) and (area[j][i] == '.'):
            area[j][i] = '#'

            # Set initial conditions
            dir_i = 0
            x = start_x
            y = start_y

            # Create a map of locations and directions visited.
            visited = set()
            visited.add((x, y, dir_i))

            # Continue to move until marker leaves the area.
            while checkArea(x, y, area):
               # If obstacle is encountered, rotate 90 degrees
               # to the right.
               if directions[dir_i] == 'up':
                  next_x = x
                  next_y = y - 1
               elif directions[dir_i] == 'right':
                  next_x = x + 1
                  next_y = y
               elif directions[dir_i] == 'down':
                  next_x = x
                  next_y = y + 1
               elif directions[dir_i] == 'left':
                  next_x = x - 1
                  next_y = y

               # Make sure that the next step is still in the area.
               if checkArea(next_x, next_y, area):
                  # If the next step is an obstacle then rotate
                  if area[next_y][next_x] == '#':
                     dir_i = (dir_i + 1) % 4
                  else:
                     # If next step is a loop then increment count
                     if (next_x, next_y, dir_i) in visited:
                        count += 1
                        x = -1
                        y = -1
                     else:
                        # If next step is okay, then add it
                        x = next_x
                        y = next_y
                        visited.add((x, y, dir_i))
                        
               else:
                  # The next step is not in the area and the marker
                  # has left the area.
                  x = next_x
                  y = next_y
                  
            # Remove the obstacle
            area[j][i] = '.'

   # Print the count
   print('Loops resulted: ' + str(count))
   
