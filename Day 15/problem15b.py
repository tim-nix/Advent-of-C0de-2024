# The file input consists of a map of the lab and a
# set of moves. A robot (@) attempts to move around
# the lab and, if any boxes ([]) are in the way, the
# robot will also attempt to push those boxes. If this
# action would cause the robot or a box to move into a
# wall (#), nothing moves instead, including the robot.

# For this problem, the lab input is expanded. Each
# wall is replaced with two wall segments, each empty
# spot is replaced with two empty spots, and a box (O)
# is replaced with a large box ([]).

# After all moves are made, the sum of the boxes' GPS
# positions are calculated. The GPS position of a box
# whose left side ([) is located at coordinates x, y
# is 100y + x.

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
# lateral direction of the move. If the move is legal
# (an empty spot exists along the path towards the
# wall) then shift the robot and any boxes over. If
# there is either a wall, or a contiguous sequence of
# boxes between the robot and the wall, then nothing
# is moved.
def makeXMove(lab, x, y, dx):
   # The next space is a wall, so no move occurs.
   if lab[y][x + dx] == '#':
      return False

   # The next space is empty, so it is occupied by
   # the contents of the previous space.
   elif lab[y][x + dx] == '.':
      lab[y][x + dx] = lab[y][x]
      return True

   # The next space is the start of a large box
   # (either [ or ]), so recurse to the next position
   # to test if a move can occur.
   elif (lab[y][x + dx] == ']') or (lab[y][x + dx] == '['):
      if makeXMove(lab, x + dx, y, dx):
         lab[y][x + dx] = lab[y][x]
         return True
      else:
         return False

      
# Recursively check the sequence of positions in the
# vertical direction of the move. If the move is legal
# (empty spots exists along the path towards the
# wall) then shift the robot and any boxes up or down.
# If there is either a wall, or a contiguous sequence
# of boxes between the robot and the wall, then
# nothing is moved.
def makeYMove(lab, positions, dy):
   # Since boxes can overlap by one position, we need
   # track all boxes affected in the row.
   space = True
   next_pos = []
   # Test each position added from the previous row.
   for p in positions:
      x, y = p
      # If any box is blocked by a wall, then no move.
      if lab[y + dy][x] == '#':
         #print('wall at ' + str((y + dy, x)))
         return False

      # If any box is encountered, then add it to the
      # new row for the recursive call.
      if lab[y + dy][x] == '[':
         if (x, y + dy) not in next_pos:
            next_pos.append((x, y + dy))
         if (x + 1, y + dy) not in next_pos:
            next_pos.append((x + 1, y + dy))

      if lab[y + dy][x] == ']':
         if (x - 1, y + dy) not in next_pos:
            next_pos.append((x - 1, y + dy))
         if (x, y + dy) not in next_pos:
            next_pos.append((x, y + dy))

   # If boxes were encountered in the new row, then
   # recurse to see if the move can be made.
   if len(next_pos) > 0:
      space = makeYMove(lab, next_pos, dy)
      
   # There is space to make the move, then move. Copy
   # all spaces in the current row up to the next row
   # and empty all current row positions.
   if space:
      for p in positions:
         x, y = p
         lab[y + dy][x] = lab[y][x]
         lab[y][x] = '.'

   # Return whether or not the move can be made.
   return space


# Expand the map of the lab to one that is twice as
# large according to the following rules:
# - If the tile is #, the new map contains ## instead.
# - If the tile is O, the new map contains [] instead.
# - If the tile is ., the new map contains .. instead.
# - If the tile is @, the new map contains @. instead.
def expandMap(lab):
   new_lab = []
   for line in lab:
      new_line = []
      for loc in line:
         if loc == '#':
            new_line.append('#')
            new_line.append('#')
         elif loc == 'O':
            new_line.append('[')
            new_line.append(']')
         elif loc == '.':
            new_line.append('.')
            new_line.append('.')
         elif loc == '@':
            new_line.append('@')
            new_line.append('.')
            
      new_lab.append(new_line)

   return new_lab


if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input15b.txt")
   lab, moves = parseInput(values)

   # Expand map.
   lab = expandMap(lab)

   # Display the initial map of the lab.
   for line in lab:
      print(''.join(line))

   # Find the location of the robot.
   r_x = 0
   r_y = 0
   for y in range(len(lab)):
      for x in range(len(lab[y])):
         if lab[y][x] == '@':
            r_x = x
            r_y = y

   # Iterate through all moves and, if each move is
   # legal, make the move.
   for move in moves:
      if move == '<':
         if makeXMove(lab, r_x, r_y, -1):
            lab[r_y][r_x] = '.'
            r_x -=1

      if move == '>':
         if makeXMove(lab, r_x, r_y, 1):
            lab[r_y][r_x] = '.'
            r_x += 1


      if move == '^':
         if makeYMove(lab, [ (r_x, r_y) ], -1):
            lab[r_y][r_x] = '.'
            r_y -= 1

      if move == 'v':
         if makeYMove(lab, [ (r_x, r_y) ], 1):
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
      for x in range(len(lab[y])):
         if lab[y][x] == '[':
            sum += y * 100 + x

   # Display the sum of the GPS coordinates.
   print('sum of GPS coordinates = ' + str(sum))
   
