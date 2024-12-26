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


# Library used for memoization of the 'findSequences'
# function call.
from functools import cache


# Store the structure of the keypads and the
# locations of the non-buttons (marked as 'B').
numpad = [ '789', '456', '123', 'B0A' ]
num_none = (0, 3)
dirpad = [ 'B^A', '<v>' ]
dir_none = (0, 0)
   
num_robots = 25


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
def getSequences(start, end, none):
   # If already at the destination, simply press 'A'.
   if start == end:
      return [ 'A' ]

   # Determine the change in x and the change in y.
   delta_x = abs(end[0] - start[0])
   delta_y = abs(end[1] - start[1])

   # Associate change is the two directions with the
   # associated symbol.
   x_move = ''
   if end[0] > start[0]:
      x_move = '>'
   else:
      x_move = '<'

   y_move = ''
   if end[1] > start[1]:
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


# This recursive function generates the sequence of
# moves needed for each robot within the sequence and
# returns the length of the shortest sequence. Thus,
# the final result is the length of the shortest
# sequence needed for the human to enter for the last
# robot to enter the code on the numerical keypad.
@cache
def findSequences(code, robot):
   # Set the appropriate keypad and the location of
   # blank based on which robot is being moved (the
   # level of recursion).
   if robot == 0:
      pad = numpad
      none = num_none
   else:
      pad = dirpad
      none = dir_none

   # Start at the 'A' location on the pad.
   code = 'A' + code

   # Keep track of the sum of the shortest sequences.
   sequence_length = 0
   
   # Select the next two move characters denoting the
   # starting location and ending location.
   for code_i in range(len(code) - 1):
      start_dir = code[code_i]
      end_dir = code[code_i + 1]
      
      # Convert to grid coordinates (x, y).
      start = findLocation(pad, start_dir)
      end = findLocation(pad, end_dir)

      # Get the list of sequences for the move.
      sequences = getSequences(start, end, none)

      # If the last robot, return the length of the
      # shortest sequence.
      if robot == num_robots:
         sequence_length += min(map(len, sequences))
      else:
         # Otherwise, return the length of shortest
         # sequence including the move sequence of all
         # other robots.
         min_length = -1
         for seq in sequences:
            seq_length = findSequences(seq, robot + 1)
            if min_length == -1:
               min_length = seq_length
            elif seq_length < min_length:
               min_length = seq_length
               
         sequence_length += min_length

   # Return the length of the shortest sequence.
   return sequence_length

   
 
if __name__ == '__main__':
   # Read the file input as a list of strings.
   codes = readFile("input21b.txt")
   
   # Initialize the complexity score.
   complexity = 0
   
   # Iterate through each door code, get the length of
   # the shortest sequence, and calculate the
   # complexity score for the code.
   for code in codes:
      complexity += int(''.join(code[:-1])) * findSequences(code, 0)

   # Display the results.
   print('complexity = ' + str(complexity))
   
