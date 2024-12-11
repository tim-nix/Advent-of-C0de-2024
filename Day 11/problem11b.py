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

# How many stones are present after blinking 75 times?

# The computational complexity for the direct
# computation (as applied in Part One) is too high. So
# we need a different approach.


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

   # Create a dictionary for each unique stone and the
   # number of times that the stones with the same
   # label occurs (for the input arrangement).
   stones_found = dict()
   for stone in stones:
      if stone not in stones_found:
         stones_found[stone] = 1
      else:
         stones_found[stone] += 1

   # Create a dictionary of mappings from a marked
   # stone to the generated stone arrangement that
   # occurs after each phase.
   map_set = dict()

   # num_phases * blinks_per_phase = 75
   num_phases = 15
   blinks_per_phase = 5
   
   # Iterate through each phase.
   for phase in range(num_phases):
      print('phase = ' + str(phase + 1))

      # For each phase, create a dictionary of
      # occurrences for each stone encountered.
      phase_stones_found = dict()

      # For each unique marking in the previous phase.
      for stone in stones_found:
         # If the mapping does not exist, discover it.
         if stone not in map_set:
            stones2 = [ stone ]
            for blink in range(blinks_per_phase):
               new_stones = []
               for s in stones2:
                  if s == 0:
                     new_stones.append(1)
                  elif (len(str(s)) % 2) == 0:
                     stone_str = str(s)
                     mid = len(stone_str)//2
                     s1 = int(stone_str[:mid])
                     s2 = int(stone_str[mid:])
                     new_stones.append(s1)
                     new_stones.append(s2)
                  else:
                     new_stones.append(s * 2024)
                     
               stones2 = new_stones

            # Add the mapping to the dictionary of
            # mappings.
            map_set[stone] = stones2

         # Add each stone in the mapping, add the number
         # of times that it occurs at the end of the phase.
         for s in map_set[stone]:
            if s not in phase_stones_found:
               phase_stones_found[s] = stones_found[stone]
            else:
               phase_stones_found[s] += stones_found[stone]

      # Set up for the next phase.
      stones_found = phase_stones_found

      # Count the total number of stones found at the
      # end of the phase.
      found = 0
      for key in stones_found:
         found += stones_found[key]

      # Print the number of stones.
      print('After phase ' + str(phase + 1) + ': ' + str(found))

   
