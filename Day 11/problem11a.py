# The file input consist of a line of marked stones
# (marked with a number).  Every time you blink, the
# stones each simultaneously change according to the
# first applicable rule in this list:
#
# (1) If the stone is engraved with the number 0, it
#     is replaced by a stone engraved with the number
#     1.
# (2) If the stone is engraved with a number that has
#     an even number of digits, it is replaced by two
#     stones. The left half of the digits are engraved
#     on the new left stone, and the right half of the
#     digits are engraved on the new right stone (the
#     new numbers don't keep extra leading zeroe).
# (3) If none of the other rules apply, the stone is
#     replaced by a new stone; the old stone's number
#     multiplied by 2024 is engraved on the new stone.

# How many stones are present after blinking 25 times?


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


# Convert the list containing the single string into
# a list of integers.
def parseInput(values):
   stones = [ int(x) for x in values[0].split() ]
   
   return stones
   

if __name__ == '__main__':
   # Read and parse input to list of tuples.
   values = readFile("input11b.txt")
   stones = parseInput(values)
   # Blink 25 times.
   for blink in range(25):
      # Create the new row of stones.
      new_stones = []
      for stone in stones:
         # Apply the three rules (the first one that
         # holds.
         if stone == 0:
            new_stones.append(1)
         elif (len(str(stone)) % 2) == 0:
            stone_str = str(stone)
            mid = len(stone_str)//2
            s1 = int(stone_str[:mid])
            s2 = int(stone_str[mid:])
            new_stones.append(s1)
            new_stones.append(s2)
         else:
            new_stones.append(stone * 2024)

      stones = new_stones

      # Print the number of stones present after the blink.
      print(str(blink + 1) + ': ' + str(len(stones)))
   
