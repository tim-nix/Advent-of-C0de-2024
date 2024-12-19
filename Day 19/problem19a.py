# Given a list of designs (each a long sequence of
# stripe colors) and a list of patterns (each a single
# towel), determine how many of the designs are
# possible; that is, how many can be constructed using
# by concantenating some combination of the patterns.


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


# The values parameter contains the data read in from
# the input file. The first line indicates the
# available towel patterns. After the blank line, the
# remaining lines each describe a design the onsen
# would like to display.
def parseInput(values):
   pre_trim = values[0].split(',')
   patterns = [ p.strip() for p in pre_trim ]
   designs = [ p for p in values[2:] ]

   return (patterns, designs)


# Determines if the design can be constructed using
# the patterns.  Works by slicing the first characters
# from the design and cheching if the slice matches a
# pattern. Continues until a match for the entire
# design is made or not more progress is made.
def isPossible(design, patterns, min_length, max_length):
   progress = [ design ]
   while len(progress) > 0:
      next_round = []
      # Check each remaining possible design.
      for p in progress:
         # Check each slice length (limited by the
         # length of the patterns).
         for i in range(min_length, max_length + 1):
            # The slice matches a pattern.
            if p[:i] in patterns:
               # Matched the entire remaining design.
               if p[i:] == '':
                  return True
               # Still some remaining design after the
               # match, so add it for checking in the
               # next round.
               else:
                  next_round.append(p[i:])

      # Set up for the next round.
      progress = next_round

   # No match was found
   return False


if __name__ == '__main__':
   # Read and parse input to a list the available
   # towel patterns and a list describing the
   # designs to display.
   values = readFile("input19b.txt")
   patterns, designs = parseInput(values)

   # Find length of shortest and longest patterns.
   # Used by isPossible() to restrict search space.
   min_length = 1000
   max_length = 0
   for p in patterns:
      if len(p) < min_length:
         min_length = len(p)
      if len(p) > max_length:
         max_length = len(p)

   # Trim out the patterns that can be constructed
   # from other patterns. Keep patterns as a list for
   # iteration and order (though lookup is longer).
   i = 0
   while i < len(patterns):
      test = patterns.pop(i)
      if not isPossible(test, patterns, min_length, max_length):
         patterns.insert(i, test)
         i += 1

   # Lookup in a set is faster.
   patterns = set(patterns)

   # Count number of designs that are possible. 
   good_designs = 0
   for design in designs:
      if isPossible(design, patterns, min_length, max_length):
         good_designs += 1

   # Display the results.
   print('Designs that are possible: ' + str(good_designs))

         
            
      
         

   
