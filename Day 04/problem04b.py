# This program conducts a word search of the
# data read from the file. The word search
# is to find two MAS in the shape of an X.
# One way to achieve that is like this:
#
# M.S
# .A.
# M.S
#
# Irrelevant characters have been replaced
# with . in the above diagram. Within the X,
# each MAS can be written forwards or backwards.

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


# This function is called when grid[y][x] is 'A'.
# Thus, look at the four characters cornering the
# center character and match to 'MAS' or 'SAM' to
# handle forwards and backwards.
def getXMas(grid, x, y):
   rstr1 = ''
   rstr2 = ''
   # Make sure 3x3 block is still on the grid and
   # create two strings of the two diagonals.
   if (y - 1 >= 0) and (y + 1 < len(grid)) and (x - 1 >= 0) and (x + 1 < len(grid[y])):
      rstr1 = grid[y-1][x-1] + grid[y][x] + grid[y+1][x+1]
      rstr2 = grid[y+1][x-1] + grid[y][x] + grid[y-1][x+1]

      # Compare constructed strings with target match.
      if ((rstr1 == 'MAS') or (rstr1 == 'SAM')) and ((rstr2 == 'MAS') or (rstr2 == 'SAM')):
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
         # If current character is 'A' then check diagonals.
         if grid[y][x] == 'A':
            if getXMas(grid, x, y):
               count += 1

   # print the result
   print('xmas count = ' + str(count))
         
   
   
