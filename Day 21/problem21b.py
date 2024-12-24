# This program solves the key press sequence for a
# human using a direction keypad to control a sequence
# of 25 robots, the last of which ismusing a direction
# keypad to control a robot using a numeric keypad to
# unlock a door.

# The numeric keypad has four rows of buttons: 789,
# 456, 123, and finally an empty gap followed by 0A.

# The directional keypad has two rows of buttons: a
# gap / ^ (up) / A (activate) on the first row and <
# (left) / v (down) / > (right) on the second row.

# First, find the fewest number of button presses
# needed to perform in order to cause the robot in
# front of the door to type each code.

# Next, calculate the complexity of a single code
# which is equal to the result of multiplying the
# length of the shortest sequence of button presses
# needed to type on the directional keypad in order
# to cause the code to be typed on the numeric
# keypad and the numeric part of the code (ignoring
# leading zeroes).

# The final answer is the sum of the complexities.

from functools import cache

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


# Find the location within the grid (the x, y
# coordinates) of the marker.
def findLocation(grid, marker):
   for y in range(len(grid)):
      for x in range(len(grid[y])):
         if grid[y][x] == marker:
            return (x, y)

   return None


# Find the shortest paths from the start location to
# the stop location which neither cross the face of
# the non-button location (marked 'B' in the code) and
# minimizes the number of moves (either all vertical
# moves followed by all horizontal moves OR all
# horizontal moves followed by all vertical moves).
def getSequences(start, stop, none):
   # If already at the destination, simply press 'A'.
   if start == stop:
      return [ 'A' ]

   # Determine the change in x and the change in y.
   delta_x = abs(stop[0] - start[0])
   delta_y = abs(stop[1] - start[1])

   # Associate change is the two directions with the
   # associated symbol.
   x_move = ''
   if stop[0] > start[0]:
      x_move = '>'
   else:
      x_move = '<'

   y_move = ''
   if stop[1] > start[1]:
      y_move = 'v'
   else:
      y_move = '^'

   # Generate the two potential move sequences.
   paths = [ x_move * delta_x + y_move * delta_y, y_move * delta_y + x_move * delta_x ]

   # For each move sequence, generate all locations
   # traversed. 
   for path in paths:
      current = start
      for move in path:
         # If any location is over the non-button
         # location, then eliminate that sequence.
         match move:
            case '>':
               next_loc = (current[0] + 1, current[1])
            case '<':
               next_loc = (current[0] - 1, current[1])
            case '^':
               next_loc = (current[0], current[1] - 1)
            case 'v':
               next_loc = (current[0], current[1] + 1)
          
         if next_loc == none:
            paths.remove(path)
            break

         current = next_loc

   # Append 'A' to each remaining sequence and return.
   return [ p + 'A' for p in paths ]


#
@cache
def findSequences(r):
   start = findLocation(dirpad, 'A')
   r2_sequence = [ '' ]
   for key in r:
      end = findLocation(dirpad, key)
      toButton = getSequences(start, end, dir_none)
      next_sequence = []
      for r2 in r2_sequence:
         for tB in toButton:
            next_sequence.append(r2 + tB)
      r2_sequence = list(set(next_sequence))
      start = end

   return r2_sequence

   
 
if __name__ == '__main__':
   # Read the file input as a list of strings.
   codes = readFile("input21b.txt")

   # Store the structure of the keypads and the
   # locations of the non-buttons (marked as 'B').
   keypad = [ '789', '456', '123', 'B0A' ]
   key_none = findLocation(keypad, 'B')
   dirpad = [ 'B^A', '<v>' ]
   dir_none = findLocation(dirpad, 'B')

   num_robots = 3

   
   # Generate the key presses on the directional
   # keypad to control Robot 2 so that it correctly
   # enters the door code on the numerical keypad.
   complexity = 0
   # Iterate through each door code.
   for code in codes:
      start = findLocation(keypad, 'A')
      r1_sequence = [ '' ]
      for key in code:
         end = findLocation(keypad, key)
         toButton = getSequences(start, end, key_none)
         next_sequence = []
         for r1 in r1_sequence:
            for tB in toButton:
               next_sequence.append(r1 + tB)
         r1_sequence = list(set(next_sequence))
         start = end

      #
      for r in range(num_robots):
         r2_sequences = []
         for r in r1_sequence:
            r2_sequence = findSequences(r)
            r2_sequences += r2_sequence

         r1_sequence = r2_sequences

         # Search through all of the generated key
         # sequences and find the one of minimum
         # length.
         min_length = len(r1_sequence[0])
         for r1 in r1_sequence:
            if len(r1) < min_length:
               min_length = len(r1)

         min_sequence = []
         for r1 in r1_sequence:
            if len(r1) == min_length:
               min_sequence.append(r1)
               
         r1_sequence = min_sequence

      # Calculate the complexity of this sequence and
      # add it to the sum.
      code_num = ''.join(code[:-1])
      complexity += int(code_num) * min_length

   # Display the results.
   print('complexity = ' + str(complexity))
   
