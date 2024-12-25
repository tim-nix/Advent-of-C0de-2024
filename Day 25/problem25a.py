# The input file contains a series of locks and keys
# (each a 5x7 grid). The locks are schematics that
# have the top row filled (#) and the bottom row empty
# (.); the keys have the top row empty and the bottom
# row filled.

# A key fits a lock if in the columns, the pins and
# key don't overlap.

# Determine how many unique lock/key pairs fit
# together without overlapping in any column


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


# Break the list of strings into a list of locks and a
# list of keys. The locks are schematics that have the
# top row filled (#) and the bottom row empty (.); the
# keys have the top row empty and the bottom row
# filled.
def parseInput(values):
   # An extra empty string at the end completes the
   # structure of the last key (keys are listed last).
   values.append('')
   locks = []
   keys = []

   # Get the next group of rows.
   next_group = []
   for line in values:
      if line != '':
         next_group.append(line)
      else:
         # Add the group as either a lock or a key.
         if (next_group[0] == '#####') and (next_group[-1] == '.....'):
            locks.append(next_group)
         else:
            keys.append(next_group)
         next_group = []

   # Return the list of locks and the list of keys.
   return (locks, keys)


# Convert the grid representation of the lock/key into
# a representation in which the pins in the schematic
# are a list of heights, one per column.
def convert(device):
   count = [ 0, 0, 0, 0, 0 ]
   # The first and last row are not checked.
   for y in range(1, len(device) - 1):
      for x in range(len(device[y])):
         if device[y][x] == '#':
            count[x] += 1

   return count

            
if __name__ == '__main__':
   # Read the input from the file and parse it into
   # a list of locks and a list of keys.
   values = readFile("input25b.txt")
   locks, keys = parseInput(values)

   # Convert the locks and keys into the height-based
   # representation of each.
   num_locks = [ convert(lock) for lock in locks ]
   num_keys  = [ convert(key) for key in keys ]

   # For each lock, try all keys to see if there is a
   # match. Keep count of matches. Multiple keys can
   # fit the same lock (each count as separate match).
   matches = 0
   for lock in num_locks:
      for key in num_keys:
         unlock = [ lock[x] + key[x] for x in range(len(key)) ]
         overlap = False
         if max(unlock) <= 5:
            matches += 1

   # Display the result.
   print('Number of matches: ' + str(matches))

   
