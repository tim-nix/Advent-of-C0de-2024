# This program conducts a word search of the
# data read from the file. It only has to find
# one word: XMAS. This word search allows words
# to be horizontal, vertical, diagonal, written
# backwards, or even overlapping other words.
# The program should find the count of ALL
# instances of XMAS within the text.

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


# Convert a list of strings into a list of lists
# of characters.
def parseInput(values):
   grid = []
   for line in values:
      char_list = list(line)
      grid.append(char_list)

   return grid


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters in the forward
# direction (incrementing x) and see if they
# match XMAS'
def getForward(grid, x, y):
   rstr = grid[y][x]
   if x + 3 < len(grid[y]):
      rstr += grid[y][x+1]
      rstr += grid[y][x+2]
      rstr += grid[y][x+3]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters in the backward
# direction (decrementing x) and see if they
# match XMAS'
def getBackward(grid, x, y):
   rstr = grid[y][x]
   if x - 3 >= 0:
      rstr += grid[y][x-1]
      rstr += grid[y][x-2]
      rstr += grid[y][x-3]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters in the upward
# direction (decrementing y) and see if they
# match XMAS'
def getUp(grid, x, y):
   rstr = grid[y][x]
   if y - 3 >= 0:
      rstr += grid[y-1][x]
      rstr += grid[y-2][x]
      rstr += grid[y-3][x]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters in the downward
# direction (incrementing y) and see if they
# match XMAS'
def getDown(grid, x, y):
   rstr = grid[y][x]
   if y + 3 < len(grid):
      rstr += grid[y+1][x]
      rstr += grid[y+2][x]
      rstr += grid[y+3][x]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters up along the
# right diagonal (decrementing y and incrementing
# x) and see if they match 'XMAS'
def getUpRight(grid, x, y):
   rstr = grid[y][x]
   if (y - 3 >= 0) and (x + 3 < len(grid[y])):
      rstr += grid[y-1][x+1]
      rstr += grid[y-2][x+2]
      rstr += grid[y-3][x+3]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters down along the
# right diagonal (incrementing y and decrementing
# x) and see if they match 'XMAS'
def getDownRight(grid, x, y):
   rstr = grid[y][x]
   if (y + 3 < len(grid)) and (x + 3 < len(grid[y])):
      rstr += grid[y+1][x+1]
      rstr += grid[y+2][x+2]
      rstr += grid[y+3][x+3]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters up along the
# left diagonal (decrementing y and decrementing
# x) and see if they match 'XMAS'
def getUpLeft(grid, x, y):
   rstr = grid[y][x]
   if (y - 3 >= 0) and (x - 3 >= 0):
      rstr += grid[y-1][x-1]
      rstr += grid[y-2][x-2]
      rstr += grid[y-3][x-3]
      
      if rstr == 'XMAS':
         return True

   return False


# The current position [y][x] is an 'X'.  Find,
# if they exist, the characters down along the
# left diagonal (incrementing y and decrementing
# x) and see if they match 'XMAS'
def getDownLeft(grid, x, y):
   rstr = grid[y][x]
   if (y + 3 < len(grid)) and (x - 3 >= 0):
      rstr += grid[y+1][x-1]
      rstr += grid[y+2][x-2]
      rstr += grid[y+3][x-3]
      
      if rstr == 'XMAS':
         return True

   return False


if __name__ == '__main__':
   # Read and parse input to a grid of characters.
   values = readFile("input4b.txt")
   grid = parseInput(values)

   # Iterate through each character of the grid.
   count = 0
   for y in range(len(grid)):
      for x in range(len(grid[y])):
         # If the current character is 'X', check
         # all directions to see if 'XMAS' is found.
         if grid[y][x] == 'X':
            if getForward(grid, x, y):
               count += 1
            if getBackward(grid, x, y):
               count += 1
            if getUp(grid, x, y):
               count += 1
            if getDown(grid, x, y):
               count += 1
            if getUpRight(grid, x, y):
               count += 1
            if getDownRight(grid, x, y):
               count += 1
            if getUpLeft(grid, x, y):
               count += 1
            if getDownLeft(grid, x, y):
               count += 1

   # print the result
   print('xmas count = ' + str(count))
         
   
   
