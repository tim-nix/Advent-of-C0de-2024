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
def getMoves(sequence):
   moves = []
   x1, y1 = sequence[0]
   for s in sequence[1:]:
      x2, y2 = s
      delta_x = x2 - x1
      delta_y = y2 - y1
      
      if delta_x == 1:
         moves.append('>')

      if delta_x == -1:
         moves.append('<')

      if delta_y == 1:
         moves.append('v')

      if delta_y == -1:
         moves.append('^')

      x1 = x2
      y1 = y2

   return moves
      

#
def getSequences(start, stop, none):
   delta_x = end[0] - start[0]
   delta_y = end[1] - start[1]
   
   sequence1 = []
   sequence2 = []
   if (delta_x > 0) and (delta_y > 0):
      for x in range(abs(delta_x)):
         sequence1.append((start[0] + x, start[1]))
         sequence2.insert(0, (end[0] - x, end[1]))

      for y in range(abs(delta_y) + 1):
         sequence1.append((end[0], start[1] + y))
         sequence2.insert(0, (start[0], end[1] - y))

   elif (delta_x > 0) and (delta_y < 0):
      for x in range(abs(delta_x)):
         sequence1.append((start[0] + x, start[1]))
         sequence2.insert(0, (end[0] - x, end[1]))

      for y in range(abs(delta_y) + 1):
         sequence1.append((end[0], start[1] - y))
         sequence2.insert(0, (start[0], end[1] + y))

   elif (delta_x < 0) and (delta_y > 0):
      for x in range(abs(delta_x)):
         sequence1.append((start[0] - x, start[1]))
         sequence2.insert(0, (end[0] + x, end[1]))

      for y in range(abs(delta_y) + 1):
         sequence1.append((end[0], start[1] + y))
         sequence2.insert(0, (start[0], end[1] - y))
         
   elif (delta_x < 0) and (delta_y < 0):
      for x in range(abs(delta_x)):
         sequence1.append((start[0] - x, start[1]))
         sequence2.insert(0, (end[0] + x, end[1]))

      for y in range(abs(delta_y) + 1):
         sequence1.append((end[0], start[1] - y))
         sequence2.insert(0, (start[0], end[1] + y))

   elif (delta_x < 0):
      for x in range(abs(delta_x) + 1):
         sequence1.append((start[0] - x, start[1]))

   elif (delta_x > 0):
      for x in range(abs(delta_x) + 1):
         sequence1.append((start[0] + x, start[1]))

   elif (delta_y > 0):
      for y in range(abs(delta_y) + 1):
         sequence1.append((start[0], start[1] + y))

   elif (delta_y < 0):
      for y in range(abs(delta_y) + 1):
         sequence1.append((start[0], start[1] - y))

   if none in sequence1:
      sequence1 = []

   if none in sequence2:
      sequence2 = []

   moves = []
   if len(sequence1) > 0:
      moves.append(getMoves(sequence1))

   if len(sequence2) > 0:
      moves.append(getMoves(sequence2))

   return moves

   
if __name__ == '__main__':
   # Read and parse input to list of lists of char.
   values = readFile("input21a.txt")
   codes = parseInput(values)

   keypad = [ [ '7', '8', '9' ],
              [ '4', '5', '6' ],
              [ '1', '2', '3' ],
              [ 'B', '0', 'A' ] ]

   dirpad = [ [ 'B', '^', 'A' ],
              [ '<', 'v', '>' ] ]

   for line in keypad:
      print(''.join(line))

   start = findLocation(keypad, '7')
   end   = findLocation(keypad, '0')
   print('start = ' + str(start))
   print('end   = ' + str(end))
   print(getSequences(start, end, (0, 3)))
         

   """
   # First robot pushing numeric keypad to unlock the
   # door.
   start = findLocation(keypad, 'A')
   r1_sequences = []
   for code in codes[:1]:
      r1_sequence = []
      for key in code:
         end = findLocation(keypad, key)
         toButton = genKeypad(start, end)
         r1_sequence += toButton
         r1_sequence.append('A')
         start = end
      r1_sequences.append(r1_sequence)

   for r_s in r1_sequences:
      print(''.join(r_s))
   print()         

   # Second robot pushing the directional keypad to
   # control the first robot.
   start = findLocation(dirpad, 'A')
   r2_sequences = []
   for r1_sequence in r1_sequences:
      r2_sequence = []
      for key in r1_sequence:
         end = findLocation(dirpad, key)
         toButton = genKeypad(start, end)
         r2_sequence += toButton
         r2_sequence.append('A')
         start = end
      r2_sequences.append(r2_sequence)

   for r_s in r2_sequences:
      print(''.join(r_s))
   print()


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
   
