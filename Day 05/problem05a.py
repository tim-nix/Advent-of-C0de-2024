# Determine the sum of middle elements for all
# correct orderings according to the rules. The
# rules and the orderings are contained within
# the input file. The first section of the input
# file specifies the page ordering rules, one
# per line. The second section specifies the
# page numbers of each update.

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


# Convert a list of strings into a list of
# orderings and a list of updates. The list
# of orderings will consist of tuples of
# integers. The list of updates will consist
# of a list of lists of integers.
def parseInput(values):
   # Split the input based on orderings and
   # updates
   split_index = values.index('')
   ordering = values[:split_index]
   # Convert orderings to tuples of integers
   order = []
   for o in ordering:
      lo, hi = o.split('|')
      order.append((int(lo), int(hi)))
   
   sequences = values[split_index+1:]
   # Convert updates to lists of integers
   updates = []
   for s in sequences:
      updates.append([ int(x) for x in s.split(',') ])

   return (order, updates)


# Check the update to ensure that it conforms
# to the ordering rules.
def check_update(update, order):
   for u in update:
      for o in order:
         # The current page matches the left side
         # of an order rule.
         if u == o[0]:
            #print('checking ' + str(update) + ' and order ' + str(o))
            # The right side of the rule is in the
            # update and is listed after the left
            # side of the rule in the update.
            if (o[1] in update) and (update.index(o[0]) > update.index(o[1])):
               return False

   return True


# Get the middle value within the update.
def getMiddle(update):
   middle_i = len(update) // 2
   return update[middle_i]


if __name__ == '__main__':
   # Read and parse input to a grid of characters.
   values = readFile("input5b.txt")
   order, updates = parseInput(values)

   sum = 0
   # Iterate through the updates
   for u in updates:
      # Check to see if the update is good
      if check_update(u, order):
         # If so, find middle value and add to sum
         sum += getMiddle(u)

   # Print the results
   print('sum of middle elements = ' + str(sum))
         

   
