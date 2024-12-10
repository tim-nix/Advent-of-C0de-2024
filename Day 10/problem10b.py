# Given a topological map of altitudes, for each
# trailhead (altitude 0), find the number of
# trails that reach a summit (altitude 9). Sum
# the results.

# Trails always increases by a height of exactly
# 1 at each step. Hiking trails never include
# diagonal steps - only up, down, left, or right
# (from the perspective of the map).


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


# Convert the list of strings into a list of
# lists of integers.
def parseInput(values):
   terrain = []
   for line in values:
      terrain.append([ int(x) for x in list(line) ])
   
   return terrain
   

# Starting at a trailhead, recurse through neighbor
# positions, incrementing height, until summit
# (height of nine) is reached. Return the set of
# summit positions reached from the starting
# trailhead.
def calcScore(terrain, location):
   x, y = location
   # If summit is reached, return a value of 1.
   if terrain[y][x] == 9:
      return 1
   else:
      # Check four adjacent locations for increase
      # of 1 in altitude.
      score = 0
      if ((x-1) >= 0) and (terrain[y][x-1] == (terrain[y][x] + 1)):
         score += calcScore(terrain, (x-1, y))
      if ((x+1) < len(terrain[y])) and (terrain[y][x+1] == (terrain[y][x] + 1)):
         score += calcScore(terrain, (x+1, y))
      if ((y-1) >= 0) and (terrain[y-1][x] == (terrain[y][x] + 1)):
         score += calcScore(terrain, (x, y-1))
      if ((y+1) < len(terrain)) and (terrain[y+1][x] == (terrain[y][x] + 1)):
         score += calcScore(terrain, (x, y+1))

      # Return the sum (score) of all summits reached
      # from the current trail.
      return score
         

if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input10b.txt")
   terrain = parseInput(values)

   # Iterate through terrain looking for a trailhead.
   score = 0
   for y in range(len(terrain)):
      for x in range(len(terrain)):
         if terrain[y][x] == 0:
            # Add number of summits reached from
            # trailhead to the score.
            score += calcScore(terrain, (x, y))

   # Print the total score for the map
   print('Score = ' + str(score))
   
