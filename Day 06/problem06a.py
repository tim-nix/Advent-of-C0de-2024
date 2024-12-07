# Count the number of positions visited by a guard.
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


# Count the number of 'X's in the area.
def countXs(area):
   count = 0
   for y in range(len(area)):
      for x in range(len(area[y])):
         if area[y][x] == 'X':
            count += 1

   return count


if __name__ == '__main__':
   # Read and parse input to a grid of characters.
   values = readFile("input6b.txt")
   area = parseInput(values)
   # Find the starting location.
   x, y = findStart(area)

   # Set direction to 'up'
   directions = [ 'up', 'right', 'down', 'left' ]
   dir_i = 0

   # Mark start with 'X'.
   area[y][x] = 'X'
   
   # Continue to move until marker leaves the area.
   while (x >= 0) and (x < len(area[0])) and (y >= 0) and (y < len(area)):   
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

      # Make sure that the next step is still in the area
      if (next_x >= 0) and (next_x < len(area[0])) and (next_y >= 0) and (next_y < len(area)):
         # Is the next step occupied.
         if area[next_y][next_x] == '.':
            area[next_y][next_x] = 'X'

         if area[next_y][next_x] == 'X':
            x = next_x
            y = next_y

         if area[next_y][next_x] == '#':
            dir_i = (dir_i + 1) % 4
      else:
         # The next step is not in the area and the marker
         # has left the area.
         x = next_x
         y = next_y

   # Count the number of X's in the area and print the results
   print('The number of positions visited: ' + str(countXs(area)))
   
