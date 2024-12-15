# The file input consists of a map of the lab and a
# set of moves. A robot (@) attempts to move around
# the lab and, if any boxes (O) are in the way, the
# robot will also attempt to push those boxes. If this
# action would cause the robot or a box to move into a
# wall (#), nothing moves instead, including the robot.

# After all moves are made, the sum of the boxes' GPS
# positions are calculated. The GPS position of a box
# located at coordinates x, y is 100y + x.

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


# Split the list of strings into two parts. The
# initial strings describe the map of the lab. The
# rest of the document describes the moves (^ for up,
# v for down, < for left, > for right) that the robot
# will attempt to make, in order.
def parseInput(values):
   lab = []
   # Parse the map of the lab.
   i = 0
   while values[i] != '':
      lab.append(list(values[i]))
      i += 1

   # Parse the moves.
   moves = []
   i += 1
   while i < len(values):
      moves = moves + list(values[i])
      i += 1

   return (lab, moves)


# Recursively check the sequence of positions in the
# direction of the move. If the move is legal (an
# empty spot exists along the path towards the wall)
# then shift the robot and any boxes over. If there
# is either a wall, or a contiguous sequence of boxes
# between the robot and the wall, then nothing is
# moved.
def makeMove(lab, x, y, dx, dy):
   # The next space is a wall, so no move occurs.
   if lab[y + dy][x + dx] == '#':
      return False

   # The next space is empty, so it is occupied by
   # the contents of the previous space.
   elif lab[y + dy][x + dx] == '.':
      lab[y + dy][x + dx] = lab[y][x]
      return True

   # The next space is a box (O), so recurse to the
   # next position to test if a move can occur.
   elif lab[y + dy][x + dx] == 'O':
      if makeMove(lab, x + dx, y + dy, dx, dy):
         lab[y + dy][x + dx] = lab[y][x]
         return True
      else:
         return False


if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input15b.txt")
   lab, moves = parseInput(values)

   # Display the initial map of the lab.
   for line in lab:
      print(''.join(line))

   # Find the location of the robot.
   r_x = 0
   r_y = 0
   for y in range(len(lab)):
      for x in range(len(lab)):
         if lab[y][x] == '@':
            r_x = x
            r_y = y

   # Iterate through all moves and, if each move is
   # legal, make the move.
   for move in moves:
      if move == '<':
         if makeMove(lab, r_x, r_y, -1, 0):
            lab[r_y][r_x] = '.'
            r_x -=1

      if move == '^':
         if makeMove(lab, r_x, r_y, 0, -1):
            lab[r_y][r_x] = '.'
            r_y -= 1

      if move == '>':
         if makeMove(lab, r_x, r_y, 1, 0):
            lab[r_y][r_x] = '.'
            r_x += 1

      if move == 'v':
         if makeMove(lab, r_x, r_y, 0, 1):
            lab[r_y][r_x] = '.'
            r_y += 1

   # Display the final map of the lab.
   print()
   for line in lab:
      print(''.join(line))

   # Calculate the sum of all GPS coordinates.
   print()
   sum = 0
   for y in range(len(lab)):
      for x in range(len(lab)):
         if lab[y][x] == 'O':
            sum += y * 100 + x

   # Display the sum of the GPS coordinates.
   print('sum of GPS coordinates = ' + str(sum))
   
