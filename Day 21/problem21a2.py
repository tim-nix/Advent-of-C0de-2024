# 


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


# Convert the list of strings (from the file input) to
# a list of list of input key presses.
def parseInput(values):
   codes = []
   for v in values:
      codes.append(list(v))

   return codes


# Find the location within the grid (the x, y
# coordinates) of the marker.
def findLocation(grid, marker):
   for y in range(len(grid)):
      for x in range(len(grid[y])):
         if grid[y][x] == marker:
            return (x, y)

   return None


#
def getSequences(start, stop, none):
   if start == stop:
      return [ 'A' ]
   
   delta_x = abs(stop[0] - start[0])
   delta_y = abs(stop[1] - start[1])
   
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

   paths = [ x_move * delta_x + y_move * delta_y, y_move * delta_y + x_move * delta_x ]
   
   for path in paths:
      current = start
      for move in path:
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

   return [ p + 'A' for p in paths ]
   
 
if __name__ == '__main__':
   # Read and parse input to list of lists of char.
   values = readFile("input21a.txt")
   codes = parseInput(values)

   keypad = [ '789', '456', '123', 'B0A' ]
   dirpad = [ 'B^A', '<v>' ]

   # First robot pushing numeric keypad to unlock the
   # door.
   start = findLocation(keypad, 'A')
   r1_sequences = []
   for code in codes[:1]:
      r1_sequence = [ '' ]
      for key in code:
         end = findLocation(keypad, key)
         toButton = getSequences(start, end, (0, 3))
         next_sequence = []
         for r1 in r1_sequence:
            for tB in toButton:
               next_sequence.append(r1 + tB)
         r1_sequence = list(set(next_sequence))
         start = end
      r1_sequences.append(r1_sequence)

   for r_s in r1_sequences:
      print(r_s)
   print()         


   start = findLocation(dirpad, 'A')
   r2_sequences = []
   for r1_sequence in r1_sequences:
      r2_sequence = [ '' ]
      for combo in r1_sequence:
         for key in combo:
            end = findLocation(dirpad, key)
            toButton = getSequences(start, end, (0, 0))
            next_sequence = []
            for r2 in r2_sequence:
               for tB in toButton:
                  next_sequence.append(r2 + tB)
            r2_sequence = list(set(next_sequence))
            start = end
      r2_sequences.append(r2_sequence)

   for seq in r2_sequences:
      seq.sort()
      for r in seq:
         print(r)
   print()

   """
   # Human pushing the directional keypad to control
   # the second robot.
   start = findLocation(dirpad, 'A')
   r3_sequences = []
   for r2_sequence in r2_sequences:
      r3_sequence = []
      for key in r2_sequence:
         end = findLocation(dirpad, key)
         toButton = genKeypad(start, end)
         r3_sequence += toButton
         r3_sequence.append('A')
         start = end
      r3_sequences.append(r3_sequence)

   for i in range(len(r3_sequences)):
      print(''.join(codes[i]) + ': ' + ''.join(r3_sequences[i]))

   for r_s in r3_sequences:
      print(len(r_s))
   
   """
   
