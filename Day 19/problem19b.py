# Given a list of designs (each a long sequence of
# stripe colors) and a list of patterns (each a single
# towel), determine the sum of the different ways each
# design could be made.


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


# Count all the possible ways that the design can be
# made from the patterns. Use the global variable
# 'known' for storing known designs and their pattern
# count.
def countPossible(design, patterns, minL, maxL):
   # If design is 'known' then return its value.
   if design in known:
      return known[design]

   # If design is too small then return 0.
   if len(design) <= minL:
      #print(design + ' is minimal, so returning.')
      return 0

   # Check the possible prefixes based on the size
   # (minL and maxL characters).  Determine the number
   # of number of ways the design can be formed; that
   # is 'count'.
   count = 0
   for i in range(minL, min(maxL + 1, len(design))):
      # If the prefix matches a pattern, then recurse.
      if (design[:i] in patterns):
         count += countPossible(design[i:], patterns, minL, maxL)
         
   # Add 'design' to the cache of 'known'. 
   if count > 0:
      known[design] = count
      
   # Return the count.
   return count
   

if __name__ == '__main__':
   # Read and parse input to a list the available
   # towel patterns and a list describing the
   # designs to display.
   values = readFile("input19b.txt")
   patterns, designs = parseInput(values)

   #print('patterns = ' + str(patterns))

   # Find length of shortest and longest patterns.
   # Used by isPossible() to restrict search space.
   min_length = 1000
   max_length = 0
   for p in patterns:
      if len(p) < min_length:
         min_length = len(p)
      if len(p) > max_length:
         max_length = len(p)

   #print('min_length = ' + str(min_length))
   #print('max_length = ' + str(max_length))

   # Trim out the patterns that can be constructed
   # from other patterns. Keep patterns as a list for
   # iteration and order (though lookup is longer).
   trimmed = []
   i = 0
   while i < len(patterns):
      test = patterns.pop(i)
      if not isPossible(test, patterns, min_length, max_length):
         patterns.insert(i, test)
         i += 1
      else:
         trimmed.append(test)
      

   # Convert patterns from list to set for faster
   # checks.
   patterns = set(patterns)
   
   # Create a cache for storing known patterns for a
   # given design.
   global known
   known = dict()

   # All the base patterns (can't be formed from other
   # patterns) are added to the cache.
   for p in patterns:
      known[p] = 1

   # The order these are added back in matters, so
   # sort based on length.
   trimmed.sort(key=lambda s: len(s))

   # Now add all of the trimmed patterns back to
   # patterns and the cache. The correct value stored
   # in the cache is dependent on the order that
   # these are added back to the patterns.
   for p in trimmed:
      known[p] = countPossible(p, patterns, min_length, max_length) + 1
      patterns.add(p)

   # Count number of designs that are possible.
   good_designs = 0
   for design in designs:
      delta = countPossible(design, patterns, min_length, max_length)
      good_designs += delta

   # Display the results.
   print('Designs that are possible: ' + str(good_designs))

         
            
      
         

   
